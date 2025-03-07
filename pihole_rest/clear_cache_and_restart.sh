#!/bin/bash
# cleanup pycache files
find -name *.pyc -type f -exec rm {} \; 2>/dev/null
find -name __pycache__ -type d -exec rmdir {} \; 2>/dev/null
omd restart apache
