# ./d1_common/types/generated/dataoneTypes_v2_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:cdd9555a55a103332598275a87c4a7c1422c46ed
# Generated 2017-10-17 10:39:46.783181 by PyXB version 1.2.6 using Python 2.7.12.final.0
# Namespace http://ns.dataone.org/service/types/v2.0


import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:c93058c6-b359-11e7-b444-080027018ba0')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
from . import dataoneTypes_v1 as _ImportedBinding_dataoneTypes_v1

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://ns.dataone.org/service/types/v2.0', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
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
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Complex type {http://ns.dataone.org/service/types/v2.0}MediaTypeProperty with content type SIMPLE
class MediaTypeProperty (pyxb.binding.basis.complexTypeDefinition):
    """Additional optional properties for MediaType as
          described by IANA."""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MediaTypeProperty')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 63, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpns_dataone_orgservicetypesv2_0_MediaTypeProperty_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 70, 10)
    __name._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 70, 10)
    
    name = property(__name.value, __name.set, None, 'The property name for this entry.\n                ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.MediaTypeProperty = MediaTypeProperty
Namespace.addCategoryObject('typeBinding', 'MediaTypeProperty', MediaTypeProperty)


# Complex type {http://ns.dataone.org/service/types/v2.0}MediaType with content type ELEMENT_ONLY
class MediaType (pyxb.binding.basis.complexTypeDefinition):
    """Value drawn from the value space of IANA Media Types (
        http://www.iana.org/assignments/media-types/media-types.xhtml ). When
        specified, indicates the IANA Media Type (aka MIME-Type) of the object.
        The name attribute MUST include the media type and subtype
        (e.g. text/csv). The media type value is not case sensitive.
      Any required media type parameters must be provided, and
        optional parameters may be specified. There are no explicit constraints
        on the name of media-type properties or their values, however they
        SHOULD conform to media type optional and required parameters as
        specified in the respective media type RFC.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MediaType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 81, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element property uses Python identifier property_
    __property = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'property'), 'property_', '__httpns_dataone_orgservicetypesv2_0_MediaType_property', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 97, 6), )

    
    property_ = property(__property.value, __property.set, None, 'Media-type parameter(s) as specified by the\n            respective RFC for the media-type.\n          ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpns_dataone_orgservicetypesv2_0_MediaType_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 108, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 108, 4)
    
    name = property(__name.value, __name.set, None, "The value of the media-type specified as a\n          required 'name' attribute of the mediaType element.\n        ")

    _ElementMap.update({
        __property.name() : __property
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.MediaType = MediaType
Namespace.addCategoryObject('typeBinding', 'MediaType', MediaType)


# Complex type {http://ns.dataone.org/service/types/v2.0}SystemMetadata with content type ELEMENT_ONLY
class SystemMetadata (_ImportedBinding_dataoneTypes_v1.SystemMetadata):
    """System metadata in DataONE APIs version 2.0 extends
        the :class:`types.SystemMetadata` definition of version 1.x by adding
        :term:`seriesId`, :term:`mediaType`, and :term:`fileName` elements. Each
        of these are optional, so Version 1.x System Metadata is compatible with
        Version 2.x, though not vice-versa.
        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SystemMetadata')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 119, 2)
    _ElementMap = _ImportedBinding_dataoneTypes_v1.SystemMetadata._ElementMap.copy()
    _AttributeMap = _ImportedBinding_dataoneTypes_v1.SystemMetadata._AttributeMap.copy()
    # Base type is _ImportedBinding_dataoneTypes_v1.SystemMetadata
    
    # Element serialVersion (serialVersion) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element identifier (identifier) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element formatId (formatId) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element size (size) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element checksum (checksum) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element submitter (submitter) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element rightsHolder (rightsHolder) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element accessPolicy (accessPolicy) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element replicationPolicy (replicationPolicy) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element obsoletes (obsoletes) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element obsoletedBy (obsoletedBy) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element archived (archived) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element dateUploaded (dateUploaded) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element dateSysMetadataModified (dateSysMetadataModified) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element originMemberNode (originMemberNode) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element authoritativeMemberNode (authoritativeMemberNode) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element replica (replica) inherited from {http://ns.dataone.org/service/types/v1}SystemMetadata
    
    # Element seriesId uses Python identifier seriesId
    __seriesId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'seriesId'), 'seriesId', '__httpns_dataone_orgservicetypesv2_0_SystemMetadata_seriesId', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 131, 12), )

    
    seriesId = property(__seriesId.value, __seriesId.set, None, 'The :term:`seriesId` is an optional, unique\n                  Unicode string that identifies an object revision chain. A\n                  seriesId will resolve to the latest version of an object. A seriesId can not appear in any other revision chain.\n                  The values used for seriesId must be unique\n                  within DataONE and cannot be the same as the :term:`primary\n                  identifier` of an object. The same encoding rules used for identifier\n                  values apply to seriesId values.')

    
    # Element mediaType uses Python identifier mediaType
    __mediaType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mediaType'), 'mediaType', '__httpns_dataone_orgservicetypesv2_0_SystemMetadata_mediaType', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 144, 14), )

    
    mediaType = property(__mediaType.value, __mediaType.set, None, 'When specified, indicates the IANA Media\n                    Type (aka MIME-Type) of the object. When specified, this\n                    value overrides the default value specified in the version\n                    2.0 ObjectFormat structure. The value should include the\n                    media type and subtype (e.g. text/csv). The mediaType value\n                    is not case sensitive.The purpose of this value is to provide\n                      more detailed information about the specific media type\n                      of the associated object than may be available through\n                      the associated ObjectFormat.\n                    When specified, the mediaType value here\n                      overrides the value recorded in the referenced\n                      :class:`ObjectFormat`.\n                    This value SHOULD be set by the content\n                    creator. It MAY be set by any receiving agent if the value\n                    is not already set, the value in the ObjectFormat is less\n                    specific, and a correct value is specified elsewhere such\n                    as by a HTTP Content-Type parameter.\n                    This value MAY be changed to correct an\n                    erroneous entry.')

    
    # Element fileName uses Python identifier fileName
    __fileName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'fileName'), 'fileName', '__httpns_dataone_orgservicetypesv2_0_SystemMetadata_fileName', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 171, 14), )

    
    fileName = property(__fileName.value, __fileName.set, None, 'Optional though recommended value providing\n                    a suggested file name for the object. Values should\n                    conform to cross platform file naming conventions.\n                  This value SHOULD be set by the content\n                    creator.This value MAY be set by any receiving agent\n                    Changing the value is discouraged once set, unless by the\n                    authoritative Member Node of content owner.\n                  ')

    _ElementMap.update({
        __seriesId.name() : __seriesId,
        __mediaType.name() : __mediaType,
        __fileName.name() : __fileName
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SystemMetadata = SystemMetadata
Namespace.addCategoryObject('typeBinding', 'SystemMetadata', SystemMetadata)


# Complex type {http://ns.dataone.org/service/types/v2.0}NodeList with content type ELEMENT_ONLY
class NodeList (pyxb.binding.basis.complexTypeDefinition):
    """ A list of :class:`v2_0.Types.Node` entries returned by
      :func:`CNCore.listNodes()`.
      NodeList is described in :mod:`NodeList`.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NodeList')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 191, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element node uses Python identifier node
    __node = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'node'), 'node', '__httpns_dataone_orgservicetypesv2_0_NodeList_node', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 200, 6), )

    
    node = property(__node.value, __node.set, None, None)

    _ElementMap.update({
        __node.name() : __node
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.NodeList = NodeList
Namespace.addCategoryObject('typeBinding', 'NodeList', NodeList)


# Complex type {http://ns.dataone.org/service/types/v2.0}Node with content type ELEMENT_ONLY
class Node (_ImportedBinding_dataoneTypes_v1.Node):
    """Extends the Version 1.x :class:`Types.Node` by adding
        an optional unbounded parameter entry providing additional simple
        metadata relevant to a Node. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Node')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 209, 2)
    _ElementMap = _ImportedBinding_dataoneTypes_v1.Node._ElementMap.copy()
    _AttributeMap = _ImportedBinding_dataoneTypes_v1.Node._AttributeMap.copy()
    # Base type is _ImportedBinding_dataoneTypes_v1.Node
    
    # Element identifier (identifier) inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Element name (name) inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Element description (description) inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Element baseURL (baseURL) inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Element services (services) inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Element synchronization (synchronization) inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Element nodeReplicationPolicy (nodeReplicationPolicy) inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Element ping (ping) inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Element subject (subject) inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Element contactSubject (contactSubject) inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Element property uses Python identifier property_
    __property = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'property'), 'property_', '__httpns_dataone_orgservicetypesv2_0_Node_property', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 218, 10), )

    
    property_ = property(__property.value, __property.set, None, 'Allows additional attributes be added to the\n                Node document as needed.')

    
    # Attribute replicate inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Attribute synchronize inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Attribute type inherited from {http://ns.dataone.org/service/types/v1}Node
    
    # Attribute state inherited from {http://ns.dataone.org/service/types/v1}Node
    _ElementMap.update({
        __property.name() : __property
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Node = Node
Namespace.addCategoryObject('typeBinding', 'Node', Node)


# Complex type {http://ns.dataone.org/service/types/v2.0}Property with content type SIMPLE
class Property (pyxb.binding.basis.complexTypeDefinition):
    """Additional Property elements can be included to
          describe the Node in more detail. Some properties will come from
          controlled vocabularies indicated by the type attribute, while
          others will be free-form key value pairs."""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Property')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 234, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute key uses Python identifier key
    __key = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'key'), 'key', '__httpns_dataone_orgservicetypesv2_0_Property_key', pyxb.binding.datatypes.string, required=True)
    __key._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 243, 10)
    __key._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 243, 10)
    
    key = property(__key.value, __key.set, None, 'The property key for this entry. Should be\n                  unique within the Node element.')

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpns_dataone_orgservicetypesv2_0_Property_type', pyxb.binding.datatypes.string)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 249, 10)
    __type._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 249, 10)
    
    type = property(__type.value, __type.set, None, 'The optional type for the property. Can be\n                  used to indicate if a controlled vocabulary is used for the\n                  property key to better facilitate machine interpretation.\n                ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __key.name() : __key,
        __type.name() : __type
    })
