backup=$HOME/OneDrive/task
mkdir backup
mkdir $HOME/.task
ln -sf $backup/completed.data $HOME/.task/completed.data
ln -sf $backup/pending.data $HOME/.task/pending.data
ln -sf $PWD/hooks $HOME/.task/hooks
mv $HOME/.taskrc $HOME/.taskrc.bak
echo "include $PWD/taskrc
context.work=+work
context.home=-work" > $HOME/.taskrc
