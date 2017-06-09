#!/usr/bin/env sh

cd $D1ROOT/lib_common/src && python setup.py develop
cd $D1ROOT/lib_client/src && python setup.py develop
cd $D1ROOT/client_cli/src && python setup.py develop
cd $D1ROOT/client_onedrive/src && python setup.py develop
cd $D1ROOT/gmn/src && python setup.py develop
cd $D1ROOT/test_utilities/src && python setup.py develop