_module_typeBindings.Property = Property
Namespace.addCategoryObject('typeBinding', 'Property', Property)


# Complex type {http://ns.dataone.org/service/types/v2.0}ObjectFormat with content type ELEMENT_ONLY
class ObjectFormat (_ImportedBinding_dataoneTypes_v1.ObjectFormat):
    """Extends Version 1.x :class:`Types.ObjectFormat` by
        adding :term:`mediaType` and :term:`extension` elements.
       """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ObjectFormat')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 262, 2)
    _ElementMap = _ImportedBinding_dataoneTypes_v1.ObjectFormat._ElementMap.copy()
    _AttributeMap = _ImportedBinding_dataoneTypes_v1.ObjectFormat._AttributeMap.copy()
    # Base type is _ImportedBinding_dataoneTypes_v1.ObjectFormat
    
    # Element formatId (formatId) inherited from {http://ns.dataone.org/service/types/v1}ObjectFormat
    
    # Element formatName (formatName) inherited from {http://ns.dataone.org/service/types/v1}ObjectFormat
    
    # Element formatType (formatType) inherited from {http://ns.dataone.org/service/types/v1}ObjectFormat
    
    # Element mediaType uses Python identifier mediaType
    __mediaType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mediaType'), 'mediaType', '__httpns_dataone_orgservicetypesv2_0_ObjectFormat_mediaType', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 271, 10), )

    
    mediaType = property(__mediaType.value, __mediaType.set, None, 'The IANA Media Type for this object format.\n                ')

    
    # Element extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'extension'), 'extension', '__httpns_dataone_orgservicetypesv2_0_ObjectFormat_extension', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 277, 8), )

    
    extension = property(__extension.value, __extension.set, None, 'Suggested file name extension to be used\n                  when serializing this type of object to a file. The value\n                  should not include the period (.).')

    _ElementMap.update({
        __mediaType.name() : __mediaType,
        __extension.name() : __extension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ObjectFormat = ObjectFormat
Namespace.addCategoryObject('typeBinding', 'ObjectFormat', ObjectFormat)


# Complex type {http://ns.dataone.org/service/types/v2.0}ObjectFormatList with content type ELEMENT_ONLY
class ObjectFormatList (_ImportedBinding_dataoneTypes_v1.Slice):
    """Extends :class:`Types.ObjectFormatList` to provide a
        list of :class:`v2_0.Types.ObjectFormat`.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ObjectFormatList')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 290, 2)
    _ElementMap = _ImportedBinding_dataoneTypes_v1.Slice._ElementMap.copy()
    _AttributeMap = _ImportedBinding_dataoneTypes_v1.Slice._AttributeMap.copy()
    # Base type is _ImportedBinding_dataoneTypes_v1.Slice
    
    # Element objectFormat uses Python identifier objectFormat
    __objectFormat = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'objectFormat'), 'objectFormat', '__httpns_dataone_orgservicetypesv2_0_ObjectFormatList_objectFormat', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 299, 10), )

    
    objectFormat = property(__objectFormat.value, __objectFormat.set, None, None)

    
    # Attribute count inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute start inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute total inherited from {http://ns.dataone.org/service/types/v1}Slice
    _ElementMap.update({
        __objectFormat.name() : __objectFormat
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ObjectFormatList = ObjectFormatList
Namespace.addCategoryObject('typeBinding', 'ObjectFormatList', ObjectFormatList)


# Complex type {http://ns.dataone.org/service/types/v2.0}Log with content type ELEMENT_ONLY
class Log (_ImportedBinding_dataoneTypes_v1.Slice):
    """Extends :class:`Types.Log` to represent a collection of
        :class:`v2_0.Types.LogEntry` elements, used to transfer log information
        between DataONE components."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Log')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 309, 2)
    _ElementMap = _ImportedBinding_dataoneTypes_v1.Slice._ElementMap.copy()
    _AttributeMap = _ImportedBinding_dataoneTypes_v1.Slice._AttributeMap.copy()
    # Base type is _ImportedBinding_dataoneTypes_v1.Slice
    
    # Element logEntry uses Python identifier logEntry
    __logEntry = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'logEntry'), 'logEntry', '__httpns_dataone_orgservicetypesv2_0_Log_logEntry', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 318, 10), )

    
    logEntry = property(__logEntry.value, __logEntry.set, None, None)

    
    # Attribute count inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute start inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute total inherited from {http://ns.dataone.org/service/types/v1}Slice
    _ElementMap.update({
        __logEntry.name() : __logEntry
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Log = Log
Namespace.addCategoryObject('typeBinding', 'Log', Log)


# Complex type {http://ns.dataone.org/service/types/v2.0}LogEntry with content type ELEMENT_ONLY
class LogEntry (pyxb.binding.basis.complexTypeDefinition):
    """Extends :class:`Types.LogEntry` by relaxing the value
        space for the *event* element."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LogEntry')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 326, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element entryId uses Python identifier entryId
    __entryId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'entryId'), 'entryId', '__httpns_dataone_orgservicetypesv2_0_LogEntry_entryId', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 332, 6), )

    
    entryId = property(__entryId.value, __entryId.set, None, 'A unique identifier for this log entry. The\n          identifier should be unique for a particular node; This is not drawn\n          from the same value space as other identifiers in DataONE, and so is\n          not subject to the same restrictions.')

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv2_0_LogEntry_identifier', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 341, 6), )

    
    identifier = property(__identifier.value, __identifier.set, None, 'The :term:`identifier` of the object that was the\n          target of the operation which generated this log entry.')

    
    # Element ipAddress uses Python identifier ipAddress
    __ipAddress = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ipAddress'), 'ipAddress', '__httpns_dataone_orgservicetypesv2_0_LogEntry_ipAddress', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 348, 6), )

    
    ipAddress = property(__ipAddress.value, __ipAddress.set, None, 'The IP address, as reported by the service receiving\n          the request, of the request origin.')

    
    # Element userAgent uses Python identifier userAgent
    __userAgent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'userAgent'), 'userAgent', '__httpns_dataone_orgservicetypesv2_0_LogEntry_userAgent', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 355, 6), )

    
    userAgent = property(__userAgent.value, __userAgent.set, None, 'The user agent of the client making the request, as\n          reported in the User-Agent HTTP header.')

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'subject'), 'subject', '__httpns_dataone_orgservicetypesv2_0_LogEntry_subject', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 362, 6), )

    
    subject = property(__subject.value, __subject.set, None, 'The :term:`Subject` used for making the request.\n          This may be the DataONE :term:`public` user if the request is not\n          authenticated, otherwise it will be the *subject* of the certificate\n          used for authenticating the request.')

    
    # Element event uses Python identifier event
    __event = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'event'), 'event', '__httpns_dataone_orgservicetypesv2_0_LogEntry_event', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 371, 6), )

    
    event = property(__event.value, __event.set, None, 'A non-empty string indicating the type of event\n            logged. A value from the :class:`Types.Event` enumeration is\n            recommended though no longer required for Version 2.x.\n          ')

    
    # Element dateLogged uses Python identifier dateLogged
    __dateLogged = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dateLogged'), 'dateLogged', '__httpns_dataone_orgservicetypesv2_0_LogEntry_dateLogged', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 380, 6), )

    
    dateLogged = property(__dateLogged.value, __dateLogged.set, None, 'A :class:`Types.DateTime` time stamp indicating when\n          the event triggering the log message ocurred. Note that all time\n          stamps in DataONE are in UTC.')

    
    # Element nodeIdentifier uses Python identifier nodeIdentifier
    __nodeIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'nodeIdentifier'), 'nodeIdentifier', '__httpns_dataone_orgservicetypesv2_0_LogEntry_nodeIdentifier', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 388, 6), )

    
    nodeIdentifier = property(__nodeIdentifier.value, __nodeIdentifier.set, None, 'The unique identifier for the node where the log\n          message was generated.')

    _ElementMap.update({
        __entryId.name() : __entryId,
        __identifier.name() : __identifier,
        __ipAddress.name() : __ipAddress,
        __userAgent.name() : __userAgent,
        __subject.name() : __subject,
        __event.name() : __event,
        __dateLogged.name() : __dateLogged,
        __nodeIdentifier.name() : __nodeIdentifier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.LogEntry = LogEntry
Namespace.addCategoryObject('typeBinding', 'LogEntry', LogEntry)


# Complex type {http://ns.dataone.org/service/types/v2.0}OptionList with content type ELEMENT_ONLY
class OptionList (pyxb.binding.basis.complexTypeDefinition):
    """A list of options that indicate the possible values for
        a DataONE service. Each option that can be validly sent to a service is
        listed, providing the specific key that should be used when interacting
        with the service, as well as a description of that key that allows API
        users to understand the usage of the key.  For example, an OptionList
        might contain a list of themes that can be used with the MNView.view
        service, or for other services that have a configurable but controlled
        set of parameters."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'OptionList')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 399, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element option uses Python identifier option
    __option = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'option'), 'option', '__httpns_dataone_orgservicetypesv2_0_OptionList_option', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 411, 6), )

    
    option = property(__option.value, __option.set, None, "The key to be used within an API call to a DataONE\n          service, including a description of the key and its impact on the\n          service. For example, a key 'default' can be provided as the theme for\n          the MNView.view service.  Keys must not contain characters that will\n          need to be URL escaped.")

    
    # Attribute key uses Python identifier key
    __key = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'key'), 'key', '__httpns_dataone_orgservicetypesv2_0_OptionList_key', pyxb.binding.datatypes.string, required=True)
    __key._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 424, 4)
    __key._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 424, 4)
    
    key = property(__key.value, __key.set, None, 'A value that can be used with a DataONE service. Key\n        values must not contain any characters that need to be URL escaped, and\n        should be short and informative.\n        ')

    
    # Attribute description uses Python identifier description
    __description = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'description'), 'description', '__httpns_dataone_orgservicetypesv2_0_OptionList_description', pyxb.binding.datatypes.string, required=True)
    __description._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 432, 4)
    __description._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 432, 4)
    
    description = property(__description.value, __description.set, None, 'The description of an option, indicating its intended\n          use and impact on a DataONE service invocation.')

    _ElementMap.update({
        __option.name() : __option
    })
    _AttributeMap.update({
        __key.name() : __key,
        __description.name() : __description
    })
