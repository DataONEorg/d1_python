# ./pyxb/monitorlist.py
# PyXB bindings for NamespaceModule
# NSM:46147b3f04a029aa87d8aa4652c0e6f458cc89c8
# Generated 2010-11-23 10:22:01.227920 by PyXB version 1.1.2
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

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/monitorObject/0.5', create_if_missing=True)
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


# Complex type MonitorList with content type ELEMENT_ONLY
class MonitorList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MonitorList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element monitorInfo uses Python identifier monitorInfo
    __monitorInfo = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'monitorInfo'), 'monitorInfo', '__httpdataone_orgservicetypesmonitorObject0_5_MonitorList_monitorInfo', True)

    
    monitorInfo = property(__monitorInfo.value, __monitorInfo.set, None, None)


    _ElementMap = {
        __monitorInfo.name() : __monitorInfo
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MonitorList', MonitorList)


# Complex type MonitorInfo with content type ELEMENT_ONLY
class MonitorInfo (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MonitorInfo')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element count uses Python identifier count
    __count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'count'), 'count', '__httpdataone_orgservicetypesmonitorObject0_5_MonitorInfo_count', False)

    
    count = property(__count.value, __count.set, None, None)

    
    # Element date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'date'), 'date', '__httpdataone_orgservicetypesmonitorObject0_5_MonitorInfo_date', False)

    
    date = property(__date.value, __date.set, None, None)


    _ElementMap = {
        __count.name() : __count,
        __date.name() : __date
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MonitorInfo', MonitorInfo)


monitorList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'monitorList'), MonitorList)
Namespace.addCategoryObject('elementBinding', monitorList.name().localName(), monitorList)



MonitorList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'monitorInfo'), MonitorInfo, scope=MonitorList))
MonitorList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MonitorList._UseForTag(pyxb.namespace.ExpandedName(None, u'monitorInfo')), min_occurs=0L, max_occurs=None)
    )
MonitorList._ContentModel = pyxb.binding.content.ParticleModel(MonitorList._GroupModel, min_occurs=1, max_occurs=1)



MonitorInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'count'), pyxb.binding.datatypes.int, scope=MonitorInfo))

MonitorInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'date'), pyxb.binding.datatypes.date, scope=MonitorInfo))
MonitorInfo._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MonitorInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'date')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(MonitorInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'count')), min_occurs=1L, max_occurs=1L)
    )
MonitorInfo._ContentModel = pyxb.binding.content.ParticleModel(MonitorInfo._GroupModel, min_occurs=1, max_occurs=1)
