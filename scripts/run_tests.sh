#!/usr/bin/env bash

set -e
set -o pipefail

readonly PREVIOUSWRKDIR="$(pwd)"
readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"


cd_project_root() {
    echo '> cd to project root'
    cd "${SCRIPTSDIR}" && cd ..
}

cd_previous_working_dir() {
    echo '> Restore previous working directory'
    [ -d "${PREVIOUSWRKDIR}" ] && cd "${PREVIOUSWRKDIR}"
}

run_pytest() {
    echo
    echo '> Run pytest'
    py.test .
}

run_flake8() {
    echo
    echo '> Run flake8'
    echo -n 'Total errors: '
    flake8 . --count
}

run_pylint() {
    echo
    echo '> Run pylint'
    pylint MarkdownShortcuts.py
}


main() {
    cd_project_root
    # run_pytest
    run_flake8
    run_pylint
    cd_previous_working_dir

    echo & echo 'Finished.'
}

main
