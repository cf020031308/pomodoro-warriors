dir="$0"
while [ -L "${dir}" ]
do dir=$(readlink "${dir}")
done
dir=$(cd $(dirname "${dir}"); pwd)

if [ "$1" ]; then
    taskd="$1/taskwarrior"
    timed="$1/timewarrior"
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
