#!/bin/bash

gnome-terminal -- zsh -c "python3 ./Backend_endpoint/commsBack.py; exec zsh"
sleep 2

# waiting for the programs to start their sockets. Won't really be necessary after the first time, but works better this way.

gnome-terminal -- zsh -c "python3 ./terminal_gui/termEMU.py; exec zsh"
sleep 2

gnome-terminal -- zsh -c "python3 ./Sequencer/sequencer.py; exec zsh"
sleep 2

for i in {5001..5006}; do
    gnome-terminal -- zsh -c "python3 ./extraction_models/models/client_${i}.py; exec zsh"
done
