#!/bin/sh
# Generates serializers for the various core classes defined by xml schema.
# Depends on PyXB ( http://pyxb.sourceforge.net/userref_pyxbgen.html )
#
# 20100628 - Dave Vieglais for DataONE.org
# Execute this script in the src folder of the distribution after any
# changes to the xmlschema definitions.


BASEURL="https://repository.dataone.org/software/cicore/trunk/schemas"
pyxbgen --binding-root d1common/types/generated \
        -u $BASEURL/logging.xsd -m logging \
        -u $BASEURL/noderegistry.xsd -m noderegistry \
        -u $BASEURL/objectlist.xsd -m objectlist \
        -u $BASEURL/systemmetadata.xsd -m systemmetadata
