# ./pyxb/nodelist.py
# PyXB bindings for NamespaceModule
# NSM:42c0d00c00834050987db7e6d3ea15787defefca
# Generated 2010-10-28 12:50:12.923059 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:3210f33c-e2c4-11df-8ffa-65839d235cf8')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import _common

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/NodeList/0.5', create_if_missing=True)
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
class NodeState (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeState')
    _Documentation = None
NodeState._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=NodeState, enum_prefix=None)
NodeState.up = NodeState._CF_enumeration.addEnumeration(unicode_value=u'up')
NodeState.down = NodeState._CF_enumeration.addEnumeration(unicode_value=u'down')
NodeState.unknown = NodeState._CF_enumeration.addEnumeration(unicode_value=u'unknown')
NodeState._InitializeFacetMap(NodeState._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'NodeState', NodeState)

# Atomic SimpleTypeDefinition
class Environment (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Environment')
    _Documentation = None
Environment._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Environment, enum_prefix=None)
Environment.dev = Environment._CF_enumeration.addEnumeration(unicode_value=u'dev')
Environment.test = Environment._CF_enumeration.addEnumeration(unicode_value=u'test')
Environment.staging = Environment._CF_enumeration.addEnumeration(unicode_value=u'staging')
Environment.prod = Environment._CF_enumeration.addEnumeration(unicode_value=u'prod')
Environment._InitializeFacetMap(Environment._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'Environment', Environment)

# Atomic SimpleTypeDefinition
class NodeType (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeType')
    _Documentation = None
NodeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=NodeType, enum_prefix=None)
NodeType.mn = NodeType._CF_enumeration.addEnumeration(unicode_value=u'mn')
NodeType.cn = NodeType._CF_enumeration.addEnumeration(unicode_value=u'cn')
NodeType.Monitor = NodeType._CF_enumeration.addEnumeration(unicode_value=u'Monitor')
NodeType._InitializeFacetMap(NodeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'NodeType', NodeType)

# Atomic SimpleTypeDefinition
class crontabEntryType (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'crontabEntryType')
    _Documentation = None
crontabEntryType._CF_pattern = pyxb.binding.facets.CF_pattern()
crontabEntryType._CF_pattern.addPattern(pattern=u'([\\*\\d]{1,2}[\\-,]?)+')
crontabEntryType._InitializeFacetMap(crontabEntryType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'crontabEntryType', crontabEntryType)

# Complex type Synchronization with content type ELEMENT_ONLY
class Synchronization (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Synchronization')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element lastCompleteHarvest uses Python identifier lastCompleteHarvest
    __lastCompleteHarvest = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), 'lastCompleteHarvest', '__httpdataone_orgservicetypesNodeList0_5_Synchronization_lastCompleteHarvest', False)

    
    lastCompleteHarvest = property(__lastCompleteHarvest.value, __lastCompleteHarvest.set, None, u'The last time all the data from a node was pulled from a member node\n           ')

    
    # Element schedule uses Python identifier schedule
    __schedule = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'schedule'), 'schedule', '__httpdataone_orgservicetypesNodeList0_5_Synchronization_schedule', False)

    
    schedule = property(__schedule.value, __schedule.set, None, None)

    
    # Element lastHarvested uses Python identifier lastHarvested
    __lastHarvested = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastHarvested'), 'lastHarvested', '__httpdataone_orgservicetypesNodeList0_5_Synchronization_lastHarvested', False)

    
    lastHarvested = property(__lastHarvested.value, __lastHarvested.set, None, u'The last time the mn sychronization daemon ran and found new data to synchronize\n           ')


    _ElementMap = {
        __lastCompleteHarvest.name() : __lastCompleteHarvest,
        __schedule.name() : __schedule,
        __lastHarvested.name() : __lastHarvested
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Synchronization', Synchronization)


# Complex type Ping with content type EMPTY
class Ping (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Ping')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute lastSuccess uses Python identifier lastSuccess
    __lastSuccess = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'lastSuccess'), 'lastSuccess', '__httpdataone_orgservicetypesNodeList0_5_Ping_lastSuccess', pyxb.binding.datatypes.dateTime)
    
    lastSuccess = property(__lastSuccess.value, __lastSuccess.set, None, None)

    
    # Attribute success uses Python identifier success
    __success = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'success'), 'success', '__httpdataone_orgservicetypesNodeList0_5_Ping_success', pyxb.binding.datatypes.boolean)
    
    success = property(__success.value, __success.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __lastSuccess.name() : __lastSuccess,
        __success.name() : __success
    }
