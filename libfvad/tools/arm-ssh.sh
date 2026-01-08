#!/bin/bash
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ssh -i "$script_dir"/arm-ssh-key -p 2222 -t conan@localhost "$@"