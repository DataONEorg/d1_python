# d1common/types/noderegistry.py
# PyXB bindings for NamespaceModule
# NSM:86e332546bb2ba0a4fc7a322cd2a1514b059fd99
# Generated 2010-06-29 11:08:16.908949 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:23603098-8390-11df-9bc3-00264a005868')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import _common

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/NodeRegistry/0.1', create_if_missing=True)
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


# Atomic SimpleTypeDefinition
class crontabEntryType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'crontabEntryType')
    _Documentation = None
crontabEntryType._CF_pattern = pyxb.binding.facets.CF_pattern()
crontabEntryType._CF_pattern.addPattern(pattern=u'([\\*\\d]{1,2}[\\-,]?)+')
crontabEntryType._InitializeFacetMap(crontabEntryType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'crontabEntryType', crontabEntryType)

# Complex type Node with content type ELEMENT_ONLY
class Node (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Node')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element synchronization uses Python identifier synchronization
    __synchronization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'synchronization'), 'synchronization', '__httpdataone_orgservicetypesNodeRegistry0_1_Node_synchronization', False)

    
    synchronization = property(__synchronization.value, __synchronization.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypesNodeRegistry0_1_Node_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpdataone_orgservicetypesNodeRegistry0_1_Node_name', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'baseURL'), 'baseURL', '__httpdataone_orgservicetypesNodeRegistry0_1_Node_baseURL', False)

    
    baseURL = property(__baseURL.value, __baseURL.set, None, None)

    
    # Element services uses Python identifier services
    __services = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'services'), 'services', '__httpdataone_orgservicetypesNodeRegistry0_1_Node_services', False)

    
    services = property(__services.value, __services.set, None, None)

    
    # Attribute synchronize uses Python identifier synchronize
    __synchronize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'synchronize'), 'synchronize', '__httpdataone_orgservicetypesNodeRegistry0_1_Node_synchronize', pyxb.binding.datatypes.boolean, required=True)
    
    synchronize = property(__synchronize.value, __synchronize.set, None, None)

    
    # Attribute replicate uses Python identifier replicate
    __replicate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'replicate'), 'replicate', '__httpdataone_orgservicetypesNodeRegistry0_1_Node_replicate', pyxb.binding.datatypes.boolean, required=True)
    
    replicate = property(__replicate.value, __replicate.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'type'), 'type', '__httpdataone_orgservicetypesNodeRegistry0_1_Node_type', pyxb.binding.datatypes.NCName, required=True)
    
    type = property(__type.value, __type.set, None, None)


    _ElementMap = {
        __synchronization.name() : __synchronization,
        __identifier.name() : __identifier,
        __name.name() : __name,
        __baseURL.name() : __baseURL,
        __services.name() : __services
    }
    _AttributeMap = {
        __synchronize.name() : __synchronize,
        __replicate.name() : __replicate,
        __type.name() : __type
    }
Namespace.addCategoryObject('typeBinding', u'Node', Node)


# Complex type Services with content type ELEMENT_ONLY
class Services (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Services')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element service uses Python identifier service
    __service = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpdataone_orgservicetypesNodeRegistry0_1_Services_service', True)

    
    service = property(__service.value, __service.set, None, None)


    _ElementMap = {
        __service.name() : __service
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Services', Services)


# Complex type Synchronization with content type ELEMENT_ONLY
class Synchronization (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Synchronization')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element lastCompleteHarvest uses Python identifier lastCompleteHarvest
    __lastCompleteHarvest = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), 'lastCompleteHarvest', '__httpdataone_orgservicetypesNodeRegistry0_1_Synchronization_lastCompleteHarvest', False)

    
    lastCompleteHarvest = property(__lastCompleteHarvest.value, __lastCompleteHarvest.set, None, None)

    
    # Element schedule uses Python identifier schedule
    __schedule = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'schedule'), 'schedule', '__httpdataone_orgservicetypesNodeRegistry0_1_Synchronization_schedule', False)

    
    schedule = property(__schedule.value, __schedule.set, None, None)

    
    # Element lastHarvested uses Python identifier lastHarvested
    __lastHarvested = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastHarvested'), 'lastHarvested', '__httpdataone_orgservicetypesNodeRegistry0_1_Synchronization_lastHarvested', False)

    
    lastHarvested = property(__lastHarvested.value, __lastHarvested.set, None, None)


    _ElementMap = {
        __lastCompleteHarvest.name() : __lastCompleteHarvest,
        __schedule.name() : __schedule,
        __lastHarvested.name() : __lastHarvested
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Synchronization', Synchronization)


# Complex type Service with content type EMPTY
class Service (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Service')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute available uses Python identifier available
    __available = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'available'), 'available', '__httpdataone_orgservicetypesNodeRegistry0_1_Service_available', pyxb.binding.datatypes.boolean, required=True)
    
    available = property(__available.value, __available.set, None, None)

    
    # Attribute api uses Python identifier api
    __api = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'api'), 'api', '__httpdataone_orgservicetypesNodeRegistry0_1_Service_api', pyxb.binding.datatypes.NCName, required=True)
    
    api = property(__api.value, __api.set, None, None)

    
    # Attribute method uses Python identifier method
    __method = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'method'), 'method', '__httpdataone_orgservicetypesNodeRegistry0_1_Service_method', pyxb.binding.datatypes.NCName, required=True)
    
    method = property(__method.value, __method.set, None, None)

    
    # Attribute datechecked uses Python identifier datechecked
    __datechecked = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'datechecked'), 'datechecked', '__httpdataone_orgservicetypesNodeRegistry0_1_Service_datechecked', pyxb.binding.datatypes.dateTime, required=True)
    
    datechecked = property(__datechecked.value, __datechecked.set, None, None)

    
    # Attribute rest uses Python identifier rest
    __rest = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'rest'), 'rest', '__httpdataone_orgservicetypesNodeRegistry0_1_Service_rest', pyxb.binding.datatypes.string, required=True)
    
    rest = property(__rest.value, __rest.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __available.name() : __available,
        __api.name() : __api,
        __method.name() : __method,
        __datechecked.name() : __datechecked,
        __rest.name() : __rest
    }
