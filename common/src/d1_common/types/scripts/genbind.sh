#!/usr/bin/env bash

# Adapted from PyXB distribution for dc bindings
# To use:
#   1. checkout d1_common_python
#   2. cd d1_common_python/src
#   3. export D1COMMON_ROOT=$(pwd)
#   4. bash ${D1COMMON_ROOT}/d1_common/types/scripts/genbind.sh
#
# - DV

# Attempt to prevent catastrophe by validating required settings
# and aborting on any subshell error
set -e
if [ -z "${D1COMMON_ROOT+notset}" ] ; then
  echo 1>&2 ERROR: D1COMMON_ROOT not set
  exit 1
fi

BUNDLE_TAG=types
MODULE_PREFIX=d1_common.${BUNDLE_TAG}
BUNDLE_ROOT=${D1COMMON_ROOT}/d1_common/${BUNDLE_TAG}
SCHEMA_DIR=${BUNDLE_ROOT}/schemas
GENERATED_DIR=${BUNDLE_ROOT}/generated
ARCHIVE_DIR=${GENERATED_DIR}

rm -rf ${GENERATED_DIR}
mkdir -p ${GENERATED_DIR}
touch ${GENERATED_DIR}/__init__.py

( mkdir -p ${SCHEMA_DIR} \
  && cd ${SCHEMA_DIR} \
  && ( [ -f dataoneErrors.xsd ] || wget -O "dataoneErrors.xsd" "http://ns.dataone.org/service/errors/v1" ) \
  && ( [ -f dataoneTypes.xsd  ] || wget -O "dataoneTypes.xsd" "http://ns.dataone.org/service/types/v1" ) \
  && ( [ -f dataoneTypes_v1.1.xsd ] || wget -O "dataoneTypes_v1.1.xsd" "http://ns.dataone.org/service/types/v1.1" ) \
  && ( [ -f dataoneTypes_v2.0.xsd ] || wget -O "dataoneTypes_v2.0.xsd" "http://ns.dataone.org/service/types/v2.0" )
) || failure unable to obtain schema

pyxbgen \
 --module-prefix=${MODULE_PREFIX} \
 --write-for-customization \
 --archive-to-file=${ARCHIVE_DIR}/dataone_types.wxs \
 --schema-root=${SCHEMA_DIR} \
 --import-augmentable-namespace "http://ns.dataone.org/service/errors/v1" \
 -u dataoneTypes.xsd -m dataoneTypes_v1 \
 -u dataoneTypes_v1.1.xsd -m dataoneTypes_v1_1 \
 -u dataoneTypes_v2.0.xsd -m dataoneTypes_v2_0

 pyxbgen \
  --module-prefix=${MODULE_PREFIX} \
  --write-for-customization \
  --schema-root=${SCHEMA_DIR} \
  -u dataoneErrors.xsd -m dataoneErrors