_module_typeBindings.OptionList = OptionList
Namespace.addCategoryObject('typeBinding', 'OptionList', OptionList)


optionList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'optionList'), OptionList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 453, 2))
Namespace.addCategoryObject('elementBinding', optionList.name().localName(), optionList)

systemMetadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'systemMetadata'), SystemMetadata, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 454, 2))
Namespace.addCategoryObject('elementBinding', systemMetadata.name().localName(), systemMetadata)

property = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'property'), Property, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 455, 2))
Namespace.addCategoryObject('elementBinding', property.name().localName(), property)

node = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'node'), Node, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 456, 2))
Namespace.addCategoryObject('elementBinding', node.name().localName(), node)

nodeList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'nodeList'), NodeList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 457, 2))
Namespace.addCategoryObject('elementBinding', nodeList.name().localName(), nodeList)

objectFormat = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectFormat'), ObjectFormat, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 458, 2))
Namespace.addCategoryObject('elementBinding', objectFormat.name().localName(), objectFormat)

objectFormatList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectFormatList'), ObjectFormatList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 459, 2))
Namespace.addCategoryObject('elementBinding', objectFormatList.name().localName(), objectFormatList)

log = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'log'), Log, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 460, 2))
Namespace.addCategoryObject('elementBinding', log.name().localName(), log)

