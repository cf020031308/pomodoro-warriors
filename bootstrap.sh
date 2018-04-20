ln -s $PWD/taskwarrior/ $HOME/.task
ln -s $PWD/timewarrior/ $HOME/.timewarrior
echo "include ~/.task/taskrc
context.inbox=-PROJECT
context.work=project:ks or due.before:tomorrow
context.home=project.not:ks +PROJECT" > ~/.taskrc

if [ $1 ]; then
    mkdir -p $1/task/time
    touch $1/task/time{completed.data,pending.data}
    ln -sf $1/task/completed.data $HOME/.task/completed.data
    ln -sf $1/task/pending.data $HOME/.task/pending.data
    ln -sf $1/task/time $HOME/.timewarrior/data
fi
