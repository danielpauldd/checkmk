#!/bin/bash

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Default value for the variable onlyPack (0 = false)
onlyPack=0


# Function to display help
show_help() {
    echo "Usage: $0 [-p] [-h]"
    echo "Options:"
    echo "  -p    Sets the variable onlyPack to '0' (true)."
    echo "  -h    Displays this help message and exits the script."
    exit 0
}


# Parameter processing with getopts
while getopts ":ph" opt; do
    case $opt in
        p)
            onlyPack=1 # Set to true
            ;;
        h)
            show_help
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            show_help
            ;;
    esac
done

# cd into the agent/check bundle directory and use relative paths
if [[ $BASH_SOURCE = */* ]]; then
    baseDir=${BASH_SOURCE%/*}
else
    baseDir=.
fi
#Abort if we are not in the correct directory
if [[ ${baseDir} != '.' ]]; then
    echo "Please cd into the agent/check bundle directory and try again."
    exit
fi

echo -e "${GREEN}unlink some filesystem links${NC}"

Plugins=`find -maxdepth 2 -type d -path "./cmk_addons_plugins/*"`
for DirName in ${Plugins[*]} 
    do
        #strip ./ from the beginning
        DirName=${DirName/.\//}
        
        #create short version, strip cmk_addons_plugins/ from the beginning
        DirNameShort=${DirName/cmk_addons_plugins\//}
        echo -e "${GREEN}$DirNameShort${NC}"
        
        # test if there is already something installed
        DirNameLink="${OMD_ROOT}/local/lib/python3/cmk_addons/plugins/${DirNameShort}" 
        
        # only relink the files when -p was not provided
        if [ $onlyPack -ne 1 ]; then
            if [ -L $DirNameLink ]; then
                echo -e "remove symlink ${DirNameLink}"
                rm $DirNameLink 2>/dev/null
            # create symlink if no file exists
            elif [ ! -d $DirNameLink ]; then
                echo -e "${DirNameLink} was not there, nothing to do!"
            else
                echo -e "${RED}ERROR:${NC}: ${DirNameLink} is not a symlink. Abort."
                break
            fi
            echo ""

            # cleanup pycache files
            find -name *.pyc -type f -exec rm {} \; 2>/dev/null
            find -name __pycache__ -type d -exec rmdir {} \; 2>/dev/null

            cp -r "$DirName/" "$DirNameLink"
        fi
        if [ ! -e ${DirNameShort}.manifest.temp ]; then
            mkp template $DirNameShort
            vi ${OMD_ROOT}/tmp/check_mk/${DirNameShort}.manifest.temp
            cp ${OMD_ROOT}/tmp/check_mk/${DirNameShort}.manifest.temp ${DirNameShort}.manifest.temp
        else
            vi ${DirNameShort}.manifest.temp
        fi
        mkp package ${DirNameShort}.manifest.temp
        cp ${OMD_ROOT}/local/share/check_mk/enabled_packages/${DirNameShort}*.mkp .
    done
