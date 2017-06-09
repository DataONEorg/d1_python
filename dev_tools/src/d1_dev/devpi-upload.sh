#!/usr/bin/env bash

devpi user -c ${DEVPI_USER} password=${DEVPI_PW}
devpi login ${DEVPI_USER} --password=${DEVPI_PW}
devpi index -c dev bases=root/pypi
devpi use ${DEVPI_USER}/dev

cd ~/d1-git/d1_python/d1_common_python/src && devpi upload --formats=bdist_wheel
cd ~/d1-git/d1_python/d1_libclient_python/src && devpi upload --formats=bdist_wheel
cd ~/d1-git/d1_python/d1_client_cli/src && devpi upload --formats=bdist_wheel
cd ~/d1-git/d1_python/d1_mn_generic/src && devpi upload --formats=bdist_wheel
