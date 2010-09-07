# ./statusresponselist.py
# PyXB bindings for NamespaceModule
# NSM:bd5909557543568baae22458a6754f4f3dd7bde3
# Generated 2010-08-19 09:24:06.910621 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:ce99b258-aba5-11df-a12b-000c29f765e9')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import _common

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/StatusResponseList/0.1', create_if_missing=True)
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


# Complex type StatusResponse with content type ELEMENT_ONLY
class StatusResponse (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StatusResponse')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element componentVersion uses Python identifier componentVersion
    __componentVersion = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'componentVersion'), 'componentVersion', '__httpdataone_orgservicetypesStatusResponseList0_1_StatusResponse_componentVersion', False)

    
    componentVersion = property(__componentVersion.value, __componentVersion.set, None, u'Version of component in DataONE software stack.\n          ')

    
    # Element componentName uses Python identifier componentName
    __componentName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'componentName'), 'componentName', '__httpdataone_orgservicetypesStatusResponseList0_1_StatusResponse_componentName', False)

    
    componentName = property(__componentName.value, __componentName.set, None, u'Name of component in DataONE software stack.\n          ')


    _ElementMap = {
        __componentVersion.name() : __componentVersion,
        __componentName.name() : __componentName
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'StatusResponse', StatusResponse)


# Complex type StatusResponseList with content type ELEMENT_ONLY
class StatusResponseList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StatusResponseList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element statusResponse uses Python identifier statusResponse
    __statusResponse = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'statusResponse'), 'statusResponse', '__httpdataone_orgservicetypesStatusResponseList0_1_StatusResponseList_statusResponse', True)

    
    statusResponse = property(__statusResponse.value, __statusResponse.set, None, u'List of DataONE software stack components and their\n            corresponding version numbers.\n          ')


    _ElementMap = {
        __statusResponse.name() : __statusResponse
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'StatusResponseList', StatusResponseList)


statusResponseList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'statusResponseList'), StatusResponseList)
Namespace.addCategoryObject('elementBinding', statusResponseList.name().localName(), statusResponseList)



StatusResponse._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'componentVersion'), _common.ComponentVersion, scope=StatusResponse, documentation=u'Version of component in DataONE software stack.\n          '))

StatusResponse._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'componentName'), _common.ComponentName, scope=StatusResponse, documentation=u'Name of component in DataONE software stack.\n          '))
StatusResponse._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(StatusResponse._UseForTag(pyxb.namespace.ExpandedName(None, u'componentName')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(StatusResponse._UseForTag(pyxb.namespace.ExpandedName(None, u'componentVersion')), min_occurs=1L, max_occurs=1L)
    )
StatusResponse._ContentModel = pyxb.binding.content.ParticleModel(StatusResponse._GroupModel, min_occurs=1, max_occurs=1)



StatusResponseList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'statusResponse'), StatusResponse, scope=StatusResponseList, documentation=u'List of DataONE software stack components and their\n            corresponding version numbers.\n          '))
StatusResponseList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(StatusResponseList._UseForTag(pyxb.namespace.ExpandedName(None, u'statusResponse')), min_occurs=1L, max_occurs=None)
    )
StatusResponseList._ContentModel = pyxb.binding.content.ParticleModel(StatusResponseList._GroupModel, min_occurs=1, max_occurs=1)
