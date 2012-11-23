#!/bin/bash

#
# Usage:
#
#         . ENV.SH
#

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
PWD="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

P=$PWD/lib

echo "Adding $P to PYTHONPATH"
export PYTHONPATH=$P:$PYTHONPATH
