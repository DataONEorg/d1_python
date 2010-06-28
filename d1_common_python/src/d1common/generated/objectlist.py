# d1generated/objectlist.py
# PyXB bindings for NamespaceModule
# NSM:96ccb5882fb936073345ea8144478ca840b9133c
# Generated 2010-06-28 16:44:35.586339 by PyXB version 1.1.1
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:f47b93de-82f5-11df-8800-00264a005868')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import _common

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/ObjectList/0.1', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a Python instance."""
    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace.fallbackNamespace(), location_base=location_base)
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
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, _fallback_namespace=default_namespace)


# Complex type ObjectList with content type ELEMENT_ONLY
class ObjectList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element objectInfo uses Python identifier objectInfo
    __objectInfo = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectInfo'), 'objectInfo', '__httpdataone_orgservicetypesObjectList0_1_ObjectList_objectInfo', True)

    
    objectInfo = property(__objectInfo.value, __objectInfo.set, None, None)

    
    # Attribute count uses Python identifier count
    __count = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'count'), 'count', '__httpdataone_orgservicetypesObjectList0_1_ObjectList_count', pyxb.binding.datatypes.int, required=True)
    
    count = property(__count.value, __count.set, None, None)

    
    # Attribute start uses Python identifier start
    __start = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'start'), 'start', '__httpdataone_orgservicetypesObjectList0_1_ObjectList_start', pyxb.binding.datatypes.int, required=True)
    
    start = property(__start.value, __start.set, None, None)

    
    # Attribute total uses Python identifier total
    __total = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'total'), 'total', '__httpdataone_orgservicetypesObjectList0_1_ObjectList_total', pyxb.binding.datatypes.int, required=True)
    
    total = property(__total.value, __total.set, None, None)


    _ElementMap = {
        __objectInfo.name() : __objectInfo
    }
    _AttributeMap = {
        __count.name() : __count,
        __start.name() : __start,
        __total.name() : __total
    }
Namespace.addCategoryObject('typeBinding', u'ObjectList', ObjectList)


# Complex type ObjectInfo with content type ELEMENT_ONLY
class ObjectInfo (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectInfo')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element size uses Python identifier size
    __size = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'size'), 'size', '__httpdataone_orgservicetypesObjectList0_1_ObjectInfo_size', False)

    
    size = property(__size.value, __size.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypesObjectList0_1_ObjectInfo_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__httpdataone_orgservicetypesObjectList0_1_ObjectInfo_checksum', False)

    
    checksum = property(__checksum.value, __checksum.set, None, None)

    
    # Element objectFormat uses Python identifier objectFormat
    __objectFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectFormat'), 'objectFormat', '__httpdataone_orgservicetypesObjectList0_1_ObjectInfo_objectFormat', False)

    
    objectFormat = property(__objectFormat.value, __objectFormat.set, None, None)

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpdataone_orgservicetypesObjectList0_1_ObjectInfo_dateSysMetadataModified', False)

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, None)


    _ElementMap = {
        __size.name() : __size,
        __identifier.name() : __identifier,
        __checksum.name() : __checksum,
        __objectFormat.name() : __objectFormat,
        __dateSysMetadataModified.name() : __dateSysMetadataModified
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectInfo', ObjectInfo)


objectList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectList'), ObjectList)
Namespace.addCategoryObject('elementBinding', objectList.name().localName(), objectList)



ObjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectInfo'), ObjectInfo, scope=ObjectList))
ObjectList._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=ObjectList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectInfo'))),
    ])
})



ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'size'), pyxb.binding.datatypes.long, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), _common.Identifier, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'checksum'), _common.Checksum, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectFormat'), _common.ObjectFormat, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=ObjectInfo))
ObjectInfo._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'objectFormat'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'checksum'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'size'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
    ])
})
