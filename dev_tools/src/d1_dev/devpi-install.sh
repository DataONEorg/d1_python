ssh -R3141:localhost:3141 pangaea-dev-orc-1.test.dataone.org

$ export PIP_INDEX_URL=http://localhost:3141/dahl/dev/+simple/

$ . gmn_venv/bin/activate
$ pip install --upgrade --trusted-host localhost dataone.gmn

#!/usr/bin/env bash

DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/devpi-settings.sh"

export PIP_INDEX_URL=http://${DEVPI_SERVER}:3141/${DEVPI_USER}/dev/+simple/
/var/local/dataone/gmn_venv/bin/pip install --upgrade --trusted-host ${DEVPI_SERVER} dataone.gmn
