#!/bin/sh -

function realdir() {
    fpath="$1"
    while [ -L "${fpath}" ]
    do fpath=$(readlink "${fpath}")
    done
    if [ ! -d "${fpath}" ]; then
        fpath=$(dirname "${fpath}")
    fi
    cd "${fpath}"
    pwd
}

if [ "$1" ]; then
    dst=$(realdir "$1")
    taskd="${dst}/taskwarrior"
    timed="${dst}/timewarrior"
    mkdir -p "${taskd}" "${timed}"
    if [ -d "$HOME/.task" ]; then
        cp "$HOME/.task/*.data" "${taskd}"
    fi
    echo "data.location=${taskd}" >> "$HOME/.taskrc"
    if [ -d "$HOME/.timewarrior/data" ]; then
        mv "$HOME/.timewarrior/data" "${timed}"
    else
        mkdir "${timed}/data"
        if [ ! -d "$HOME/.timewarrior" ]; then
            mkdir "$HOME/.timewarrior"
        fi
    fi
    ln -s "${timed}/data" "$HOME/.timewarrior/"
else
    taskd="$HOME/.task"
    timed="$HOME/.timewarrior"
    mkdir -p "${taskd}" "${timed}"
fi

dir=$(realdir "$0")
if [ -d "${taskd}/hooks" ]; then
    mv "${taskd}/hooks" "${taskd}/hooks.bak"
fi
ln -s "${dir}/taskwarrior/hooks" "${taskd}/hooks"
echo "include ${dir}/taskwarrior/taskrc" >> "$HOME/.taskrc"

if [ -d "${timed}/extensions" ]; then
    mv "${timed}/extensions" "${timed}/extensions.bak"
fi
ln -s "${dir}/timewarrior/extensions" "${timed}/extensions"
cat "${dir}/timewarrior/timewarrior.cfg" >> "${timed}/timewarrior.cfg"
