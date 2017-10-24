# taskwarrior

backup=$HOME/OneDrive/task
mkdir backup
mkdir $HOME/.task
ln -sf $backup/task/completed.data $HOME/.task/completed.data
ln -sf $backup/task/pending.data $HOME/.task/pending.data
ln -sf $PWD/taskwarrior/hooks $HOME/.task/hooks
mv $HOME/.taskrc $HOME/.taskrc.bak
echo "include $PWD/taskwarrior/taskrc
context.work=+work
context.home=-work" > $HOME/.taskrc

# timewarrior
mkdir $HOME/.timewarrior
ln -sf backup/time $HOME/.timewarrior/data
ln -sf $PWD/timewarrior.cfg $HOME/.timewarrior/timewarrior.cfg
