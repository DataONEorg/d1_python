# ./monitor_object.py
# PyXB bindings for NamespaceModule
# NSM:3a8d5615d1fe3b625c087c8373b5e1555c9408b0
# Generated 2010-07-15 23:39:01.016391 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:6f891e08-909c-11df-a7b4-000c29f765e9')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/monitorObject/0.1', create_if_missing=True)
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


# Complex type MonitorObjectEntry with content type ELEMENT_ONLY
class MonitorObjectEntry (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MonitorObjectEntry')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element count uses Python identifier count
    __count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'count'), 'count', '__httpdataone_orgservicetypesmonitorObject0_1_MonitorObjectEntry_count', False)

    
    count = property(__count.value, __count.set, None, None)

    
    # Element date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'date'), 'date', '__httpdataone_orgservicetypesmonitorObject0_1_MonitorObjectEntry_date', False)

    
    date = property(__date.value, __date.set, None, None)


    _ElementMap = {
        __count.name() : __count,
        __date.name() : __date
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MonitorObjectEntry', MonitorObjectEntry)


# Complex type MonitorObject with content type ELEMENT_ONLY
class MonitorObject (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MonitorObject')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element monitorObjectEntry uses Python identifier monitorObjectEntry
    __monitorObjectEntry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'monitorObjectEntry'), 'monitorObjectEntry', '__httpdataone_orgservicetypesmonitorObject0_1_MonitorObject_monitorObjectEntry', True)

    
    monitorObjectEntry = property(__monitorObjectEntry.value, __monitorObjectEntry.set, None, None)


    _ElementMap = {
        __monitorObjectEntry.name() : __monitorObjectEntry
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MonitorObject', MonitorObject)


monitorObject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'monitorObject'), MonitorObject)
Namespace.addCategoryObject('elementBinding', monitorObject.name().localName(), monitorObject)



MonitorObjectEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'count'), pyxb.binding.datatypes.int, scope=MonitorObjectEntry))

MonitorObjectEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'date'), pyxb.binding.datatypes.date, scope=MonitorObjectEntry))
MonitorObjectEntry._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MonitorObjectEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'date')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(MonitorObjectEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'count')), min_occurs=1L, max_occurs=1L)
    )
MonitorObjectEntry._ContentModel = pyxb.binding.content.ParticleModel(MonitorObjectEntry._GroupModel, min_occurs=1, max_occurs=1)



MonitorObject._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'monitorObjectEntry'), MonitorObjectEntry, scope=MonitorObject))
MonitorObject._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MonitorObject._UseForTag(pyxb.namespace.ExpandedName(None, u'monitorObjectEntry')), min_occurs=1L, max_occurs=None)
    )
MonitorObject._ContentModel = pyxb.binding.content.ParticleModel(MonitorObject._GroupModel, min_occurs=1, max_occurs=1)
