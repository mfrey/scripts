#!/bin/bash

# ./forerunner.sh script
#
# A shell script for exporting data from a Garmin Forerunner 305 sports watch. 
# 
# Author:    Michael Frey, mail -at- mfrey dot net
# License:   tba
#
# Requirements:
#
# 	- garmin-tools
#         library and scripts for accessing garmin devices
#         http://code.google.com/p/garmintools/
#
#       - gmn2tcx
#         script which transforms a gmn file into a tcx file
#         http://braiden.org/?p=62  (blog post about the tool with a link to the repository)
#         http://linuxnerd.net/svn/trunk/projects/garmin-dev  (subversion repository)
#	  
# Further information about using a Forerunner 305 under Linux:
#
#       - Garmin Forerunner 305 unter Linux (German)
#         http://dzys.wordpress.com/2010/01/28/garmin-forerunner-305-unter-linux/
#
#       - Garmin Forerunner 305 mit SportTracks unter Linux (German)
#         http://sporttracks.rissling.name/
#
#

set -e 

# format specifies for printing text
NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2; tput bold)
YELLOW=$(tput setaf 3)
RED=$(tput setaf 1)

# specifies which kernel module to unload
KERNEL_MODULE="garmin_gps"
# should debug output printed (overly verbose)
DEBUG=true
# set the sport tracks home
SPORT_TRACKS="/home/michael/Software/SportTracks"
# specify where the runs should be saved
SAVE_RUNS="$SPORT_TRACKS/runs/"


# print a string in red
function red() {
    echo -e "$RED$*$NORMAL"
}

# print a string in green
function green() {
    echo -e "$GREEN$*$NORMAL"
}

# print a string in yellow
function yellow() {
    echo -e "$YELLOW$*$NORMAL"
}

# format the debug output accordingly
function debug() { ((DEBUG)) && echo ">>> $*"; }

# check if the garmin tools have been installed
function require_garmin_tools() { which -s "garmin_save_runs"; }

# save the runs from the forerunner gps watch
function save_runs() {
    # check if the kernel module is unloaded
    if [ `lsmod | grep -o ^$KERNEL_MODULE` ]; then
        # unload the module
        rmmod $KERNEL_MODULE
	# has it worked to unload the module?
	if $? -eq 0 then 
            red "could not unload the kernel module: $KERNEL_MODULE"	
	else
            debug "removed kernel module $KERNEL_MODULE"
	fi
    fi 

    # try to save the runs
    garmin_save_runs > $SAVE_RUNS

    # check if it reading the runs
    if $? -eq 0 then
       green "read runs from forerunner"
    else
       red "something went wrong while reading runs from the device"
    fi

    # 

}

#function is_save_run_directory_set() {
#    if [ -z "$GARMIN_SAVE_RUNS" ]; then 
#        red "The GARMIN_SAVE_RUNS variable is not set."
#    fi
#}


# To print success
green "Task has been completed"

# To print error
red "The configuration file does not exist"

# To print warning
yellow "You have to use higher version."

#is_save_run_directory_set 

