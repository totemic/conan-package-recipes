#!/bin/bash

# Create a list of mount points from the repository's parent directory and PWD,
# _NOT_ including $HOME because mounting $HOME (really, any parent of $HOME/Library)
# can cause 100% cpu usage on Mac even when no container is running. If you have
# 100% CPU usage, you may need to click "Reset to factory defaults" on Docker to fix
# https://github.com/docker/for-mac/issues/5164#issuecomment-857760561

# https://stackoverflow.com/a/18443300
realpath() {
  local OURPWD=$PWD
  cd "$(dirname "$1")"
  local LINK=$(readlink "$(basename "$1")")
  while [ "$LINK" ]; do
    cd "$(dirname "$LINK")"
    local LINK=$(readlink "$(basename "$1")")
  done
  local REALPATH="$PWD/$(basename "$1")"
  cd "$OURPWD"
  echo "$REALPATH"
}

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Since the script is in repo/tools, repo dir is one up
repo_dir=$(realpath "$script_dir/..")
# Some sibling repos call our tools (such as mmwave-driver), so attempt to mount the parent dir
repo_parent_dir=$(realpath "$repo_dir/..")

mount_dirs=""

# printf %q is used below to change " " to "\ ". Docker seems to have issues with
# accepting Quoted paths as parameters to -v

# Add repo_parent_dir as volume as long as it isn't at $HOME
if [[ ! "$script_dir" -ef "$HOME" ]] && [[ ! "$repo_dir" -ef "$HOME" ]]; then
    if [[ ! "$repo_parent_dir" -ef "$HOME" ]]; then
        first_mount=$(printf %q "$repo_parent_dir")
    else
        # The repo's parent directory was $HOME, so give up and just include the repo directory itself
        first_mount=$(printf %q "$repo_dir")
    fi
    mount_dirs="$mount_dirs -v$first_mount:$first_mount:delegated"
fi

# if pwd isn't inside repo_parent_dir and isn't $USER, add it to the volumes
if [[ "${PWD##$repo_parent_dir}" == "$PWD" ]] && [[ ! "$PWD" -ef "$HOME" ]]; then
    second_mount=$(printf %q "$repo_dir")
    mount_dirs="$mount_dirs -v$second_mount:$second_mount:delegated"
fi

echo -n "$mount_dirs"
