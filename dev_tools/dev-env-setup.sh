#!/usr/bin/env bash

# Set the DataONE Python packages up for development.

sudo pip install --upgrade pip
sudo pip install --upgrade setuptools
sudo pip install coverage

cd ~/d1-git/d1_python/d1_common_python/src && sudo python setup.py develop
cd ~/d1-git/d1_python/d1_libclient_python/src && sudo python setup.py develop
cd ~/d1-git/d1_python/d1_test_utilities_python/src && sudo python setup.py develop
cd ~/d1-git/d1_python/d1_mn_generic/src/gmn && sudo python ../setup.py develop
cd ~/d1-git/d1_python/d1_client_cli/src && sudo python setup.py develop


./lib_common ./lib_client ./test_utilities ./gmn ./client_cli ./client_onedrive
