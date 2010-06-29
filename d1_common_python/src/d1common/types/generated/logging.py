# d1common/types/logging.py
# PyXB bindings for NamespaceModule
# NSM:4c0b254ff7a24921cacdb99b4dab6f73821e5ad7
# Generated 2010-06-29 11:08:16.908753 by PyXB version 1.1.2
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

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/logging/0.1', create_if_missing=True)
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
class Event (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Event')
    _Documentation = None
Event._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Event, enum_prefix=None)
Event.create = Event._CF_enumeration.addEnumeration(unicode_value=u'create')
Event.read = Event._CF_enumeration.addEnumeration(unicode_value=u'read')
Event.update = Event._CF_enumeration.addEnumeration(unicode_value=u'update')
Event.delete = Event._CF_enumeration.addEnumeration(unicode_value=u'delete')
Event.replicate = Event._CF_enumeration.addEnumeration(unicode_value=u'replicate')
Event._InitializeFacetMap(Event._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'Event', Event)

# Complex type LogEntry with content type ELEMENT_ONLY
class LogEntry (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LogEntry')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element entryId uses Python identifier entryId
    __entryId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'entryId'), 'entryId', '__httpdataone_orgservicetypeslogging0_1_LogEntry_entryId', False)

    
    entryId = property(__entryId.value, __entryId.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypeslogging0_1_LogEntry_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element ipAddress uses Python identifier ipAddress
    __ipAddress = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ipAddress'), 'ipAddress', '__httpdataone_orgservicetypeslogging0_1_LogEntry_ipAddress', False)

    
    ipAddress = property(__ipAddress.value, __ipAddress.set, None, None)

    
    # Element memberNode uses Python identifier memberNode
    __memberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'memberNode'), 'memberNode', '__httpdataone_orgservicetypeslogging0_1_LogEntry_memberNode', False)

    
    memberNode = property(__memberNode.value, __memberNode.set, None, None)

    
    # Element userAgent uses Python identifier userAgent
    __userAgent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'userAgent'), 'userAgent', '__httpdataone_orgservicetypeslogging0_1_LogEntry_userAgent', False)

    
    userAgent = property(__userAgent.value, __userAgent.set, None, None)

    
    # Element principal uses Python identifier principal
    __principal = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'principal'), 'principal', '__httpdataone_orgservicetypeslogging0_1_LogEntry_principal', False)

    
    principal = property(__principal.value, __principal.set, None, None)

    
    # Element event uses Python identifier event
    __event = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'event'), 'event', '__httpdataone_orgservicetypeslogging0_1_LogEntry_event', False)

    
    event = property(__event.value, __event.set, None, None)

    
    # Element dateLogged uses Python identifier dateLogged
    __dateLogged = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateLogged'), 'dateLogged', '__httpdataone_orgservicetypeslogging0_1_LogEntry_dateLogged', False)

    
    dateLogged = property(__dateLogged.value, __dateLogged.set, None, None)


    _ElementMap = {
        __entryId.name() : __entryId,
        __identifier.name() : __identifier,
        __ipAddress.name() : __ipAddress,
        __memberNode.name() : __memberNode,
        __userAgent.name() : __userAgent,
        __principal.name() : __principal,
        __event.name() : __event,
        __dateLogged.name() : __dateLogged
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LogEntry', LogEntry)


# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element logEntry uses Python identifier logEntry
    __logEntry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'logEntry'), 'logEntry', '__httpdataone_orgservicetypeslogging0_1_CTD_ANON_logEntry', True)

    
    logEntry = property(__logEntry.value, __logEntry.set, None, None)


    _ElementMap = {
        __logEntry.name() : __logEntry
    }
    _AttributeMap = {
        
    }



log = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'log'), CTD_ANON)
Namespace.addCategoryObject('elementBinding', log.name().localName(), log)



LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'entryId'), _common.Identifier, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), _common.Identifier, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ipAddress'), pyxb.binding.datatypes.string, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'memberNode'), _common.NodeReference, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'userAgent'), pyxb.binding.datatypes.string, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'principal'), _common.Principal, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'event'), Event, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateLogged'), pyxb.binding.datatypes.dateTime, scope=LogEntry))
LogEntry._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'entryId')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'ipAddress')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'userAgent')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'principal')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'event')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'dateLogged')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'memberNode')), min_occurs=1L, max_occurs=1L)
    )
LogEntry._ContentModel = pyxb.binding.content.ParticleModel(LogEntry._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'logEntry'), LogEntry, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'logEntry')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)
