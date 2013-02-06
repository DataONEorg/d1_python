# ./pyxb/bundles/dc/raw/dcmitype.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:049d2b1ce34c6b814456fe5b9055f12be5a680b0
# Generated 2012-12-17 13:09:37.611568 by PyXB version 1.2.1
# Namespace http://purl.org/dc/dcmitype/ [xmlns:dcmitype]

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:4d0fbd32-487d-11e2-bfa7-c8600024e903')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'http://purl.org/dc/dcmitype/', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.
    
    @kw default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    saxer.parse(StringIO.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.Name, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/dc/schemas/dcmitype.xsd', 33, 8)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.Collection = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Collection', tag=u'Collection')
STD_ANON.Dataset = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Dataset', tag=u'Dataset')
STD_ANON.Event = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Event', tag=u'Event')
STD_ANON.Image = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Image', tag=u'Image')
STD_ANON.MovingImage = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'MovingImage', tag=u'MovingImage')
STD_ANON.StillImage = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'StillImage', tag=u'StillImage')
STD_ANON.InteractiveResource = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'InteractiveResource', tag=u'InteractiveResource')
STD_ANON.Service = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Service', tag=u'Service')
STD_ANON.Software = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Software', tag=u'Software')
STD_ANON.Sound = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Sound', tag=u'Sound')
STD_ANON.Text = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Text', tag=u'Text')
STD_ANON.PhysicalObject = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'PhysicalObject', tag=u'PhysicalObject')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Union simple type: {http://purl.org/dc/dcmitype/}DCMIType
# superclasses pyxb.binding.datatypes.anySimpleType
class DCMIType (pyxb.binding.basis.STD_union):

    """Simple type that is a union of STD_ANON."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DCMIType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/dc/schemas/dcmitype.xsd', 31, 2)
    _Documentation = None

    _MemberTypes = ( STD_ANON, )
DCMIType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=DCMIType)
DCMIType._CF_pattern = pyxb.binding.facets.CF_pattern()
DCMIType.Collection = u'Collection'               # originally STD_ANON.Collection
DCMIType.Dataset = u'Dataset'                     # originally STD_ANON.Dataset
DCMIType.Event = u'Event'                         # originally STD_ANON.Event
DCMIType.Image = u'Image'                         # originally STD_ANON.Image
DCMIType.MovingImage = u'MovingImage'             # originally STD_ANON.MovingImage
DCMIType.StillImage = u'StillImage'               # originally STD_ANON.StillImage
DCMIType.InteractiveResource = u'InteractiveResource'# originally STD_ANON.InteractiveResource
DCMIType.Service = u'Service'                     # originally STD_ANON.Service
DCMIType.Software = u'Software'                   # originally STD_ANON.Software
DCMIType.Sound = u'Sound'                         # originally STD_ANON.Sound
DCMIType.Text = u'Text'                           # originally STD_ANON.Text
DCMIType.PhysicalObject = u'PhysicalObject'       # originally STD_ANON.PhysicalObject
DCMIType._InitializeFacetMap(DCMIType._CF_enumeration,
   DCMIType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'DCMIType', DCMIType)