logEntry = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'logEntry'), LogEntry, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 461, 2))
Namespace.addCategoryObject('elementBinding', logEntry.name().localName(), logEntry)

mediaType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mediaType'), MediaType, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 462, 2))
Namespace.addCategoryObject('elementBinding', mediaType.name().localName(), mediaType)



MediaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'property'), MediaTypeProperty, scope=MediaType, documentation='Media-type parameter(s) as specified by the\n            respective RFC for the media-type.\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 97, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 97, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MediaType._UseForTag(pyxb.namespace.ExpandedName(None, 'property')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 97, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MediaType._Automaton = _BuildAutomaton()




SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'seriesId'), _ImportedBinding_dataoneTypes_v1.Identifier, scope=SystemMetadata, documentation='The :term:`seriesId` is an optional, unique\n                  Unicode string that identifies an object revision chain. A\n                  seriesId will resolve to the latest version of an object. A seriesId can not appear in any other revision chain.\n                  The values used for seriesId must be unique\n                  within DataONE and cannot be the same as the :term:`primary\n                  identifier` of an object. The same encoding rules used for identifier\n                  values apply to seriesId values.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 131, 12)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mediaType'), MediaType, scope=SystemMetadata, documentation='When specified, indicates the IANA Media\n                    Type (aka MIME-Type) of the object. When specified, this\n                    value overrides the default value specified in the version\n                    2.0 ObjectFormat structure. The value should include the\n                    media type and subtype (e.g. text/csv). The mediaType value\n                    is not case sensitive.The purpose of this value is to provide\n                      more detailed information about the specific media type\n                      of the associated object than may be available through\n                      the associated ObjectFormat.\n                    When specified, the mediaType value here\n                      overrides the value recorded in the referenced\n                      :class:`ObjectFormat`.\n                    This value SHOULD be set by the content\n                    creator. It MAY be set by any receiving agent if the value\n                    is not already set, the value in the ObjectFormat is less\n                    specific, and a correct value is specified elsewhere such\n                    as by a HTTP Content-Type parameter.\n                    This value MAY be changed to correct an\n                    erroneous entry.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 144, 14)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'fileName'), pyxb.binding.datatypes.string, scope=SystemMetadata, documentation='Optional though recommended value providing\n                    a suggested file name for the object. Values should\n                    conform to cross platform file naming conventions.\n                  This value SHOULD be set by the content\n                    creator.This value MAY be set by any receiving agent\n                    Changing the value is discouraged once set, unless by the\n                    authoritative Member Node of content owner.\n                  ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 171, 14)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1354, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1422, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1451, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1466, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1478, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1488, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1499, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1510, 6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1522, 6))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1533, 6))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1541, 6))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1554, 6))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 131, 12))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 144, 14))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 171, 14))
    counters.add(cc_14)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'serialVersion')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1354, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'identifier')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1366, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'formatId')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1392, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'size')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1407, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'checksum')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1413, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'submitter')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1422, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'rightsHolder')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1435, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'accessPolicy')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1451, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'replicationPolicy')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1466, 6))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'obsoletes')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1478, 6))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'obsoletedBy')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1488, 6))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'archived')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1499, 6))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'dateUploaded')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1510, 6))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'dateSysMetadataModified')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1522, 6))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'originMemberNode')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1533, 6))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'authoritativeMemberNode')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1541, 6))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'replica')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1554, 6))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'seriesId')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 131, 12))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'mediaType')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 144, 14))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, 'fileName')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 171, 14))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
         ]))
    transitions.append(fac.Transition(st_18, [
         ]))
    transitions.append(fac.Transition(st_19, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_14, True) ]))
    st_19._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SystemMetadata._Automaton = _BuildAutomaton_()




