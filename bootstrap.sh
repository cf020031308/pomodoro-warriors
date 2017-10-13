mkdir $HOME/.task
ln -sf $HOME/OneDrive/task/completed.data $HOME/.task/completed.data
ln -sf $HOME/OneDrive/task/pending.data $HOME/.task/pending.data
ln -sf $PWD/hooks $HOME/.task/hooks
mv $HOME/.taskrc $HOME/.taskrc.bak
echo "include $PWD/taskrc" > $HOME/.taskrc
