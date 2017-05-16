#!/usr/bin/env bash

PIP_INDEX_URL=http://${DEVPI_SERVER}:3141/${DEVPI_USER}/dev/+simple/
/var/local/dataone/gmn_venv/bin/pip install --upgrade --trusted-host ${DEVPI_SERVER} dataone.gmn