NodeList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'node'), Node, scope=NodeList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 200, 6)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(NodeList._UseForTag(pyxb.namespace.ExpandedName(None, 'node')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 200, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
NodeList._Automaton = _BuildAutomaton_2()




Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'property'), Property, scope=Node, documentation='Allows additional attributes be added to the\n                Node document as needed.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 218, 10)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 551, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 558, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 568, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 579, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 585, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 218, 10))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'identifier')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 516, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'name')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 526, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'description')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 533, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'baseURL')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 542, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'services')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 551, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'synchronization')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 558, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'nodeReplicationPolicy')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 568, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'ping')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 579, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'subject')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 585, 6))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'contactSubject')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 599, 6))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(Node._UseForTag(pyxb.namespace.ExpandedName(None, 'property')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 218, 10))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_10._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Node._Automaton = _BuildAutomaton_3()




ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mediaType'), MediaType, scope=ObjectFormat, documentation='The IANA Media Type for this object format.\n                ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 271, 10)))

ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'extension'), pyxb.binding.datatypes.string, scope=ObjectFormat, documentation='Suggested file name extension to be used\n                  when serializing this type of object to a file. The value\n                  should not include the period (.).', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 277, 8)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 271, 10))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 277, 8))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, 'formatId')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 730, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, 'formatName')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 739, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, 'formatType')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 748, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, 'mediaType')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 271, 10))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, 'extension')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 277, 8))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ObjectFormat._Automaton = _BuildAutomaton_4()




