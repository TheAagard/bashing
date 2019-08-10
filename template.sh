#!/bin/bash
##
# XXX DESCRIPTION XXX
##

# bail out on error
set -e

# defaults


usage() {
    echo -e "Usage: $1 [-h]"
}

# parse args
POSARGS=()
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            usage $0
            exit 0
            ;;
        -*|--*)
            echo -e "ERROR: Illegal option: $key"
            usage $0
            exit 1
            ;;
        *)
            POSARGS+=("$1")
            shift
            ;;
    esac
done

# check positional args
if [[ ${#POSARGS[@]} -gt 0 ]]; then
    echo -e "ERROR: Too many arguments."
    usage $0
    exit 1
fi
set -- "${POSARGS[@]}"

# main program
