#!/bin/bash

NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2; tput bold)
YELLOW=$(tput setaf 3)
RED=$(tput setaf 1)

function red() {
    echo -e "$RED$*$NORMAL"
}

function green() {
    echo -e "$GREEN$*$NORMAL"
}

function yellow() {
    echo -e "$YELLOW$*$NORMAL"
}

#function save_runs() {
#garmin_save_runs > ~michael/Software/SportTracks/runs.txt
#}

function is_save_run_directory_set() {
    if [ -z "$GARMIN_SAVE_RUNS" ]; then 
        red "VAR is unset"
    fi
}

# To print success
green "Task has been completed"

# To print error
red "The configuration file does not exist"

# To print warning
yellow "You have to use higher version."

is_save_run_directory_set 