Namespace.addCategoryObject('typeBinding', u'Ping', Ping)


# Complex type Status with content type EMPTY
class Status (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Status')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute dateChecked uses Python identifier dateChecked
    __dateChecked = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dateChecked'), 'dateChecked', '__httpdataone_orgservicetypesNodeList0_5_Status_dateChecked', pyxb.binding.datatypes.dateTime, required=True)
    
    dateChecked = property(__dateChecked.value, __dateChecked.set, None, None)

    
    # Attribute success uses Python identifier success
    __success = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'success'), 'success', '__httpdataone_orgservicetypesNodeList0_5_Status_success', pyxb.binding.datatypes.boolean)
    
    success = property(__success.value, __success.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __dateChecked.name() : __dateChecked,
        __success.name() : __success
    }
Namespace.addCategoryObject('typeBinding', u'Status', Status)


# Complex type Service with content type ELEMENT_ONLY
class Service (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Service')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element method uses Python identifier method
    __method = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'method'), 'method', '__httpdataone_orgservicetypesNodeList0_5_Service_method', True)

    
    method = property(__method.value, __method.set, None, None)

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpdataone_orgservicetypesNodeList0_5_Service_name', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute available uses Python identifier available
    __available = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'available'), 'available', '__httpdataone_orgservicetypesNodeList0_5_Service_available', pyxb.binding.datatypes.boolean)
    
    available = property(__available.value, __available.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpdataone_orgservicetypesNodeList0_5_Service_version', _common.ServiceVersion, required=True)
    
    version = property(__version.value, __version.set, None, None)


    _ElementMap = {
        __method.name() : __method,
        __name.name() : __name
    }
    _AttributeMap = {
        __available.name() : __available,
        __version.name() : __version
    }
Namespace.addCategoryObject('typeBinding', u'Service', Service)


# Complex type NodeHealth with content type ELEMENT_ONLY
class NodeHealth (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeHealth')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element status uses Python identifier status
    __status = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'status'), 'status', '__httpdataone_orgservicetypesNodeList0_5_NodeHealth_status', False)

    
    status = property(__status.value, __status.set, None, None)

    
    # Element ping uses Python identifier ping
    __ping = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ping'), 'ping', '__httpdataone_orgservicetypesNodeList0_5_NodeHealth_ping', False)

    
    ping = property(__ping.value, __ping.set, None, None)

    
    # Attribute state uses Python identifier state
    __state = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'state'), 'state', '__httpdataone_orgservicetypesNodeList0_5_NodeHealth_state', NodeState, required=True)
    
    state = property(__state.value, __state.set, None, None)


    _ElementMap = {
        __status.name() : __status,
        __ping.name() : __ping
    }
    _AttributeMap = {
        __state.name() : __state
    }
Namespace.addCategoryObject('typeBinding', u'NodeHealth', NodeHealth)


