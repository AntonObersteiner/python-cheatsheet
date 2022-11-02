tmux new-session -d -s cheats 'vim cheatsheet.py';
tmux split-window; tmux send 'vim segment.py' ENTER;
tmux split-window; tmux send 'vim preamble.tex' ENTER;
tmux split-window; tmux send 'vim Makefile' ENTER;
tmux next-layout;
echo "tmux attach -t cheats"
