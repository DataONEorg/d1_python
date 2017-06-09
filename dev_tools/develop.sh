#!/usr/bin/env sh

cd $D1ROOT/d1_python/lib_common/src && python setup.py develop
cd $D1ROOT/d1_python/lib_client/src && python setup.py develop
cd $D1ROOT/d1_python/client_cli/src && python setup.py develop
cd $D1ROOT/d1_python/client_onedrive/src && python setup.py develop
cd $D1ROOT/d1_python/gmn/src && python setup.py develop
cd $D1ROOT/d1_python/test_utilities/src && python setup.py develop