Namespace.addCategoryObject('typeBinding', u'Service', Service)


# Complex type Schedule with content type EMPTY
class Schedule (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Schedule')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute hour uses Python identifier hour
    __hour = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'hour'), 'hour', '__httpdataone_orgservicetypesNodeRegistry0_1_Schedule_hour', crontabEntryType, required=True)
    
    hour = property(__hour.value, __hour.set, None, None)

    
    # Attribute mon uses Python identifier mon
    __mon = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mon'), 'mon', '__httpdataone_orgservicetypesNodeRegistry0_1_Schedule_mon', crontabEntryType, required=True)
    
    mon = property(__mon.value, __mon.set, None, None)

    
    # Attribute sec uses Python identifier sec
    __sec = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'sec'), 'sec', '__httpdataone_orgservicetypesNodeRegistry0_1_Schedule_sec', crontabEntryType, required=True)
    
    sec = property(__sec.value, __sec.set, None, None)

    
    # Attribute wday uses Python identifier wday
    __wday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'wday'), 'wday', '__httpdataone_orgservicetypesNodeRegistry0_1_Schedule_wday', crontabEntryType, required=True)
    
    wday = property(__wday.value, __wday.set, None, None)

    
    # Attribute year uses Python identifier year
    __year = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'year'), 'year', '__httpdataone_orgservicetypesNodeRegistry0_1_Schedule_year', crontabEntryType, required=True)
    
    year = property(__year.value, __year.set, None, None)

    
    # Attribute mday uses Python identifier mday
    __mday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mday'), 'mday', '__httpdataone_orgservicetypesNodeRegistry0_1_Schedule_mday', crontabEntryType, required=True)
    
    mday = property(__mday.value, __mday.set, None, None)

    
    # Attribute min uses Python identifier min
    __min = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'min'), 'min', '__httpdataone_orgservicetypesNodeRegistry0_1_Schedule_min', crontabEntryType, required=True)
    
    min = property(__min.value, __min.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __hour.name() : __hour,
        __mon.name() : __mon,
        __sec.name() : __sec,
        __wday.name() : __wday,
        __year.name() : __year,
        __mday.name() : __mday,
        __min.name() : __min
    }
Namespace.addCategoryObject('typeBinding', u'Schedule', Schedule)


# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element node uses Python identifier node
    __node = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'node'), 'node', '__httpdataone_orgservicetypesNodeRegistry0_1_CTD_ANON_node', True)

    
    node = property(__node.value, __node.set, None, None)


    _ElementMap = {
        __node.name() : __node
    }
    _AttributeMap = {
        
    }



nodeRegistry = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'nodeRegistry'), CTD_ANON)
Namespace.addCategoryObject('elementBinding', nodeRegistry.name().localName(), nodeRegistry)



Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'synchronization'), Synchronization, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), _common.Identifier, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), _common.NodeReference, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'services'), Services, scope=Node))
Node._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'name')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'baseURL')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'services')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'synchronization')), min_occurs=0L, max_occurs=1L)
    )
Node._ContentModel = pyxb.binding.content.ParticleModel(Node._GroupModel, min_occurs=1, max_occurs=1)



Services._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'service'), Service, scope=Services))
Services._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Services._UseForTag(pyxb.namespace.ExpandedName(None, u'service')), min_occurs=1L, max_occurs=None)
    )
Services._ContentModel = pyxb.binding.content.ParticleModel(Services._GroupModel, min_occurs=1, max_occurs=1)



Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), pyxb.binding.datatypes.dateTime, scope=Synchronization))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'schedule'), Schedule, scope=Synchronization))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastHarvested'), pyxb.binding.datatypes.dateTime, scope=Synchronization))
Synchronization._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'schedule')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastHarvested')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest')), min_occurs=1, max_occurs=1)
    )
Synchronization._ContentModel = pyxb.binding.content.ParticleModel(Synchronization._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'node'), Node, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'node')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)