# Complex type Node with content type ELEMENT_ONLY
class Node (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Node')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element services uses Python identifier services
    __services = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'services'), 'services', '__httpdataone_orgservicetypesNodeList0_5_Node_services', False)

    
    services = property(__services.value, __services.set, None, None)

    
    # Element synchronization uses Python identifier synchronization
    __synchronization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'synchronization'), 'synchronization', '__httpdataone_orgservicetypesNodeList0_5_Node_synchronization', False)

    
    synchronization = property(__synchronization.value, __synchronization.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypesNodeList0_5_Node_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'A unique identifier for the node. This may initially be the same as the\n            baseURL, however this value should not change for future implementations of the same\n            node, whereas the baseURL may change in the future. \n            ')

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpdataone_orgservicetypesNodeList0_5_Node_name', False)

    
    name = property(__name.value, __name.set, None, u'A human readable name of the Node. \n            The name of the node is being used in Mercury currently to assign a path,\n            so format should be consistent with dataone directory naming conventions\n          ')

    
    # Element health uses Python identifier health
    __health = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'health'), 'health', '__httpdataone_orgservicetypesNodeList0_5_Node_health', False)

    
    health = property(__health.value, __health.set, None, u'The name of the node is being used in Mercury currently to assign a\n            path, so format should be consistent with dataone directory naming conventions\n          ')

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__httpdataone_orgservicetypesNodeList0_5_Node_description', False)

    
    description = property(__description.value, __description.set, None, u'Description of content maintained by this node and any other free style\n            notes. May be we should allow CDATA element with the purpose of using for display\n          ')

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'baseURL'), 'baseURL', '__httpdataone_orgservicetypesNodeList0_5_Node_baseURL', False)

    
    baseURL = property(__baseURL.value, __baseURL.set, None, None)

    
    # Attribute environment uses Python identifier environment
    __environment = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'environment'), 'environment', '__httpdataone_orgservicetypesNodeList0_5_Node_environment', Environment)
    
    environment = property(__environment.value, __environment.set, None, None)

    
    # Attribute synchronize uses Python identifier synchronize
    __synchronize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'synchronize'), 'synchronize', '__httpdataone_orgservicetypesNodeList0_5_Node_synchronize', pyxb.binding.datatypes.boolean, required=True)
    
    synchronize = property(__synchronize.value, __synchronize.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'type'), 'type', '__httpdataone_orgservicetypesNodeList0_5_Node_type', NodeType, required=True)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute replicate uses Python identifier replicate
    __replicate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'replicate'), 'replicate', '__httpdataone_orgservicetypesNodeList0_5_Node_replicate', pyxb.binding.datatypes.boolean, required=True)
    
    replicate = property(__replicate.value, __replicate.set, None, None)


    _ElementMap = {
        __services.name() : __services,
        __synchronization.name() : __synchronization,
        __identifier.name() : __identifier,
        __name.name() : __name,
        __health.name() : __health,
        __description.name() : __description,
        __baseURL.name() : __baseURL
    }
    _AttributeMap = {
        __environment.name() : __environment,
        __synchronize.name() : __synchronize,
        __type.name() : __type,
        __replicate.name() : __replicate
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
    __service = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpdataone_orgservicetypesNodeList0_5_Services_service', True)

    
    service = property(__service.value, __service.set, None, None)


    _ElementMap = {
        __service.name() : __service
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Services', Services)


# Complex type Schedule with content type EMPTY
class Schedule (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Schedule')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute hour uses Python identifier hour
    __hour = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'hour'), 'hour', '__httpdataone_orgservicetypesNodeList0_5_Schedule_hour', crontabEntryType, required=True)
    
    hour = property(__hour.value, __hour.set, None, None)

    
    # Attribute min uses Python identifier min
    __min = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'min'), 'min', '__httpdataone_orgservicetypesNodeList0_5_Schedule_min', crontabEntryType, required=True)
    
    min = property(__min.value, __min.set, None, None)

    
    # Attribute mon uses Python identifier mon
    __mon = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mon'), 'mon', '__httpdataone_orgservicetypesNodeList0_5_Schedule_mon', crontabEntryType, required=True)
    
    mon = property(__mon.value, __mon.set, None, None)

    
    # Attribute mday uses Python identifier mday
    __mday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mday'), 'mday', '__httpdataone_orgservicetypesNodeList0_5_Schedule_mday', crontabEntryType, required=True)
    
    mday = property(__mday.value, __mday.set, None, None)

    
    # Attribute sec uses Python identifier sec
    __sec = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'sec'), 'sec', '__httpdataone_orgservicetypesNodeList0_5_Schedule_sec', crontabEntryType, required=True)
    
    sec = property(__sec.value, __sec.set, None, None)

    
    # Attribute wday uses Python identifier wday
    __wday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'wday'), 'wday', '__httpdataone_orgservicetypesNodeList0_5_Schedule_wday', crontabEntryType, required=True)
    
    wday = property(__wday.value, __wday.set, None, None)

    
    # Attribute year uses Python identifier year
    __year = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'year'), 'year', '__httpdataone_orgservicetypesNodeList0_5_Schedule_year', crontabEntryType, required=True)
    
    year = property(__year.value, __year.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __hour.name() : __hour,
        __min.name() : __min,
        __mon.name() : __mon,
        __mday.name() : __mday,
        __sec.name() : __sec,
        __wday.name() : __wday,
        __year.name() : __year
    }
Namespace.addCategoryObject('typeBinding', u'Schedule', Schedule)


# Complex type NodeList with content type ELEMENT_ONLY
class NodeList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element node uses Python identifier node
    __node = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'node'), 'node', '__httpdataone_orgservicetypesNodeList0_5_NodeList_node', True)

    
    node = property(__node.value, __node.set, None, None)


    _ElementMap = {
        __node.name() : __node
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'NodeList', NodeList)


