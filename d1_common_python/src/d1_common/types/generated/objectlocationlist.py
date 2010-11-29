# ./pyxb/objectlocationlist.py
# PyXB bindings for NamespaceModule
# NSM:b76d06d55b64bd5b8a6949ed646876856310e825
# Generated 2010-11-23 10:22:01.228753 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:2d02ce12-f726-11df-b71e-000c29f765e9')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import _common

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/ObjectLocationList/0.5', create_if_missing=True)
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


# Complex type ObjectLocation with content type ELEMENT_ONLY
class ObjectLocation (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectLocation')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element preference uses Python identifier preference
    __preference = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'preference'), 'preference', '__httpdataone_orgservicetypesObjectLocationList0_5_ObjectLocation_preference', False)

    
    preference = property(__preference.value, __preference.set, None, u'A weighting parameter that provides a hint to the caller \n\t    for the relative preference for nodes from which the content should be retrieved.\n\t  ')

    
    # Element nodeIdentifier uses Python identifier nodeIdentifier
    __nodeIdentifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), 'nodeIdentifier', '__httpdataone_orgservicetypesObjectLocationList0_5_ObjectLocation_nodeIdentifier', False)

    
    nodeIdentifier = property(__nodeIdentifier.value, __nodeIdentifier.set, None, u'Identifier of the node (the same identifier used\n\t    in the node registry for identifying the node.\n          ')

    
    # Element url uses Python identifier url
    __url = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'url'), 'url', '__httpdataone_orgservicetypesObjectLocationList0_5_ObjectLocation_url', False)

    
    url = property(__url.value, __url.set, None, u'The full (absolute) URL that can be used to\n\t    retrieve the object using the get() method of the rest interface.\n\t  ')

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'baseURL'), 'baseURL', '__httpdataone_orgservicetypesObjectLocationList0_5_ObjectLocation_baseURL', False)

    
    baseURL = property(__baseURL.value, __baseURL.set, None, u'The current base URL for services implemented on the target node.\n\t  ')


    _ElementMap = {
        __preference.name() : __preference,
        __nodeIdentifier.name() : __nodeIdentifier,
        __url.name() : __url,
        __baseURL.name() : __baseURL
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectLocation', ObjectLocation)


# Complex type ObjectLocationList with content type ELEMENT_ONLY
class ObjectLocationList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectLocationList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element objectLocation uses Python identifier objectLocation
    __objectLocation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectLocation'), 'objectLocation', '__httpdataone_orgservicetypesObjectLocationList0_5_ObjectLocationList_objectLocation', True)

    
    objectLocation = property(__objectLocation.value, __objectLocation.set, None, u'List of nodes from which the object can be\n\t    retrieved')

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypesObjectLocationList0_5_ObjectLocationList_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'The identifier of the object being resolved.\n\t  ')


    _ElementMap = {
        __objectLocation.name() : __objectLocation,
        __identifier.name() : __identifier
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectLocationList', ObjectLocationList)


objectLocationList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectLocationList'), ObjectLocationList)
Namespace.addCategoryObject('elementBinding', objectLocationList.name().localName(), objectLocationList)



ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'preference'), pyxb.binding.datatypes.integer, scope=ObjectLocation, documentation=u'A weighting parameter that provides a hint to the caller \n\t    for the relative preference for nodes from which the content should be retrieved.\n\t  '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), _common.Identifier, scope=ObjectLocation, documentation=u'Identifier of the node (the same identifier used\n\t    in the node registry for identifying the node.\n          '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'url'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation=u'The full (absolute) URL that can be used to\n\t    retrieve the object using the get() method of the rest interface.\n\t  '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation=u'The current base URL for services implemented on the target node.\n\t  '))
ObjectLocation._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'nodeIdentifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'baseURL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'url')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'preference')), min_occurs=0L, max_occurs=1L)
    )
ObjectLocation._ContentModel = pyxb.binding.content.ParticleModel(ObjectLocation._GroupModel, min_occurs=1, max_occurs=1)



ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectLocation'), ObjectLocation, scope=ObjectLocationList, documentation=u'List of nodes from which the object can be\n\t    retrieved'))

ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), _common.Identifier, scope=ObjectLocationList, documentation=u'The identifier of the object being resolved.\n\t  '))
ObjectLocationList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectLocation')), min_occurs=0L, max_occurs=None)
    )
ObjectLocationList._ContentModel = pyxb.binding.content.ParticleModel(ObjectLocationList._GroupModel, min_occurs=1, max_occurs=1)