ObjectFormatList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'objectFormat'), ObjectFormat, scope=ObjectFormatList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 299, 10)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ObjectFormatList._UseForTag(pyxb.namespace.ExpandedName(None, 'objectFormat')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 299, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ObjectFormatList._Automaton = _BuildAutomaton_5()




Log._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'logEntry'), LogEntry, scope=Log, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 318, 10)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 318, 10))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Log._UseForTag(pyxb.namespace.ExpandedName(None, 'logEntry')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 318, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Log._Automaton = _BuildAutomaton_6()




LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'entryId'), _ImportedBinding_dataoneTypes_v1.NonEmptyString, scope=LogEntry, documentation='A unique identifier for this log entry. The\n          identifier should be unique for a particular node; This is not drawn\n          from the same value space as other identifiers in DataONE, and so is\n          not subject to the same restrictions.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 332, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'identifier'), _ImportedBinding_dataoneTypes_v1.Identifier, scope=LogEntry, documentation='The :term:`identifier` of the object that was the\n          target of the operation which generated this log entry.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 341, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ipAddress'), pyxb.binding.datatypes.string, scope=LogEntry, documentation='The IP address, as reported by the service receiving\n          the request, of the request origin.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 348, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'userAgent'), pyxb.binding.datatypes.string, scope=LogEntry, documentation='The user agent of the client making the request, as\n          reported in the User-Agent HTTP header.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 355, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'subject'), _ImportedBinding_dataoneTypes_v1.Subject, scope=LogEntry, documentation='The :term:`Subject` used for making the request.\n          This may be the DataONE :term:`public` user if the request is not\n          authenticated, otherwise it will be the *subject* of the certificate\n          used for authenticating the request.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 362, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'event'), _ImportedBinding_dataoneTypes_v1.NonEmptyString, scope=LogEntry, documentation='A non-empty string indicating the type of event\n            logged. A value from the :class:`Types.Event` enumeration is\n            recommended though no longer required for Version 2.x.\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 371, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dateLogged'), pyxb.binding.datatypes.dateTime, scope=LogEntry, documentation='A :class:`Types.DateTime` time stamp indicating when\n          the event triggering the log message ocurred. Note that all time\n          stamps in DataONE are in UTC.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 380, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'nodeIdentifier'), _ImportedBinding_dataoneTypes_v1.NodeReference, scope=LogEntry, documentation='The unique identifier for the node where the log\n          message was generated.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 388, 6)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'entryId')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 332, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'identifier')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 341, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'ipAddress')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 348, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'userAgent')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 355, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'subject')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 362, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'event')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 371, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'dateLogged')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 380, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'nodeIdentifier')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 388, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
LogEntry._Automaton = _BuildAutomaton_7()




OptionList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'option'), _ImportedBinding_dataoneTypes_v1.NonEmptyString, scope=OptionList, documentation="The key to be used within an API call to a DataONE\n          service, including a description of the key and its impact on the\n          service. For example, a key 'default' can be provided as the theme for\n          the MNView.view service.  Keys must not contain characters that will\n          need to be URL escaped.", location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 411, 6)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 411, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(OptionList._UseForTag(pyxb.namespace.ExpandedName(None, 'option')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v2.0.xsd', 411, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
OptionList._Automaton = _BuildAutomaton_8()

