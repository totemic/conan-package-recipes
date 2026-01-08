#!/bin/bash
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# Since the script is in repo/tools, repo dir is one up
repo_dir="$( cd "$script_dir/.." >/dev/null 2>&1 && pwd )"
repos_dir="$( cd "$repo_dir/.." >/dev/null 2>&1 && pwd )"

# https://hub.docker.com/r/conanio/gcc8-armv8
TAG=conanio/gcc8-armv8:1.45.0

pushd "${script_dir}" > /dev/null

# make sure the permissions are tight enough, otherwise ssh won't let us use the key.
# Sometimes the permissions are set to the wrong value after checking out from git
chmod 600 "$script_dir"/arm-ssh-key

# remove running container
docker rm -f clion_remote-arm-cc

#ssh-keygen -t ed25519 -f "$script_dir"/arm-ssh-key
# build new image
docker build --build-arg UID="$(id -u)" --build-arg GID="$(id -g)" --build-arg TAG="${TAG}" --build-arg SSH_KEY="$(cat "$script_dir"/arm-ssh-key.pub)" -t koko/remote-arm-cc:latest -f Dockerfile.remote-arm-cc .
# use consistency level delegated to speed up access from docker. https://docs.docker.com/docker-for-mac/osxfs-caching/
popd

# remove previous backup of known_hosts
rm -f "$HOME/.ssh/known_hosts.old"
# remove known_hosts entry so that next ssh will use the correct entry
ssh-keygen -f "$HOME/.ssh/known_hosts" -R "[localhost]:2222"

# start new one -v$HOME/.conan/data:$HOME/.conan/data:delegated -eCONAN_USER_HOME=$HOME
# /home/conan/embedded-sw is the path configured in CLion deploy path mapping
docker run -d --cap-add sys_ptrace -p127.0.0.1:2222:22 -v"$repos_dir":/home/conan/repos -v"$HOME/.conan":/home/conan/.conan:delegated -eIS_DOCKER_ENV=1 -eCC_ARCH=arm64 --name clion_remote-arm-cc koko/remote-arm-cc:latest
# Get mount points based on the location of this script (parent of repo, and PWD as long as neither is $HOME)
#docker_mounts="$("${script_dir}"/docker-mount-dirs.sh)"
#docker run -d --cap-add sys_ptrace -p127.0.0.1:2222:22 $docker_mounts -v"$HOME/.conan":"$HOME/.conan":delegated -v/private:/private:delegated -eIS_DOCKER_ENV=1 -eCC_ARCH=arm64 -eDESTDIR -eCONAN_USER_HOME=$HOME --name clion_remote-arm-cc koko/remote-arm-cc:latest

echo
echo "to login, run:"
echo
echo "ssh -i ${script_dir}/arm-ssh-key -p 2222 conan@localhost"
echo