# Complex type ServiceMethod with content type EMPTY
class ServiceMethod (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceMethod')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute implemented uses Python identifier implemented
    __implemented = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'implemented'), 'implemented', '__httpdataone_orgservicetypesNodeList0_5_ServiceMethod_implemented', pyxb.binding.datatypes.boolean, required=True)
    
    implemented = property(__implemented.value, __implemented.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpdataone_orgservicetypesNodeList0_5_ServiceMethod_name', pyxb.binding.datatypes.NMTOKEN)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute rest uses Python identifier rest
    __rest = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'rest'), 'rest', '__httpdataone_orgservicetypesNodeList0_5_ServiceMethod_rest', pyxb.binding.datatypes.token, required=True)
    
    rest = property(__rest.value, __rest.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __implemented.name() : __implemented,
        __name.name() : __name,
        __rest.name() : __rest
    }
Namespace.addCategoryObject('typeBinding', u'ServiceMethod', ServiceMethod)


nodeList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'nodeList'), NodeList)
Namespace.addCategoryObject('elementBinding', nodeList.name().localName(), nodeList)



Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation=u'The last time all the data from a node was pulled from a member node\n           '))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'schedule'), Schedule, scope=Synchronization))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastHarvested'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation=u'The last time the mn sychronization daemon ran and found new data to synchronize\n           '))
Synchronization._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'schedule')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastHarvested')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest')), min_occurs=1, max_occurs=1)
    )
Synchronization._ContentModel = pyxb.binding.content.ParticleModel(Synchronization._GroupModel, min_occurs=1, max_occurs=1)



Service._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'method'), ServiceMethod, scope=Service))

Service._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), _common.ServiceName, scope=Service))
Service._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Service._UseForTag(pyxb.namespace.ExpandedName(None, u'name')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Service._UseForTag(pyxb.namespace.ExpandedName(None, u'method')), min_occurs=0L, max_occurs=None)
    )
Service._ContentModel = pyxb.binding.content.ParticleModel(Service._GroupModel, min_occurs=1, max_occurs=1)



NodeHealth._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'status'), Status, scope=NodeHealth))

NodeHealth._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ping'), Ping, scope=NodeHealth))
NodeHealth._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NodeHealth._UseForTag(pyxb.namespace.ExpandedName(None, u'ping')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(NodeHealth._UseForTag(pyxb.namespace.ExpandedName(None, u'status')), min_occurs=1, max_occurs=1)
    )
NodeHealth._ContentModel = pyxb.binding.content.ParticleModel(NodeHealth._GroupModel, min_occurs=1, max_occurs=1)



Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'services'), Services, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'synchronization'), Synchronization, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), _common.NodeReference, scope=Node, documentation=u'A unique identifier for the node. This may initially be the same as the\n            baseURL, however this value should not change for future implementations of the same\n            node, whereas the baseURL may change in the future. \n            '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), _common.NonEmptyString, scope=Node, documentation=u'A human readable name of the Node. \n            The name of the node is being used in Mercury currently to assign a path,\n            so format should be consistent with dataone directory naming conventions\n          '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'health'), NodeHealth, scope=Node, documentation=u'The name of the node is being used in Mercury currently to assign a\n            path, so format should be consistent with dataone directory naming conventions\n          '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'description'), _common.NonEmptyString, scope=Node, documentation=u'Description of content maintained by this node and any other free style\n            notes. May be we should allow CDATA element with the purpose of using for display\n          '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=Node))
Node._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'name')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'description')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'baseURL')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'services')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'synchronization')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'health')), min_occurs=0L, max_occurs=1L)
    )
Node._ContentModel = pyxb.binding.content.ParticleModel(Node._GroupModel, min_occurs=1, max_occurs=1)



Services._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'service'), Service, scope=Services))
Services._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Services._UseForTag(pyxb.namespace.ExpandedName(None, u'service')), min_occurs=1L, max_occurs=None)
    )
Services._ContentModel = pyxb.binding.content.ParticleModel(Services._GroupModel, min_occurs=1, max_occurs=1)



NodeList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'node'), Node, scope=NodeList))
NodeList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NodeList._UseForTag(pyxb.namespace.ExpandedName(None, u'node')), min_occurs=1L, max_occurs=None)
    )
NodeList._ContentModel = pyxb.binding.content.ParticleModel(NodeList._GroupModel, min_occurs=1, max_occurs=1)
