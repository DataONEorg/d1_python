#!/usr/bin/env bash

if [ -z "$DEVPI_USER" ]; then
    echo "Must set DEVPI_USER"
    exit 1
fi

if [ -z "$DEVPI_PW" ]; then
    echo "Must set DEVPI_PW"
    exit 1
fi

devpi user -c ${DEVPI_USER} password=${DEVPI_PW}
devpi login ${DEVPI_USER} --password=${DEVPI_PW}
devpi index -c dev bases=root/pypi
devpi use ${DEVPI_USER}/dev
#devpi use ~/dev

cd ~/dev/d1_python/lib_common/src && devpi upload --formats=bdist_wheel
cd ~/dev/d1_python/lib_client/src && devpi upload --formats=bdist_wheel
cd ~/dev/d1_python/client_cli/src && devpi upload --formats=bdist_wheel
cd ~/dev/d1_python/gmn/src && devpi upload --formats=bdist_wheel
