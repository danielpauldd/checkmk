#!/bin/bash

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

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

echo -e "${GREEN}create some filesystem links${NC}"

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
        if [ -L $DirNameLink ]; then
            echo -e "replace symlink ${DirNameLink}"
            rm $DirNameLink 2>/dev/null
            ln -sf ${PWD}/$DirName $DirNameLink
        # create symlink if no file exists
        elif [ ! -d $DirNameLink ]; then
            echo -e "${YELLOW}WARNING:${NC}: ${DirNameLink} was not there, create a new symlink!"
            ln -sf ${PWD}/$DirName $DirNameLink
        else
            echo -e "${RED}ERROR:${NC}: ${DirNameLink} is not a symlink. Abort."
        fi
        echo ""

    done

# cleanup pycache files
find -name *.pyc -type f -exec rm {} \; 2>/dev/null
find -name __pycache__ -type d -exec rmdir {} \; 2>/dev/null
