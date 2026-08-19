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

echo -e "${GREEN}create some filesystem links (cmk_addons_plugins)${NC}"

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

        #check if there is an mkp package
        version=$(mkp list | grep ${DirNameShort} | grep Enabled | awk '{print $2}')
        if [ -n "$version" ]; then
            echo -e "${YELLOW}mkp $DirNameShort $version gefunden, deaktiviere das MKP{NC}"
            mkp disable ${DirNameShort} ${version}
            rm -rf $DirNameLink 2>/dev/null
        fi
        
        if [ -L $DirNameLink ]; then
            echo -e "create symlink ${DirNameLink} -> ${PWD}/$DirName"
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

# Alle Dateien finden und dann Ordner/Dateien mit
# cmk_addons_plugins/ .git/ .vscode/ und alle .gitkeep Files ausschliessen
Files=`find -type f -path "${baseDir}/*/*" | grep -E -v "(^|/)(cmk_addons_plugins|.git|.vscode)/|.gitkeep"`
for filename in ${Files[*]}; do
    
    #strip ./ from the beginning
    filename=${filename/.\//}
    if test -f "${PWD}/${filename}"; then
        filelink="${OMD_ROOT}/local/${filename}" 
        # replace file with symlink when it's already a symlink (or it's forced)
        if [ -L $filelink ] || $FORCE; then
            echo -e "${GREEN}symlink $filelink to $filename${NC}"
            rm $filelink 2>/dev/null
            mkdir -p $(dirname "$filelink") 2>/dev/null
            ln -sf ${PWD}/$filename $filelink
        # create symlink if no file exists
        elif [ ! -f $filelink ]; then
            echo -e "${YELLOW}WARNING:${NC}: ${filelink} was not there, create a new symlink!"
            ln -sf ${PWD}/$filename $filelink
        else
            echo -e "${RED}ERROR:${NC}: ${filelink} is not a symlink. Abort."
        fi
    fi
    echo ""
done

# cleanup pycache files
find -name *.pyc -type f -exec rm {} \; 2>/dev/null
find -name __pycache__ -type d -exec rmdir {} \; 2>/dev/null
