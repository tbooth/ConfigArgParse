#!/bin/bash
# This bash script builds the API documentation for ConfigArgParse.

# Change to the source directory path.
cd -P "$( dirname "${BASH_SOURCE}" )"

# Stop if errors
set -euo pipefail
IFS=$'\n\t,'

# Figure the project version
project_version="$(setuptools-git-versioning)"
printf 'Project version is %s, according to setuptools-git-versioning\n' "$project_version"

# Figure commit ref or tag
git_sha="$(git rev-parse HEAD)"
if ! git describe --exact-match --tags > /dev/null 2>&1 ; then
    is_tag=false
else
    git_sha="$(git describe --exact-match --tags)"
    is_tag=true
fi

# Init output folder
docs_folder="./apidocs/"
rm -rf "${docs_folder}"
mkdir -vp "${docs_folder}"

# We generate the docs for the argparse module too, such that we can document
# the methods inherited from argparse.ArgumentParser, not only the methods that configargparse overrides.
# And it help to have a better vision of the whole thing also.
if [ ! -e argparse.py ] ; then
    curl https://raw.githubusercontent.com/python/cpython/3.13/Lib/argparse.py > ./argparse.py
    echo "__docformat__ = 'restructuredtext'" >> ./argparse.py

    # Delete the file when the script exits
    trap "rm -f argparse.py" EXIT
fi

# Allow the PROJECT_URL to be overridden by the caller
PROJECT_URL="${PROJECT_URL:-https://github.com/bw2/ConfigArgParse}"

set +e
pydoctor \
    --project-name="ConfigArgParse ${project_version}" \
    --project-url="${PROJECT_URL}" \
    --html-viewsource-base="${PROJECT_URL}/tree/${git_sha}" \
    --intersphinx=https://docs.python.org/3/objects.inv \
    --make-html \
    --quiet \
    --project-base-dir=.\
    --docformat=google \
    --html-output="${docs_folder}" \
    ./argparse.py ./configargparse.py

if [ "$?" = 0 ] ; then
    printf '\n%s\n' "API docs generated in ${docs_folder}"
elif [ -e "${docs_folder}/index.html" ] ; then
    printf '\n%s\n' "API docs generated in ${docs_folder} with errors"
fi

