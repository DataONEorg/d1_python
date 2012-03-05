# ./d1_common/types/generated/dataoneTypes.py
# PyXB bindings for NM:b5056e9f5bcbaa65eac428b50fd841172c48ddf9
# Generated 2012-03-02 08:44:18.700270 by PyXB version 1.1.3
# Namespace http://ns.dataone.org/service/types/v1

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:927b915e-647e-11e1-b39f-000c294230b4')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'http://ns.dataone.org/service/types/v1', create_if_missing=True)
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
class NonEmptyString (pyxb.binding.datatypes.string):

    """A derived string type with at least length 1 and it
      must contain non-whitespace."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonEmptyString')
    _Documentation = u'A derived string type with at least length 1 and it\n      must contain non-whitespace.'
NonEmptyString._CF_pattern = pyxb.binding.facets.CF_pattern()
NonEmptyString._CF_pattern.addPattern(pattern=u'[\\s]*[\\S][\\s\\S]*')
NonEmptyString._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1L))
NonEmptyString._InitializeFacetMap(NonEmptyString._CF_pattern,
   NonEmptyString._CF_minLength)
Namespace.addCategoryObject('typeBinding', u'NonEmptyString', NonEmptyString)

# Atomic SimpleTypeDefinition
class ChecksumAlgorithm (pyxb.binding.datatypes.string):

    """The cryptographic hash algorithm used to calculate a
      checksum. DataONE recognizes the Library of Congress list of
      cryptographic hash algorithms that can be used as names in this field,
      and specifically uses the *madsrdf:authoritativeLabel* field as the name
      of the algorithm in this field. See: `Library of Congress Cryptographic
      Algorithm Vocabulary`_. All compliant implementations must support at
      least SHA-1 and MD5, but may support other algorithms as well.Valid entries include: SHA-1, MD5The default checksum is *SHA-1*... _Library of Congress Cryptographic Algorithm Vocabulary: http://id.loc.gov/vocabulary/cryptographicHashFunctions.rdf
      """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ChecksumAlgorithm')
    _Documentation = u'The cryptographic hash algorithm used to calculate a\n      checksum. DataONE recognizes the Library of Congress list of\n      cryptographic hash algorithms that can be used as names in this field,\n      and specifically uses the *madsrdf:authoritativeLabel* field as the name\n      of the algorithm in this field. See: `Library of Congress Cryptographic\n      Algorithm Vocabulary`_. All compliant implementations must support at\n      least SHA-1 and MD5, but may support other algorithms as well.Valid entries include: SHA-1, MD5The default checksum is *SHA-1*... _Library of Congress Cryptographic Algorithm Vocabulary: http://id.loc.gov/vocabulary/cryptographicHashFunctions.rdf\n      '
ChecksumAlgorithm._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ChecksumAlgorithm', ChecksumAlgorithm)

# Atomic SimpleTypeDefinition
class ObjectFormatIdentifier (NonEmptyString):

    """A string used to identify an instance of
      :class:`Types.ObjectFormat` and MUST be unique within an instance of
      :class:`Types.ObjectFormatList`. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectFormatIdentifier')
    _Documentation = u'A string used to identify an instance of\n      :class:`Types.ObjectFormat` and MUST be unique within an instance of\n      :class:`Types.ObjectFormatList`. '
ObjectFormatIdentifier._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ObjectFormatIdentifier', ObjectFormatIdentifier)

# Atomic SimpleTypeDefinition
class NonEmptyString800 (NonEmptyString):

    """ An NonEmptyString800 is a NonEmptyString string with
      a maximum length of 800 characters."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonEmptyString800')
    _Documentation = u' An NonEmptyString800 is a NonEmptyString string with\n      a maximum length of 800 characters.'
NonEmptyString800._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(800L))
NonEmptyString800._InitializeFacetMap(NonEmptyString800._CF_maxLength)
Namespace.addCategoryObject('typeBinding', u'NonEmptyString800', NonEmptyString800)

# Atomic SimpleTypeDefinition
class NonEmptyNoWhitespaceString800 (NonEmptyString800):

    """A NonEmptyNoWhitespaceString800 is a NonEmptyString800
      string that doesn't allow whitespace characters (space, tab, newline,
      carriage return). Unicode whitespace characters outside of the ASCII
      character set need to be checked programmatically."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonEmptyNoWhitespaceString800')
    _Documentation = u"A NonEmptyNoWhitespaceString800 is a NonEmptyString800\n      string that doesn't allow whitespace characters (space, tab, newline,\n      carriage return). Unicode whitespace characters outside of the ASCII\n      character set need to be checked programmatically."
NonEmptyNoWhitespaceString800._CF_pattern = pyxb.binding.facets.CF_pattern()
NonEmptyNoWhitespaceString800._CF_pattern.addPattern(pattern=u'\\S+')
NonEmptyNoWhitespaceString800._InitializeFacetMap(NonEmptyNoWhitespaceString800._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'NonEmptyNoWhitespaceString800', NonEmptyNoWhitespaceString800)

# Atomic SimpleTypeDefinition
class CrontabEntry (pyxb.binding.datatypes.token):

    """A single value in the series of values that together 
      form a single crontab entry. The format follows the syntax conventions 
      defined by the `Quartz Scheduler`_, as excerpted here under the Apache 2 license:.. _Quartz Scheduler: http://www.quartz-scheduler.org/api/2.1.0/org/quartz/CronExpression.html.. include:: Types_crontabentry.txt"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CrontabEntry')
    _Documentation = u'A single value in the series of values that together \n      form a single crontab entry. The format follows the syntax conventions \n      defined by the `Quartz Scheduler`_, as excerpted here under the Apache 2 license:.. _Quartz Scheduler: http://www.quartz-scheduler.org/api/2.1.0/org/quartz/CronExpression.html.. include:: Types_crontabentry.txt'
CrontabEntry._CF_pattern = pyxb.binding.facets.CF_pattern()
CrontabEntry._CF_pattern.addPattern(pattern=u'([\\?\\*\\d/#,\\-a-zA-Z])+')
CrontabEntry._InitializeFacetMap(CrontabEntry._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'CrontabEntry', CrontabEntry)

# Atomic SimpleTypeDefinition
class CrontabEntrySeconds (pyxb.binding.datatypes.token):

    """A restriction on the seconds field in a single 
      Schedule entry, following the syntax conventions defined by the `Quartz
      Scheduler`_.The wildcard character value is not allowed in this
      (seconds) field as this would create an impractical synchronization
      schedule.. _Quartz Scheduler: http://www.quartz-scheduler.org/api/2.1.0/org/quartz/CronExpression.html"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CrontabEntrySeconds')
    _Documentation = u'A restriction on the seconds field in a single \n      Schedule entry, following the syntax conventions defined by the `Quartz\n      Scheduler`_.The wildcard character value is not allowed in this\n      (seconds) field as this would create an impractical synchronization\n      schedule.. _Quartz Scheduler: http://www.quartz-scheduler.org/api/2.1.0/org/quartz/CronExpression.html'
CrontabEntrySeconds._CF_pattern = pyxb.binding.facets.CF_pattern()
CrontabEntrySeconds._CF_pattern.addPattern(pattern=u'[0-5]?\\d')
CrontabEntrySeconds._InitializeFacetMap(CrontabEntrySeconds._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'CrontabEntrySeconds', CrontabEntrySeconds)

# Atomic SimpleTypeDefinition
class ServiceName (NonEmptyString):

    """The name of a service that is available on a
      Node."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceName')
    _Documentation = u'The name of a service that is available on a\n      Node.'
ServiceName._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ServiceName', ServiceName)

# Atomic SimpleTypeDefinition
class ServiceVersion (NonEmptyString):

    """The version of a service provided by a Node. Service
      versions are expressed as version labels such as "v1", "v2". DataONE
      services are released only as major service versions; patches to
      services are not indicated in this version label."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceVersion')
    _Documentation = u'The version of a service provided by a Node. Service\n      versions are expressed as version labels such as "v1", "v2". DataONE\n      services are released only as major service versions; patches to\n      services are not indicated in this version label.'
ServiceVersion._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ServiceVersion', ServiceVersion)

# Atomic SimpleTypeDefinition
class Permission (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """A string value indicating the set of actions that can
      be performed on a resource as specified in an access policy. The set of
      permissions include the ability to read a resource (*read*), modify a
      resource (*write*), and to change the set of access control policies for
      a resource (*changePermission*). Permission levels are cumulative, in
      that write permission implicitly grants read access, and
      changePermission permission implicitly grants write access (and
      therefore read as well). If a subject is granted multiple permissions,
      the highest level of access applies."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Permission')
    _Documentation = u'A string value indicating the set of actions that can\n      be performed on a resource as specified in an access policy. The set of\n      permissions include the ability to read a resource (*read*), modify a\n      resource (*write*), and to change the set of access control policies for\n      a resource (*changePermission*). Permission levels are cumulative, in\n      that write permission implicitly grants read access, and\n      changePermission permission implicitly grants write access (and\n      therefore read as well). If a subject is granted multiple permissions,\n      the highest level of access applies.'
Permission._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Permission, enum_prefix=None)
Permission.read = Permission._CF_enumeration.addEnumeration(unicode_value=u'read', tag=u'read')
Permission.write = Permission._CF_enumeration.addEnumeration(unicode_value=u'write', tag=u'write')
Permission.changePermission = Permission._CF_enumeration.addEnumeration(unicode_value=u'changePermission', tag=u'changePermission')
Permission._InitializeFacetMap(Permission._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'Permission', Permission)

# Atomic SimpleTypeDefinition
class NodeState (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """An indicator of the current node accessibility. Nodes
      that are marked *down* are inaccessible for service operations, those
      that are *up* are in the normal accessible state, and *unknown*
      indicates that the state has not been determined yet."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeState')
    _Documentation = u'An indicator of the current node accessibility. Nodes\n      that are marked *down* are inaccessible for service operations, those\n      that are *up* are in the normal accessible state, and *unknown*\n      indicates that the state has not been determined yet.'
NodeState._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=NodeState, enum_prefix=None)
NodeState.up = NodeState._CF_enumeration.addEnumeration(unicode_value=u'up', tag=u'up')
NodeState.down = NodeState._CF_enumeration.addEnumeration(unicode_value=u'down', tag=u'down')
NodeState.unknown = NodeState._CF_enumeration.addEnumeration(unicode_value=u'unknown', tag=u'unknown')
NodeState._InitializeFacetMap(NodeState._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'NodeState', NodeState)

# Atomic SimpleTypeDefinition
class NodeType (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """The type of this node, which is either *mn* for
      Member Nodes, or *cn* for Coordinating Nodes."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeType')
    _Documentation = u'The type of this node, which is either *mn* for\n      Member Nodes, or *cn* for Coordinating Nodes.'
NodeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=NodeType, enum_prefix=None)
NodeType.mn = NodeType._CF_enumeration.addEnumeration(unicode_value=u'mn', tag=u'mn')
NodeType.cn = NodeType._CF_enumeration.addEnumeration(unicode_value=u'cn', tag=u'cn')
NodeType.Monitor = NodeType._CF_enumeration.addEnumeration(unicode_value=u'Monitor', tag=u'Monitor')
NodeType._InitializeFacetMap(NodeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'NodeType', NodeType)

# Atomic SimpleTypeDefinition
class ReplicationStatus (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An enumerated string value indicating the current
      state of a replica of an object. When an object identified needs to be
      replicated, it is added to the replication task queue and is marked as
      *queued*; a CN will pick up that task and request that it be replicated
      to a MN and marks that it as *requested*; when a MN finishes replicating
      the object, it informs the CN that it is finished and it is marked as
      *completed*. If an MN is unable to complete replication, the
      replication status is marked as *failed*.Periodically a CN checks each replica to be sure it is
      both available and valid (matching checksum with original), and if it is
      either inaccessible or invalid then it marks it as *invalidated*, which
      indicates that the object replication needs to be invoked
      again.The replication process is described in Use Case 09 
      (:doc:`/design/UseCases/09_uc`)."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReplicationStatus')
    _Documentation = u'An enumerated string value indicating the current\n      state of a replica of an object. When an object identified needs to be\n      replicated, it is added to the replication task queue and is marked as\n      *queued*; a CN will pick up that task and request that it be replicated\n      to a MN and marks that it as *requested*; when a MN finishes replicating\n      the object, it informs the CN that it is finished and it is marked as\n      *completed*. If an MN is unable to complete replication, the\n      replication status is marked as *failed*.Periodically a CN checks each replica to be sure it is\n      both available and valid (matching checksum with original), and if it is\n      either inaccessible or invalid then it marks it as *invalidated*, which\n      indicates that the object replication needs to be invoked\n      again.The replication process is described in Use Case 09 \n      (:doc:`/design/UseCases/09_uc`).'
ReplicationStatus._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ReplicationStatus, enum_prefix=None)
ReplicationStatus.queued = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'queued', tag=u'queued')
ReplicationStatus.requested = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'requested', tag=u'requested')
ReplicationStatus.completed = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'completed', tag=u'completed')
ReplicationStatus.failed = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'failed', tag=u'failed')
ReplicationStatus.invalidated = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'invalidated', tag=u'invalidated')
ReplicationStatus._InitializeFacetMap(ReplicationStatus._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ReplicationStatus', ReplicationStatus)

# Atomic SimpleTypeDefinition
class Event (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """The controlled list of events that are logged, which
      will include *create*, *update*, *delete*, *read*, *replicate*,
      *synchronization_failed* and *replication_failed*
      events."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Event')
    _Documentation = u'The controlled list of events that are logged, which\n      will include *create*, *update*, *delete*, *read*, *replicate*,\n      *synchronization_failed* and *replication_failed*\n      events.'
Event._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Event, enum_prefix=None)
Event.create = Event._CF_enumeration.addEnumeration(unicode_value=u'create', tag=u'create')
Event.read = Event._CF_enumeration.addEnumeration(unicode_value=u'read', tag=u'read')
Event.update = Event._CF_enumeration.addEnumeration(unicode_value=u'update', tag=u'update')
Event.delete = Event._CF_enumeration.addEnumeration(unicode_value=u'delete', tag=u'delete')
Event.replicate = Event._CF_enumeration.addEnumeration(unicode_value=u'replicate', tag=u'replicate')
Event.synchronization_failed = Event._CF_enumeration.addEnumeration(unicode_value=u'synchronization_failed', tag=u'synchronization_failed')
Event.replication_failed = Event._CF_enumeration.addEnumeration(unicode_value=u'replication_failed', tag=u'replication_failed')
Event._InitializeFacetMap(Event._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'Event', Event)

# Complex type NodeReference with content type SIMPLE
class NodeReference (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = NonEmptyString
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeReference')
    # Base type is NonEmptyString

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'NodeReference', NodeReference)


# Complex type Synchronization with content type ELEMENT_ONLY
class Synchronization (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Synchronization')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element lastCompleteHarvest uses Python identifier lastCompleteHarvest
    __lastCompleteHarvest = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), 'lastCompleteHarvest', '__httpns_dataone_orgservicetypesv1_Synchronization_lastCompleteHarvest', False)

    
    lastCompleteHarvest = property(__lastCompleteHarvest.value, __lastCompleteHarvest.set, None, u'The last time (UTC) all the data from a node was\n          pulled from a member node during a complete synchronization\n          process.')

    
    # Element schedule uses Python identifier schedule
    __schedule = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'schedule'), 'schedule', '__httpns_dataone_orgservicetypesv1_Synchronization_schedule', False)

    
    schedule = property(__schedule.value, __schedule.set, None, u'An entry set by the Member Node indicating the\n          frequency for which synchronization should occur. This setting will\n          be influenced by the frequency with which content is updated on the\n          Member Node and the acceptable latency for detection and subsequent\n          processing of new content.')

    
    # Element lastHarvested uses Python identifier lastHarvested
    __lastHarvested = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastHarvested'), 'lastHarvested', '__httpns_dataone_orgservicetypesv1_Synchronization_lastHarvested', False)

    
    lastHarvested = property(__lastHarvested.value, __lastHarvested.set, None, u'The most recent modification date (UTC) of objects\n          checked during the last harvest of the node.')


    _ElementMap = {
        __lastCompleteHarvest.name() : __lastCompleteHarvest,
        __schedule.name() : __schedule,
        __lastHarvested.name() : __lastHarvested
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Synchronization', Synchronization)


# Complex type LogEntry with content type ELEMENT_ONLY
class LogEntry (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LogEntry')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_LogEntry_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'The :term:`identifier` of the object that was the\n          target of the operation which generated this log entry.')

    
    # Element entryId uses Python identifier entryId
    __entryId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'entryId'), 'entryId', '__httpns_dataone_orgservicetypesv1_LogEntry_entryId', False)

    
    entryId = property(__entryId.value, __entryId.set, None, u'A unique identifier for this log entry. The\n          identifier should be unique for a particular node; This is not drawn\n          from the same value space as other identifiers in DataONE, and so is\n          not subjec to the same restrictions.')

    
    # Element dateLogged uses Python identifier dateLogged
    __dateLogged = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateLogged'), 'dateLogged', '__httpns_dataone_orgservicetypesv1_LogEntry_dateLogged', False)

    
    dateLogged = property(__dateLogged.value, __dateLogged.set, None, u'A :class:`Types.DateTime` time stamp indicating when\n          the event triggering the log message ocurred. Note that all time\n          stamps in DataONE are in UTC.')

    
    # Element nodeIdentifier uses Python identifier nodeIdentifier
    __nodeIdentifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), 'nodeIdentifier', '__httpns_dataone_orgservicetypesv1_LogEntry_nodeIdentifier', False)

    
    nodeIdentifier = property(__nodeIdentifier.value, __nodeIdentifier.set, None, u'The unique identifier for the node where the log\n          message was generated.')

    
    # Element ipAddress uses Python identifier ipAddress
    __ipAddress = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ipAddress'), 'ipAddress', '__httpns_dataone_orgservicetypesv1_LogEntry_ipAddress', False)

    
    ipAddress = property(__ipAddress.value, __ipAddress.set, None, u'The IP address, as reported by the service receiving\n          the request, of the request origin.')

    
    # Element event uses Python identifier event
    __event = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'event'), 'event', '__httpns_dataone_orgservicetypesv1_LogEntry_event', False)

    
    event = property(__event.value, __event.set, None, u'An entry from the :class:`Types.Event` enumeration\n          indicating the type of operation that triggered the log message.')

    
    # Element userAgent uses Python identifier userAgent
    __userAgent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'userAgent'), 'userAgent', '__httpns_dataone_orgservicetypesv1_LogEntry_userAgent', False)

    
    userAgent = property(__userAgent.value, __userAgent.set, None, u'The user agent of the client making the request, as\n          reported in the User-Agent HTTP header.')

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_LogEntry_subject', False)

    
    subject = property(__subject.value, __subject.set, None, u'The :term:`Subject` used for making the request.\n          This may be the DataONE :term:`public` user if the request is not\n          authenticated, otherwise it will be the *Subject* of the certificate\n          used for authenticating the request.')


    _ElementMap = {
        __identifier.name() : __identifier,
        __entryId.name() : __entryId,
        __dateLogged.name() : __dateLogged,
        __nodeIdentifier.name() : __nodeIdentifier,
        __ipAddress.name() : __ipAddress,
        __event.name() : __event,
        __userAgent.name() : __userAgent,
        __subject.name() : __subject
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LogEntry', LogEntry)


# Complex type Slice with content type EMPTY
class Slice (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Slice')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute count uses Python identifier count
    __count = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'count'), 'count', '__httpns_dataone_orgservicetypesv1_Slice_count', pyxb.binding.datatypes.int, required=True)
    
    count = property(__count.value, __count.set, None, u'The number of entries in the\n        slice.')

    
    # Attribute start uses Python identifier start
    __start = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'start'), 'start', '__httpns_dataone_orgservicetypesv1_Slice_start', pyxb.binding.datatypes.int, required=True)
    
    start = property(__start.value, __start.set, None, u'The zero-based index of the first element in the\n        slice.')

    
    # Attribute total uses Python identifier total
    __total = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'total'), 'total', '__httpns_dataone_orgservicetypesv1_Slice_total', pyxb.binding.datatypes.int, required=True)
    
    total = property(__total.value, __total.set, None, u'The total number of entries in the source list from\n        which the slice was extracted.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __count.name() : __count,
        __start.name() : __start,
        __total.name() : __total
    }
Namespace.addCategoryObject('typeBinding', u'Slice', Slice)


# Complex type Log with content type ELEMENT_ONLY
class Log (Slice):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Log')
    # Base type is Slice
    
    # Element logEntry uses Python identifier logEntry
    __logEntry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'logEntry'), 'logEntry', '__httpns_dataone_orgservicetypesv1_Log_logEntry', True)

    
    logEntry = property(__logEntry.value, __logEntry.set, None, None)

    
    # Attribute count inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute start inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute total inherited from {http://ns.dataone.org/service/types/v1}Slice

    _ElementMap = Slice._ElementMap.copy()
    _ElementMap.update({
        __logEntry.name() : __logEntry
    })
    _AttributeMap = Slice._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Log', Log)


# Complex type Replica with content type ELEMENT_ONLY
class Replica (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Replica')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element replicaVerified uses Python identifier replicaVerified
    __replicaVerified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicaVerified'), 'replicaVerified', '__httpns_dataone_orgservicetypesv1_Replica_replicaVerified', False)

    
    replicaVerified = property(__replicaVerified.value, __replicaVerified.set, None, u' The last date and time on which the integrity of\n          a replica was verified by the coordinating node. Verification occurs\n          by checking that the checksum of the stored object matches the\n          checksum recorded for the object in the system\n          metadata.')

    
    # Element replicaMemberNode uses Python identifier replicaMemberNode
    __replicaMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicaMemberNode'), 'replicaMemberNode', '__httpns_dataone_orgservicetypesv1_Replica_replicaMemberNode', False)

    
    replicaMemberNode = property(__replicaMemberNode.value, __replicaMemberNode.set, None, u'A reference to the Member Node that houses this\n          replica, regardless of whether it has arrived at the Member Node or\n          not. See *replicationStatus* to determine if the replica is\n          completely transferred. ')

    
    # Element replicationStatus uses Python identifier replicationStatus
    __replicationStatus = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicationStatus'), 'replicationStatus', '__httpns_dataone_orgservicetypesv1_Replica_replicationStatus', False)

    
    replicationStatus = property(__replicationStatus.value, __replicationStatus.set, None, u' The current status of this replica, indicating\n          the stage of replication process for the object. Only *completed*\n          replicas should be considered as available. ')


    _ElementMap = {
        __replicaVerified.name() : __replicaVerified,
        __replicaMemberNode.name() : __replicaMemberNode,
        __replicationStatus.name() : __replicationStatus
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Replica', Replica)


# Complex type AccessRule with content type ELEMENT_ONLY
class AccessRule (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AccessRule')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element permission uses Python identifier permission
    __permission = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'permission'), 'permission', '__httpns_dataone_orgservicetypesv1_AccessRule_permission', True)

    
    permission = property(__permission.value, __permission.set, None, None)

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_AccessRule_subject', True)

    
    subject = property(__subject.value, __subject.set, None, None)


    _ElementMap = {
        __permission.name() : __permission,
        __subject.name() : __subject
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AccessRule', AccessRule)


# Complex type Services with content type ELEMENT_ONLY
class Services (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Services')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element service uses Python identifier service
    __service = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpns_dataone_orgservicetypesv1_Services_service', True)

    
    service = property(__service.value, __service.set, None, None)


    _ElementMap = {
        __service.name() : __service
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Services', Services)


# Complex type Checksum with content type SIMPLE
class Checksum (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Checksum')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute algorithm uses Python identifier algorithm
    __algorithm = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'algorithm'), 'algorithm', '__httpns_dataone_orgservicetypesv1_Checksum_algorithm', ChecksumAlgorithm, required=True)
    
    algorithm = property(__algorithm.value, __algorithm.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __algorithm.name() : __algorithm
    }
Namespace.addCategoryObject('typeBinding', u'Checksum', Checksum)


# Complex type SubjectList with content type ELEMENT_ONLY
class SubjectList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SubjectList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_SubjectList_subject', True)

    
    subject = property(__subject.value, __subject.set, None, None)


    _ElementMap = {
        __subject.name() : __subject
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SubjectList', SubjectList)


# Complex type Subject with content type SIMPLE
class Subject (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = NonEmptyString
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Subject')
    # Base type is NonEmptyString

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Subject', Subject)


# Complex type ReplicationPolicy with content type ELEMENT_ONLY
class ReplicationPolicy (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReplicationPolicy')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element blockedMemberNode uses Python identifier blockedMemberNode
    __blockedMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'blockedMemberNode'), 'blockedMemberNode', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_blockedMemberNode', True)

    
    blockedMemberNode = property(__blockedMemberNode.value, __blockedMemberNode.set, None, u'The object MUST never be replicated to nodes\n          listed as *blockedMemberNodes*. Where there is a conflict between a\n          *preferredMemberNode* and a *blockedMemberNode* entry, the\n          *blockedMemberNode* entry prevails. ')

    
    # Element preferredMemberNode uses Python identifier preferredMemberNode
    __preferredMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'preferredMemberNode'), 'preferredMemberNode', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_preferredMemberNode', True)

    
    preferredMemberNode = property(__preferredMemberNode.value, __preferredMemberNode.set, None, u'Preferred Nodes are utilized over other nodes as\n          replication targets, up to the number of replicas requested. If\n          preferred nodes are unavailable, or if insufficient nodes are listed\n          as preferred to meet the requested number of replicas, then the\n          Coordinating Nodes will pick additional replica nodes for the\n          content. ')

    
    # Attribute replicationAllowed uses Python identifier replicationAllowed
    __replicationAllowed = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'replicationAllowed'), 'replicationAllowed', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_replicationAllowed', pyxb.binding.datatypes.boolean)
    
    replicationAllowed = property(__replicationAllowed.value, __replicationAllowed.set, None, u'A boolean flag indicating if the object should be\n        replicated (*true*, default) or not (*false*).')

    
    # Attribute numberReplicas uses Python identifier numberReplicas
    __numberReplicas = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'numberReplicas'), 'numberReplicas', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_numberReplicas', pyxb.binding.datatypes.int)
    
    numberReplicas = property(__numberReplicas.value, __numberReplicas.set, None, u'An integer indicating the number of replicas\n        targeted for this object. Defaults to 3.')


    _ElementMap = {
        __blockedMemberNode.name() : __blockedMemberNode,
        __preferredMemberNode.name() : __preferredMemberNode
    }
    _AttributeMap = {
        __replicationAllowed.name() : __replicationAllowed,
        __numberReplicas.name() : __numberReplicas
    }
Namespace.addCategoryObject('typeBinding', u'ReplicationPolicy', ReplicationPolicy)


# Complex type Identifier with content type SIMPLE
class Identifier (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = NonEmptyNoWhitespaceString800
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Identifier')
    # Base type is NonEmptyNoWhitespaceString800

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Identifier', Identifier)


# Complex type Person with content type ELEMENT_ONLY
class Person (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Person')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element familyName uses Python identifier familyName
    __familyName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'familyName'), 'familyName', '__httpns_dataone_orgservicetypesv1_Person_familyName', False)

    
    familyName = property(__familyName.value, __familyName.set, None, u'The family name of the *Person*.')

    
    # Element isMemberOf uses Python identifier isMemberOf
    __isMemberOf = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'isMemberOf'), 'isMemberOf', '__httpns_dataone_orgservicetypesv1_Person_isMemberOf', True)

    
    isMemberOf = property(__isMemberOf.value, __isMemberOf.set, None, u'A *group* or role in which the *Person* is a member,\n          expressed using the unique :class:`Types.Subject` identifier for\n          that :class:`Types.Group`, and repeatable if they are a member of\n          more than one group. ')

    
    # Element email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'email'), 'email', '__httpns_dataone_orgservicetypesv1_Person_email', True)

    
    email = property(__email.value, __email.set, None, u'The email address of the *Person*, repeatable if\n          they have more than one email address. ')

    
    # Element equivalentIdentity uses Python identifier equivalentIdentity
    __equivalentIdentity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'equivalentIdentity'), 'equivalentIdentity', '__httpns_dataone_orgservicetypesv1_Person_equivalentIdentity', True)

    
    equivalentIdentity = property(__equivalentIdentity.value, __equivalentIdentity.set, None, u'An alternative but equivalent identity for the\n          :term:`principal` that has been used in alternate identity systems,\n          repeatable if more than one equivalent identity applies.\n          ')

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Person_subject', False)

    
    subject = property(__subject.value, __subject.set, None, u'The unique, immutable identifier for the\n          *Person*.')

    
    # Element verified uses Python identifier verified
    __verified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'verified'), 'verified', '__httpns_dataone_orgservicetypesv1_Person_verified', False)

    
    verified = property(__verified.value, __verified.set, None, u"*true* if the name and email address of the\n          *Person* have been :term:`verified` to ensure that the *givenName*\n          and *familyName* represent the real person's legal name, and that\n          the email address is correct for that person and is in the control\n          of the indicated individual. Verification occurs through an\n          established procedure within DataONE as part of the Identity\n          Management system. A Person can not change their own *verified*\n          field, but rather must be verified and changed through this DataONE\n          established process. ")

    
    # Element givenName uses Python identifier givenName
    __givenName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'givenName'), 'givenName', '__httpns_dataone_orgservicetypesv1_Person_givenName', True)

    
    givenName = property(__givenName.value, __givenName.set, None, u'The given name of the *Person*, repeatable if they\n          have more than one given name.')


    _ElementMap = {
        __familyName.name() : __familyName,
        __isMemberOf.name() : __isMemberOf,
        __email.name() : __email,
        __equivalentIdentity.name() : __equivalentIdentity,
        __subject.name() : __subject,
        __verified.name() : __verified,
        __givenName.name() : __givenName
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Person', Person)


# Complex type Schedule with content type EMPTY
class Schedule (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Schedule')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute mon uses Python identifier mon
    __mon = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mon'), 'mon', '__httpns_dataone_orgservicetypesv1_Schedule_mon', CrontabEntry, required=True)
    
    mon = property(__mon.value, __mon.set, None, None)

    
    # Attribute hour uses Python identifier hour
    __hour = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'hour'), 'hour', '__httpns_dataone_orgservicetypesv1_Schedule_hour', CrontabEntry, required=True)
    
    hour = property(__hour.value, __hour.set, None, None)

    
    # Attribute sec uses Python identifier sec
    __sec = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'sec'), 'sec', '__httpns_dataone_orgservicetypesv1_Schedule_sec', CrontabEntrySeconds, required=True)
    
    sec = property(__sec.value, __sec.set, None, None)

    
    # Attribute wday uses Python identifier wday
    __wday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'wday'), 'wday', '__httpns_dataone_orgservicetypesv1_Schedule_wday', CrontabEntry, required=True)
    
    wday = property(__wday.value, __wday.set, None, None)

    
    # Attribute year uses Python identifier year
    __year = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'year'), 'year', '__httpns_dataone_orgservicetypesv1_Schedule_year', CrontabEntry, required=True)
    
    year = property(__year.value, __year.set, None, None)

    
    # Attribute mday uses Python identifier mday
    __mday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mday'), 'mday', '__httpns_dataone_orgservicetypesv1_Schedule_mday', CrontabEntry, required=True)
    
    mday = property(__mday.value, __mday.set, None, None)

    
    # Attribute min uses Python identifier min
    __min = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'min'), 'min', '__httpns_dataone_orgservicetypesv1_Schedule_min', CrontabEntry, required=True)
    
    min = property(__min.value, __min.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __mon.name() : __mon,
        __hour.name() : __hour,
        __sec.name() : __sec,
        __wday.name() : __wday,
        __year.name() : __year,
        __mday.name() : __mday,
        __min.name() : __min
    }
Namespace.addCategoryObject('typeBinding', u'Schedule', Schedule)


# Complex type NodeReplicationPolicy with content type ELEMENT_ONLY
class NodeReplicationPolicy (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeReplicationPolicy')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element allowedObjectFormat uses Python identifier allowedObjectFormat
    __allowedObjectFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'allowedObjectFormat'), 'allowedObjectFormat', '__httpns_dataone_orgservicetypesv1_NodeReplicationPolicy_allowedObjectFormat', True)

    
    allowedObjectFormat = property(__allowedObjectFormat.value, __allowedObjectFormat.set, None, u'An optional, repeatable statement of an object\n          format that this node is willing to replicate, expressed as a\n          :class:`Types.ObjectFormatIdentifier`.')

    
    # Element maxObjectSize uses Python identifier maxObjectSize
    __maxObjectSize = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'maxObjectSize'), 'maxObjectSize', '__httpns_dataone_orgservicetypesv1_NodeReplicationPolicy_maxObjectSize', False)

    
    maxObjectSize = property(__maxObjectSize.value, __maxObjectSize.set, None, u'An optional statement of the maximum size in octets \n          (8-bit bytes) of objects this node is willing to accept for\n          replication.')

    
    # Element allowedNode uses Python identifier allowedNode
    __allowedNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'allowedNode'), 'allowedNode', '__httpns_dataone_orgservicetypesv1_NodeReplicationPolicy_allowedNode', True)

    
    allowedNode = property(__allowedNode.value, __allowedNode.set, None, u'An optional, repeatable statement of a peer source\n          node from which this node is willing to replicate content, expressed\n          as a :class:`Types.NodeReference`.')

    
    # Element spaceAllocated uses Python identifier spaceAllocated
    __spaceAllocated = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'spaceAllocated'), 'spaceAllocated', '__httpns_dataone_orgservicetypesv1_NodeReplicationPolicy_spaceAllocated', False)

    
    spaceAllocated = property(__spaceAllocated.value, __spaceAllocated.set, None, u'An optional statement of the total space in bytes\n          allocated for replication object storage on this\n          node.')


    _ElementMap = {
        __allowedObjectFormat.name() : __allowedObjectFormat,
        __maxObjectSize.name() : __maxObjectSize,
        __allowedNode.name() : __allowedNode,
        __spaceAllocated.name() : __spaceAllocated
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'NodeReplicationPolicy', NodeReplicationPolicy)


# Complex type Service with content type ELEMENT_ONLY
class Service (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Service')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element restriction uses Python identifier restriction
    __restriction = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'restriction'), 'restriction', '__httpns_dataone_orgservicetypesv1_Service_restriction', True)

    
    restriction = property(__restriction.value, __restriction.set, None, u'A list of method names and :term:`Subjects` with\n          permission to invoke those methods.')

    
    # Attribute available uses Python identifier available
    __available = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'available'), 'available', '__httpns_dataone_orgservicetypesv1_Service_available', pyxb.binding.datatypes.boolean)
    
    available = property(__available.value, __available.set, None, u'A boolean flag indicating if the service is\n        available (*true*, default) or otherwise (*false*).\n        ')

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpns_dataone_orgservicetypesv1_Service_version', ServiceVersion, required=True)
    
    version = property(__version.value, __version.set, None, u'Version of the service supported by the node.\n        Version is expressed in whole steps, no minor version identifiers are\n        used. For example, the version 1.0.0 API would be indicated by the\n        value "v1"')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesv1_Service_name', ServiceName, required=True)
    
    name = property(__name.value, __name.set, None, u'The name of the service. The valid list of entries\n        for Member Nodes includes: *MNCore*, *MNRead*, *MNAuthorization*,\n        *MNStorage*, and *MNReplication*. The valid list of entries for\n        Coordinating Nodes includes: *CNCore*, *CNRead*, *CNAuthorization*,\n        *CNIdentity*, *CNReplication*, and *CNRegister*.')


    _ElementMap = {
        __restriction.name() : __restriction
    }
    _AttributeMap = {
        __available.name() : __available,
        __version.name() : __version,
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'Service', Service)


# Complex type ObjectInfo with content type ELEMENT_ONLY
class ObjectInfo (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectInfo')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element size uses Python identifier size
    __size = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'size'), 'size', '__httpns_dataone_orgservicetypesv1_ObjectInfo_size', False)

    
    size = property(__size.value, __size.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_ObjectInfo_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__httpns_dataone_orgservicetypesv1_ObjectInfo_checksum', False)

    
    checksum = property(__checksum.value, __checksum.set, None, None)

    
    # Element formatId uses Python identifier formatId
    __formatId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'formatId'), 'formatId', '__httpns_dataone_orgservicetypesv1_ObjectInfo_formatId', False)

    
    formatId = property(__formatId.value, __formatId.set, None, None)

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpns_dataone_orgservicetypesv1_ObjectInfo_dateSysMetadataModified', False)

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, None)


    _ElementMap = {
        __size.name() : __size,
        __identifier.name() : __identifier,
        __checksum.name() : __checksum,
        __formatId.name() : __formatId,
        __dateSysMetadataModified.name() : __dateSysMetadataModified
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectInfo', ObjectInfo)


# Complex type NodeList with content type ELEMENT_ONLY
class NodeList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element node uses Python identifier node
    __node = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'node'), 'node', '__httpns_dataone_orgservicetypesv1_NodeList_node', True)

    
    node = property(__node.value, __node.set, None, None)


    _ElementMap = {
        __node.name() : __node
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'NodeList', NodeList)


# Complex type SubjectInfo with content type ELEMENT_ONLY
class SubjectInfo (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SubjectInfo')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element group uses Python identifier group
    __group = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'group'), 'group', '__httpns_dataone_orgservicetypesv1_SubjectInfo_group', True)

    
    group = property(__group.value, __group.set, None, None)

    
    # Element person uses Python identifier person
    __person = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'person'), 'person', '__httpns_dataone_orgservicetypesv1_SubjectInfo_person', True)

    
    person = property(__person.value, __person.set, None, None)


    _ElementMap = {
        __group.name() : __group,
        __person.name() : __person
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SubjectInfo', SubjectInfo)


# Complex type Ping with content type EMPTY
class Ping (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Ping')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute lastSuccess uses Python identifier lastSuccess
    __lastSuccess = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'lastSuccess'), 'lastSuccess', '__httpns_dataone_orgservicetypesv1_Ping_lastSuccess', pyxb.binding.datatypes.dateTime)
    
    lastSuccess = property(__lastSuccess.value, __lastSuccess.set, None, u'The date time value (UTC) of the last time a\n        successful ping was performed.')

    
    # Attribute success uses Python identifier success
    __success = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'success'), 'success', '__httpns_dataone_orgservicetypesv1_Ping_success', pyxb.binding.datatypes.boolean)
    
    success = property(__success.value, __success.set, None, u'A boolean flag indicating *true* if the node was\n        reached by the last :func:`MNCore.ping` or :func:`CNCore.ping` call,\n        otherwise *false*.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __lastSuccess.name() : __lastSuccess,
        __success.name() : __success
    }
Namespace.addCategoryObject('typeBinding', u'Ping', Ping)


# Complex type ObjectLocation with content type ELEMENT_ONLY
class ObjectLocation (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectLocation')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element preference uses Python identifier preference
    __preference = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'preference'), 'preference', '__httpns_dataone_orgservicetypesv1_ObjectLocation_preference', False)

    
    preference = property(__preference.value, __preference.set, None, u'A weighting parameter that provides a hint to the\n          caller for the relative preference for nodes from which the content\n          should be retrieved. Higher values have higher preference.\n          ')

    
    # Element nodeIdentifier uses Python identifier nodeIdentifier
    __nodeIdentifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), 'nodeIdentifier', '__httpns_dataone_orgservicetypesv1_ObjectLocation_nodeIdentifier', False)

    
    nodeIdentifier = property(__nodeIdentifier.value, __nodeIdentifier.set, None, u'Identifier of the :class:`Types.Node` (the same\n          identifier used in the node registry for identifying the node).\n          ')

    
    # Element url uses Python identifier url
    __url = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'url'), 'url', '__httpns_dataone_orgservicetypesv1_ObjectLocation_url', False)

    
    url = property(__url.value, __url.set, None, u'The full (absolute) URL that can be used to\n          retrieve the object using the get() method of the rest\n          interface.For example, if identifier was "ABX154", and the\n          node had a base URL of ``http://mn1.dataone.org/mn`` then the value\n          would be \n          ``http://mn1.dataone.org/mn/v1/object/ABX154``')

    
    # Element version uses Python identifier version
    __version = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpns_dataone_orgservicetypesv1_ObjectLocation_version', True)

    
    version = property(__version.value, __version.set, None, u'The version of services implemented on the node.\n          Used with base url to construct a URL for service calls to this\n          node. Note that complete information on services available on a Node\n          is available from the :func:`CNCore.listNodes` service.\n          ')

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'baseURL'), 'baseURL', '__httpns_dataone_orgservicetypesv1_ObjectLocation_baseURL', False)

    
    baseURL = property(__baseURL.value, __baseURL.set, None, u'The current base URL (the *baseURL* element from\n          the :class:`Types.Node` record) for services implemented on the\n          target node. Used with service version to construct a URL for\n          service calls to this node. Note that complete information on\n          services available on a Node is available from the\n          :func:`CNCore.listNodes` service. ')


    _ElementMap = {
        __preference.name() : __preference,
        __nodeIdentifier.name() : __nodeIdentifier,
        __url.name() : __url,
        __version.name() : __version,
        __baseURL.name() : __baseURL
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectLocation', ObjectLocation)


# Complex type AccessPolicy with content type ELEMENT_ONLY
class AccessPolicy (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AccessPolicy')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element allow uses Python identifier allow
    __allow = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'allow'), 'allow', '__httpns_dataone_orgservicetypesv1_AccessPolicy_allow', True)

    
    allow = property(__allow.value, __allow.set, None, None)


    _ElementMap = {
        __allow.name() : __allow
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AccessPolicy', AccessPolicy)


# Complex type ObjectList with content type ELEMENT_ONLY
class ObjectList (Slice):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectList')
    # Base type is Slice
    
    # Element objectInfo uses Python identifier objectInfo
    __objectInfo = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectInfo'), 'objectInfo', '__httpns_dataone_orgservicetypesv1_ObjectList_objectInfo', True)

    
    objectInfo = property(__objectInfo.value, __objectInfo.set, None, None)

    
    # Attribute count inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute start inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute total inherited from {http://ns.dataone.org/service/types/v1}Slice

    _ElementMap = Slice._ElementMap.copy()
    _ElementMap.update({
        __objectInfo.name() : __objectInfo
    })
    _AttributeMap = Slice._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ObjectList', ObjectList)


# Complex type ObjectLocationList with content type ELEMENT_ONLY
class ObjectLocationList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectLocationList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element objectLocation uses Python identifier objectLocation
    __objectLocation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectLocation'), 'objectLocation', '__httpns_dataone_orgservicetypesv1_ObjectLocationList_objectLocation', True)

    
    objectLocation = property(__objectLocation.value, __objectLocation.set, None, u'List of nodes from which the object can be\n        retrieved')

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_ObjectLocationList_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'The :term:`identifier` of the object being\n        resolved.')


    _ElementMap = {
        __objectLocation.name() : __objectLocation,
        __identifier.name() : __identifier
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectLocationList', ObjectLocationList)


# Complex type Group with content type ELEMENT_ONLY
class Group (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Group')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element rightsHolder uses Python identifier rightsHolder
    __rightsHolder = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'rightsHolder'), 'rightsHolder', '__httpns_dataone_orgservicetypesv1_Group_rightsHolder', True)

    
    rightsHolder = property(__rightsHolder.value, __rightsHolder.set, None, u'Represents the list of owners of this :term:`group`.\n        All groups are readable by anyone in the DataONE system, but can only\n        be modified by subjects listed in *rightsHolder* fields. Designation\n        as a :term:`rightsHolder` allows the subject, or their equivalent\n        identities, to make changes to the mutable properties of the group,\n        including its name, membership list and rights holder list. The\n        subject of the group itself is immutable. ')

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Group_subject', False)

    
    subject = property(__subject.value, __subject.set, None, u'The unique, immutable identifier of the\n          :term:`group`. Group subjects must not be reused, and so they are\n          both immutable and can not be deleted from the DataONE\n          system.')

    
    # Element groupName uses Python identifier groupName
    __groupName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'groupName'), 'groupName', '__httpns_dataone_orgservicetypesv1_Group_groupName', False)

    
    groupName = property(__groupName.value, __groupName.set, None, u'The name of the Group.')

    
    # Element hasMember uses Python identifier hasMember
    __hasMember = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'hasMember'), 'hasMember', '__httpns_dataone_orgservicetypesv1_Group_hasMember', True)

    
    hasMember = property(__hasMember.value, __hasMember.set, None, u'A :term:`Subject` that is a member of this\n            group, expressed using the unique identifier for that\n            Subject.')


    _ElementMap = {
        __rightsHolder.name() : __rightsHolder,
        __subject.name() : __subject,
        __groupName.name() : __groupName,
        __hasMember.name() : __hasMember
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Group', Group)


# Complex type SystemMetadata with content type ELEMENT_ONLY
class SystemMetadata (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SystemMetadata')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element obsoletes uses Python identifier obsoletes
    __obsoletes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'obsoletes'), 'obsoletes', '__httpns_dataone_orgservicetypesv1_SystemMetadata_obsoletes', False)

    
    obsoletes = property(__obsoletes.value, __obsoletes.set, None, u'The :term:`Identifier` of an object that is a\n          prior version of the object described in this system metadata record\n          and that is obsoleted by this object. When an object is obsoleted,\n          it is removed from all DataONE search indices but is still\n          accessible from the :func:`CNRead.get` service. ')

    
    # Element authoritativeMemberNode uses Python identifier authoritativeMemberNode
    __authoritativeMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode'), 'authoritativeMemberNode', '__httpns_dataone_orgservicetypesv1_SystemMetadata_authoritativeMemberNode', False)

    
    authoritativeMemberNode = property(__authoritativeMemberNode.value, __authoritativeMemberNode.set, None, u' A reference to the Member Node that acts as the\n          authoritative source for an object in the system. The\n          *authoritativeMemberNode* will often also be the *originMemberNode*,\n          unless there has been a need to transfer authority for an object to\n          a new node, such as when a Member Node becomes defunct. The\n          *authoritativeMemberNode* has all the rights of the *rightsHolder*\n          to maintain and curate the object, including making any changes\n          necessary. ')

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__httpns_dataone_orgservicetypesv1_SystemMetadata_checksum', False)

    
    checksum = property(__checksum.value, __checksum.set, None, u' A calculated hash value used to validate object\n          integrity over time and after network transfers. The value is\n          calculated using a standard hashing algorithm that is accepted by\n          DataONE and that is indicated in the included *ChecksumAlgorithm*\n          attribute. ')

    
    # Element submitter uses Python identifier submitter
    __submitter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'submitter'), 'submitter', '__httpns_dataone_orgservicetypesv1_SystemMetadata_submitter', False)

    
    submitter = property(__submitter.value, __submitter.set, None, u':term:`Subject` who submitted the associated\n          abject to the DataONE Member Node. The Member Node must set this\n          field when it receives the system metadata document from a client\n          (the field is optional from the client perspective, but is required\n          when a MN creates an object). By default, the submitter lacks any\n          rights to modify an object, so care must be taken to set\n          *rightsHolder* and *accessPolicy* correctly with a reference to the\n          subject of the submitter if the submitter is to be able to make\n          further changes to the object.')

    
    # Element obsoletedBy uses Python identifier obsoletedBy
    __obsoletedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'obsoletedBy'), 'obsoletedBy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_obsoletedBy', False)

    
    obsoletedBy = property(__obsoletedBy.value, __obsoletedBy.set, None, u'The :term:`Identifier` of an object that is a\n          subsequent version of the object described in this system metadata\n          record and that therefore obsoletes this object. When an object is\n          obsoleted, it is removed from all DataONE search indices but is\n          still accessible from the :func:`CNRead.get` service.\n          ')

    
    # Element serialVersion uses Python identifier serialVersion
    __serialVersion = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'serialVersion'), 'serialVersion', '__httpns_dataone_orgservicetypesv1_SystemMetadata_serialVersion', False)

    
    serialVersion = property(__serialVersion.value, __serialVersion.set, None, u' A serial number maintained by the coordinating node\n            to indicate when changes have occurred to *SystemMetadata* to avoid\n            update conflicts. Clients should ensure that they have the most\n            recent version of a *SystemMetadata* document before attempting to\n            update, otherwise an error will be thrown to prevent conflicts. The\n            Coordinating Node must set this optional field when it receives the\n            system metadata document. ')

    
    # Element replica uses Python identifier replica
    __replica = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replica'), 'replica', '__httpns_dataone_orgservicetypesv1_SystemMetadata_replica', True)

    
    replica = property(__replica.value, __replica.set, None, u' A container field used to repeatedly provide\n          several metadata fields about each replica that exists in the\n          system, or is being replicated. Note that a *replica* field exists\n          even for the Authoritative/Origin Member Nodes so that the status of\n          those objects can be tracked. ')

    
    # Element archived uses Python identifier archived
    __archived = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'archived'), 'archived', '__httpns_dataone_orgservicetypesv1_SystemMetadata_archived', False)

    
    archived = property(__archived.value, __archived.set, None, u'A boolean flag, set to *true* if the object has\n          been classified as archived. An archived object does not show up in\n          search indexes in DataONE, but is still accessible via the CNRead\n          and MNRead services if associated access polices allow. The field is\n          optional, and if absent, then objects are implied to not be\n          archived, which is the same as setting archived to\n          *false*.')

    
    # Element originMemberNode uses Python identifier originMemberNode
    __originMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'originMemberNode'), 'originMemberNode', '__httpns_dataone_orgservicetypesv1_SystemMetadata_originMemberNode', False)

    
    originMemberNode = property(__originMemberNode.value, __originMemberNode.set, None, u'A reference to the Member Node that originally\n          uploaded the associated object. This value should never change, even\n          if the Member Node ceases to exist. ')

    
    # Element rightsHolder uses Python identifier rightsHolder
    __rightsHolder = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'rightsHolder'), 'rightsHolder', '__httpns_dataone_orgservicetypesv1_SystemMetadata_rightsHolder', False)

    
    rightsHolder = property(__rightsHolder.value, __rightsHolder.set, None, u':term:`Subject` that has ultimate authority for\n          the object and is authorized to make all decisions regarding the\n          disposition and accessibility of the object. The *rightsHolder* has\n          all rights to access the object, update the object, and grant\n          permissions for the object, even if additional access control rules\n          are not specified for the object. Typically, the *rightsHolder*\n          field would be set to the name of the subject submitting an object,\n          so that the person can make further changes later. By default, the\n          *submitter* lacks any rights to modify an object, so care must be\n          taken to set *rightsHolder* and *accessPolicy* correctly with a\n          reference to the subject of the *submitter* if the *submitter* is to\n          be able to make further changes to the object. ')

    
    # Element replicationPolicy uses Python identifier replicationPolicy
    __replicationPolicy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicationPolicy'), 'replicationPolicy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_replicationPolicy', False)

    
    replicationPolicy = property(__replicationPolicy.value, __replicationPolicy.set, None, u'A controlled list of policy choices that determine\n          how many replicas should be maintained for a given object and any\n          preferences or requirements as to which Member Nodes should be\n          allowed to house the replicas. The policy determines whether\n          replication is allowed, the number of replicas desired, the list of\n          preferred nodes to hold the replicas, and a list of blocked nodes on\n          which replicas must not exist.')

    
    # Element dateUploaded uses Python identifier dateUploaded
    __dateUploaded = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateUploaded'), 'dateUploaded', '__httpns_dataone_orgservicetypesv1_SystemMetadata_dateUploaded', False)

    
    dateUploaded = property(__dateUploaded.value, __dateUploaded.set, None, u'Date and time (UTC) that the object was uploaded\n          into the DataONE system, which is typically the time that the object\n          is first created on a Member Node using the :func:`MNStorage.create`\n          operation. Note this is independent of the publication or release\n          date of the object. The Member Node must set this optional field\n          when it receives the system metadata document from a\n          client.')

    
    # Element formatId uses Python identifier formatId
    __formatId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'formatId'), 'formatId', '__httpns_dataone_orgservicetypesv1_SystemMetadata_formatId', False)

    
    formatId = property(__formatId.value, __formatId.set, None, u' Designation of the standard or format that should\n          be used to interpret the contents of the object, drawn from\n          controlled list of formats that are provided by the DataONE\n          :class:`Types.ObjectFormat` service. DataONE maintains a list of\n          formats in use and their canonical FormatIdentifiers. The format\n          identifier for an object should imply its mime type for data objects\n          and metadata type and serialization format for metadata objects.\n          Examples include the namespace of the EML 2.1 metadata\n          specification, the DOCTYPE of the Biological Data Profile, the mime\n          type of ``text/csv`` files, and the canonical name of the NetCDF\n          specification. ')

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpns_dataone_orgservicetypesv1_SystemMetadata_dateSysMetadataModified', False)

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, u' Date and time (UTC) that this system metadata\n          record was last modified in the DataONE system. This is the same\n          timestamp as *dateUploaded* until the system metadata is further\n          modified. The Member Node must set this optional field when it\n          receives the system metadata document from a\n          client.')

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_SystemMetadata_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'The :term:`identifier` is a unique Unicode string\n          that is used to canonically name and identify the object in DataONE.\n          Each object in DataONE is immutable, and therefore all objects must\n          have a unique Identifier. If two objects are related to one another\n          (such as one object is a more recent version of another object),\n          each of these two objects will have unique identifiers. The\n          relationship among the objects is specified in other metadata fields\n          (see *Obsoletes* and *ObsoletedBy*), but this does not preclude the\n          inclusion of version information in the identifier string. However,\n          DataONE treats all Identifiers as opaque and will not try to infer\n          versioning semantics based on the content of the Identifiers --\n          rather, this information is found in the *Obsoletes* and\n          *ObsoletedBy* fields. Note that identifiers are used in a number of\n          REST API calls as parts of the URL path. As such, all special\n          characters such as "/", " ", "+", "\\", "%" must be properly encoded,\n          e.g. "%2F", "%20", "%2B", "%5C", "%25" respectively when used in\n          REST method calls. See RFC3896_ for more details. For example, the\n          :func:`MNRead.get()` call for an object with identifier:``http://some.location.name/mydata.cgi?id=2088``would be:``http://mn1.server.name/mn/v1/object/http:%2F%2Fsome.location.name%2Fmydata.cgi%3Fid%3D2088``.. _RFC3896: http://www.ietf.org/rfc/rfc3896.txt ')

    
    # Element size uses Python identifier size
    __size = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'size'), 'size', '__httpns_dataone_orgservicetypesv1_SystemMetadata_size', False)

    
    size = property(__size.value, __size.set, None, u' The size of the object in octets (8-bit bytes).\n          ')

    
    # Element accessPolicy uses Python identifier accessPolicy
    __accessPolicy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'accessPolicy'), 'accessPolicy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_accessPolicy', False)

    
    accessPolicy = property(__accessPolicy.value, __accessPolicy.set, None, u'The *accessPolicy* determines which\n          :term:`Subjects` are allowed to make changes to an object in\n          addition to the *rightsHolder* and *authoritativeMemberNode*. The\n          *accessPolicy* is set for an object during a\n          :func:`MNStorage.create` or :func:`MNStorage.update` call, or when\n          *SystemMetadata* is updated on the Coordinating Node via various\n          mechanisms. This policy replaces any existing policies that might\n          exist for the object. Member Nodes that house an object are\n          obligated to enforce the *accessPolicy* for that\n          object.')


    _ElementMap = {
        __obsoletes.name() : __obsoletes,
        __authoritativeMemberNode.name() : __authoritativeMemberNode,
        __checksum.name() : __checksum,
        __submitter.name() : __submitter,
        __obsoletedBy.name() : __obsoletedBy,
        __serialVersion.name() : __serialVersion,
        __replica.name() : __replica,
        __archived.name() : __archived,
        __originMemberNode.name() : __originMemberNode,
        __rightsHolder.name() : __rightsHolder,
        __replicationPolicy.name() : __replicationPolicy,
        __dateUploaded.name() : __dateUploaded,
        __formatId.name() : __formatId,
        __dateSysMetadataModified.name() : __dateSysMetadataModified,
        __identifier.name() : __identifier,
        __size.name() : __size,
        __accessPolicy.name() : __accessPolicy
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SystemMetadata', SystemMetadata)


# Complex type ObjectFormatList with content type ELEMENT_ONLY
class ObjectFormatList (Slice):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectFormatList')
    # Base type is Slice
    
    # Element objectFormat uses Python identifier objectFormat
    __objectFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectFormat'), 'objectFormat', '__httpns_dataone_orgservicetypesv1_ObjectFormatList_objectFormat', True)

    
    objectFormat = property(__objectFormat.value, __objectFormat.set, None, None)

    
    # Attribute count inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute start inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute total inherited from {http://ns.dataone.org/service/types/v1}Slice

    _ElementMap = Slice._ElementMap.copy()
    _ElementMap.update({
        __objectFormat.name() : __objectFormat
    })
    _AttributeMap = Slice._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ObjectFormatList', ObjectFormatList)


# Complex type Session with content type ELEMENT_ONLY
class Session (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Session')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element subjectInfo uses Python identifier subjectInfo
    __subjectInfo = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subjectInfo'), 'subjectInfo', '__httpns_dataone_orgservicetypesv1_Session_subjectInfo', False)

    
    subjectInfo = property(__subjectInfo.value, __subjectInfo.set, None, None)

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Session_subject', False)

    
    subject = property(__subject.value, __subject.set, None, None)


    _ElementMap = {
        __subjectInfo.name() : __subjectInfo,
        __subject.name() : __subject
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Session', Session)


# Complex type Node with content type ELEMENT_ONLY
class Node (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Node')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__httpns_dataone_orgservicetypesv1_Node_description', False)

    
    description = property(__description.value, __description.set, None, u'Description of a Node, explaining the community it\n          serves and other relevant information about the node, such as what\n          content is maintained by this node and any other free style notes.\n          ')

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Node_subject', True)

    
    subject = property(__subject.value, __subject.set, None, u'The :term:`Subject` of this node, which can be\n          repeated as needed. The *Node.subject* represents the identifier of\n          the node that would be found in X.509 certificates used to securely\n          communicate with this node. Thus, it is an :term:`X.509\n          Distinguished Name` that applies to the host on which the Node is\n          operating. When (and if) this hostname changes the new subject for\n          the node would be added to the Node to track the subject that has\n          been used in various access control rules over time.\n          ')

    
    # Element contactSubject uses Python identifier contactSubject
    __contactSubject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'contactSubject'), 'contactSubject', '__httpns_dataone_orgservicetypesv1_Node_contactSubject', True)

    
    contactSubject = property(__contactSubject.value, __contactSubject.set, None, u'The appropriate person or group to contact\n          regarding the disposition, management, and status of this Member\n          Node. The *Node.contactSubject* is an :term:`X.509 Distinguished\n          Name` for a person or group that can be used to look up current\n          contact details (e.g., name, email address) for the contact in the\n          DataONE Identity service. DataONE uses the *contactSubject* to\n          provide notices of interest to DataONE nodes, including information\n          such as policy changes, maintenance updates, node outage\n          notifications, among other information useful for administering a\n          node. Each node that is registered with DataONE must provide at\n          least one *contactSubject* that has been :term:`verified` with\n          DataONE. ')

    
    # Element services uses Python identifier services
    __services = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'services'), 'services', '__httpns_dataone_orgservicetypesv1_Node_services', False)

    
    services = property(__services.value, __services.set, None, u'A list of services that are provided by this node.\n          Used in node descriptions so that nodes can provide metadata about\n          each service they implement and support.')

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'baseURL'), 'baseURL', '__httpns_dataone_orgservicetypesv1_Node_baseURL', False)

    
    baseURL = property(__baseURL.value, __baseURL.set, None, u'The base URL of the node, indicating the\n           protocol, fully qualified domain name, and path to the implementing\n           service, excluding the version of the API. e.g.\n           ``https://server.example.edu/app/d1/mn`` rather than\n           ``https://server.example.edu/app/d1/mn/v1``')

    
    # Element synchronization uses Python identifier synchronization
    __synchronization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'synchronization'), 'synchronization', '__httpns_dataone_orgservicetypesv1_Node_synchronization', False)

    
    synchronization = property(__synchronization.value, __synchronization.set, None, u'Configuration information for the process by which\n            content is harvested from Member Nodes to Coordinating Nodes. This\n            includes the schedule on which harvesting should occur, and metadata\n            about the last synchronization attempts for the\n            node.')

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_Node_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'A unique identifier for the node. Although this\n          may initially be the same as the *baseURL*, such practice is not\n          recommended however as this value MUST NOT change for future\n          implementations of the same node, whereas the *baseURL* may change\n          in the future. ')

    
    # Element nodeReplicationPolicy uses Python identifier nodeReplicationPolicy
    __nodeReplicationPolicy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'nodeReplicationPolicy'), 'nodeReplicationPolicy', '__httpns_dataone_orgservicetypesv1_Node_nodeReplicationPolicy', False)

    
    nodeReplicationPolicy = property(__nodeReplicationPolicy.value, __nodeReplicationPolicy.set, None, u'The replication policy for this node that expresses\n            constraints on object size, total objects, source nodes, and object\n            format types. A node may want to restrict replication from only\n            certain peer nodes, may have file size limits, total allocated size\n            limits, or may want to focus on being a replica target for\n            domain-specific object formats.')

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesv1_Node_name', False)

    
    name = property(__name.value, __name.set, None, u'A human readable name of the Node. This name can\n          be used as a label in many systems to represent the node, and thus\n          should be short, but understandable. ')

    
    # Element ping uses Python identifier ping
    __ping = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ping'), 'ping', '__httpns_dataone_orgservicetypesv1_Node_ping', False)

    
    ping = property(__ping.value, __ping.set, None, u'Stored results from the :func:`MNCore.ping` and\n           :func:`CNCore.ping` methods.')

    
    # Attribute synchronize uses Python identifier synchronize
    __synchronize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'synchronize'), 'synchronize', '__httpns_dataone_orgservicetypesv1_Node_synchronize', pyxb.binding.datatypes.boolean, required=True)
    
    synchronize = property(__synchronize.value, __synchronize.set, None, u'Set to *true* if the node should be\n        :term:`synchronized` by a Coordinating Node, otherwise\n        *false*.')

    
    # Attribute state uses Python identifier state
    __state = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'state'), 'state', '__httpns_dataone_orgservicetypesv1_Node_state', NodeState, required=True)
    
    state = property(__state.value, __state.set, None, u'The state of the node (*up*, *down*), chosen from\n        the :class:`Types.NodeState` type.')

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'type'), 'type', '__httpns_dataone_orgservicetypesv1_Node_type', NodeType, required=True)
    
    type = property(__type.value, __type.set, None, u'The type of the node (Coordinating, Member,\n        Monitor), chosen from the :class:`Types.NodeType`\n        type.')

    
    # Attribute replicate uses Python identifier replicate
    __replicate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'replicate'), 'replicate', '__httpns_dataone_orgservicetypesv1_Node_replicate', pyxb.binding.datatypes.boolean, required=True)
    
    replicate = property(__replicate.value, __replicate.set, None, u'Set to *true* if the node is willing to be a\n        :term:`replication target`, otherwise *false*.')


    _ElementMap = {
        __description.name() : __description,
        __subject.name() : __subject,
        __contactSubject.name() : __contactSubject,
        __services.name() : __services,
        __baseURL.name() : __baseURL,
        __synchronization.name() : __synchronization,
        __identifier.name() : __identifier,
        __nodeReplicationPolicy.name() : __nodeReplicationPolicy,
        __name.name() : __name,
        __ping.name() : __ping
    }
    _AttributeMap = {
        __synchronize.name() : __synchronize,
        __state.name() : __state,
        __type.name() : __type,
        __replicate.name() : __replicate
    }
Namespace.addCategoryObject('typeBinding', u'Node', Node)


# Complex type ChecksumAlgorithmList with content type ELEMENT_ONLY
class ChecksumAlgorithmList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ChecksumAlgorithmList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element algorithm uses Python identifier algorithm
    __algorithm = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'algorithm'), 'algorithm', '__httpns_dataone_orgservicetypesv1_ChecksumAlgorithmList_algorithm', True)

    
    algorithm = property(__algorithm.value, __algorithm.set, None, None)


    _ElementMap = {
        __algorithm.name() : __algorithm
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ChecksumAlgorithmList', ChecksumAlgorithmList)


# Complex type ObjectFormat with content type ELEMENT_ONLY
class ObjectFormat (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectFormat')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element formatType uses Python identifier formatType
    __formatType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'formatType'), 'formatType', '__httpns_dataone_orgservicetypesv1_ObjectFormat_formatType', False)

    
    formatType = property(__formatType.value, __formatType.set, None, u'A string field indicating whether or not this\n          format is :term:`science data` (*DATA*), :term:`science metadata`\n          (*METADATA*) or a :term:`resource map` (*RESOURCE*). If the format\n          is a self-describing data format that includes science metadata,\n          then the field should also be set to science metadata.\n          ')

    
    # Element formatId uses Python identifier formatId
    __formatId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'formatId'), 'formatId', '__httpns_dataone_orgservicetypesv1_ObjectFormat_formatId', False)

    
    formatId = property(__formatId.value, __formatId.set, None, u' The unique identifier of the object format in the\n          DataONE Object Format Vocabulary. The identifier should comply with\n          DataONE Identifier rules, i.e. no whitespace, only UTF-8 or US-ASCII\n          printable characters.')

    
    # Element formatName uses Python identifier formatName
    __formatName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'formatName'), 'formatName', '__httpns_dataone_orgservicetypesv1_ObjectFormat_formatName', False)

    
    formatName = property(__formatName.value, __formatName.set, None, u'For objects that are typed using a Document Type\n          Definition, this lists the well-known and accepted named version of\n          the DTD. In other cases, an appropriately unambiguous descriptive\n          name should be chosen.')


    _ElementMap = {
        __formatType.name() : __formatType,
        __formatId.name() : __formatId,
        __formatName.name() : __formatName
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectFormat', ObjectFormat)


# Complex type ServiceMethodRestriction with content type ELEMENT_ONLY
class ServiceMethodRestriction (SubjectList):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceMethodRestriction')
    # Base type is SubjectList
    
    # Element subject (subject) inherited from {http://ns.dataone.org/service/types/v1}SubjectList
    
    # Attribute methodName uses Python identifier methodName
    __methodName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'methodName'), 'methodName', '__httpns_dataone_orgservicetypesv1_ServiceMethodRestriction_methodName', pyxb.binding.datatypes.string, required=True)
    
    methodName = property(__methodName.value, __methodName.set, None, u'The formal name of the method in this *Service*\n          which is to be restricted.')


    _ElementMap = SubjectList._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = SubjectList._AttributeMap.copy()
    _AttributeMap.update({
        __methodName.name() : __methodName
    })
Namespace.addCategoryObject('typeBinding', u'ServiceMethodRestriction', ServiceMethodRestriction)


log = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'log'), Log)
Namespace.addCategoryObject('elementBinding', log.name().localName(), log)

nodeReference = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'nodeReference'), NodeReference)
Namespace.addCategoryObject('elementBinding', nodeReference.name().localName(), nodeReference)

replica = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'replica'), Replica)
Namespace.addCategoryObject('elementBinding', replica.name().localName(), replica)

services = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'services'), Services)
Namespace.addCategoryObject('elementBinding', services.name().localName(), services)

subjectList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subjectList'), SubjectList)
Namespace.addCategoryObject('elementBinding', subjectList.name().localName(), subjectList)

accessRule = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'accessRule'), AccessRule)
Namespace.addCategoryObject('elementBinding', accessRule.name().localName(), accessRule)

nodeList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'nodeList'), NodeList)
Namespace.addCategoryObject('elementBinding', nodeList.name().localName(), nodeList)

identifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'identifier'), Identifier)
Namespace.addCategoryObject('elementBinding', identifier.name().localName(), identifier)

person = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'person'), Person)
Namespace.addCategoryObject('elementBinding', person.name().localName(), person)

service = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'service'), Service)
Namespace.addCategoryObject('elementBinding', service.name().localName(), service)

subject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subject'), Subject)
Namespace.addCategoryObject('elementBinding', subject.name().localName(), subject)

accessPolicy = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'accessPolicy'), AccessPolicy)
Namespace.addCategoryObject('elementBinding', accessPolicy.name().localName(), accessPolicy)

objectList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectList'), ObjectList)
Namespace.addCategoryObject('elementBinding', objectList.name().localName(), objectList)

objectLocationList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectLocationList'), ObjectLocationList)
Namespace.addCategoryObject('elementBinding', objectLocationList.name().localName(), objectLocationList)

group = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'group'), Group)
Namespace.addCategoryObject('elementBinding', group.name().localName(), group)

objectInfo = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectInfo'), ObjectInfo)
Namespace.addCategoryObject('elementBinding', objectInfo.name().localName(), objectInfo)

systemMetadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'systemMetadata'), SystemMetadata)
Namespace.addCategoryObject('elementBinding', systemMetadata.name().localName(), systemMetadata)

objectFormatList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectFormatList'), ObjectFormatList)
Namespace.addCategoryObject('elementBinding', objectFormatList.name().localName(), objectFormatList)

session = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'session'), Session)
Namespace.addCategoryObject('elementBinding', session.name().localName(), session)

checksum = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'checksum'), Checksum)
Namespace.addCategoryObject('elementBinding', checksum.name().localName(), checksum)

synchronization = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'synchronization'), Synchronization)
Namespace.addCategoryObject('elementBinding', synchronization.name().localName(), synchronization)

node = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'node'), Node)
Namespace.addCategoryObject('elementBinding', node.name().localName(), node)

checksumAlgorithmList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'checksumAlgorithmList'), ChecksumAlgorithmList)
Namespace.addCategoryObject('elementBinding', checksumAlgorithmList.name().localName(), checksumAlgorithmList)

objectFormat = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectFormat'), ObjectFormat)
Namespace.addCategoryObject('elementBinding', objectFormat.name().localName(), objectFormat)

replicationPolicy = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'replicationPolicy'), ReplicationPolicy)
Namespace.addCategoryObject('elementBinding', replicationPolicy.name().localName(), replicationPolicy)

serviceMethodRestriction = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'serviceMethodRestriction'), ServiceMethodRestriction)
Namespace.addCategoryObject('elementBinding', serviceMethodRestriction.name().localName(), serviceMethodRestriction)

logEntry = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'logEntry'), LogEntry)
Namespace.addCategoryObject('elementBinding', logEntry.name().localName(), logEntry)

schedule = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'schedule'), Schedule)
Namespace.addCategoryObject('elementBinding', schedule.name().localName(), schedule)

subjectInfo = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subjectInfo'), SubjectInfo)
Namespace.addCategoryObject('elementBinding', subjectInfo.name().localName(), subjectInfo)

nodeReplicationPolicy = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'nodeReplicationPolicy'), NodeReplicationPolicy)
Namespace.addCategoryObject('elementBinding', nodeReplicationPolicy.name().localName(), nodeReplicationPolicy)



Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation=u'The last time (UTC) all the data from a node was\n          pulled from a member node during a complete synchronization\n          process.'))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'schedule'), Schedule, scope=Synchronization, documentation=u'An entry set by the Member Node indicating the\n          frequency for which synchronization should occur. This setting will\n          be influenced by the frequency with which content is updated on the\n          Member Node and the acceptable latency for detection and subsequent\n          processing of new content.'))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastHarvested'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation=u'The most recent modification date (UTC) of objects\n          checked during the last harvest of the node.'))
Synchronization._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'schedule')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastHarvested')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest')), min_occurs=0L, max_occurs=1L)
    )
Synchronization._ContentModel = pyxb.binding.content.ParticleModel(Synchronization._GroupModel, min_occurs=1, max_occurs=1)



LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=LogEntry, documentation=u'The :term:`identifier` of the object that was the\n          target of the operation which generated this log entry.'))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'entryId'), NonEmptyString, scope=LogEntry, documentation=u'A unique identifier for this log entry. The\n          identifier should be unique for a particular node; This is not drawn\n          from the same value space as other identifiers in DataONE, and so is\n          not subjec to the same restrictions.'))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateLogged'), pyxb.binding.datatypes.dateTime, scope=LogEntry, documentation=u'A :class:`Types.DateTime` time stamp indicating when\n          the event triggering the log message ocurred. Note that all time\n          stamps in DataONE are in UTC.'))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), NodeReference, scope=LogEntry, documentation=u'The unique identifier for the node where the log\n          message was generated.'))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ipAddress'), pyxb.binding.datatypes.string, scope=LogEntry, documentation=u'The IP address, as reported by the service receiving\n          the request, of the request origin.'))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'event'), Event, scope=LogEntry, documentation=u'An entry from the :class:`Types.Event` enumeration\n          indicating the type of operation that triggered the log message.'))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'userAgent'), pyxb.binding.datatypes.string, scope=LogEntry, documentation=u'The user agent of the client making the request, as\n          reported in the User-Agent HTTP header.'))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=LogEntry, documentation=u'The :term:`Subject` used for making the request.\n          This may be the DataONE :term:`public` user if the request is not\n          authenticated, otherwise it will be the *Subject* of the certificate\n          used for authenticating the request.'))
LogEntry._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'entryId')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'ipAddress')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'userAgent')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'event')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'dateLogged')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'nodeIdentifier')), min_occurs=1L, max_occurs=1L)
    )
LogEntry._ContentModel = pyxb.binding.content.ParticleModel(LogEntry._GroupModel, min_occurs=1, max_occurs=1)



Log._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'logEntry'), LogEntry, scope=Log))
Log._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Log._UseForTag(pyxb.namespace.ExpandedName(None, u'logEntry')), min_occurs=0L, max_occurs=None)
    )
Log._ContentModel = pyxb.binding.content.ParticleModel(Log._GroupModel, min_occurs=1, max_occurs=1)



Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicaVerified'), pyxb.binding.datatypes.dateTime, scope=Replica, documentation=u' The last date and time on which the integrity of\n          a replica was verified by the coordinating node. Verification occurs\n          by checking that the checksum of the stored object matches the\n          checksum recorded for the object in the system\n          metadata.'))

Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicaMemberNode'), NodeReference, scope=Replica, documentation=u'A reference to the Member Node that houses this\n          replica, regardless of whether it has arrived at the Member Node or\n          not. See *replicationStatus* to determine if the replica is\n          completely transferred. '))

Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicationStatus'), ReplicationStatus, scope=Replica, documentation=u' The current status of this replica, indicating\n          the stage of replication process for the object. Only *completed*\n          replicas should be considered as available. '))
Replica._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicaMemberNode')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicationStatus')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicaVerified')), min_occurs=1, max_occurs=1)
    )
Replica._ContentModel = pyxb.binding.content.ParticleModel(Replica._GroupModel, min_occurs=1, max_occurs=1)



AccessRule._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'permission'), Permission, scope=AccessRule))

AccessRule._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=AccessRule))
AccessRule._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AccessRule._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AccessRule._UseForTag(pyxb.namespace.ExpandedName(None, u'permission')), min_occurs=1L, max_occurs=None)
    )
AccessRule._ContentModel = pyxb.binding.content.ParticleModel(AccessRule._GroupModel, min_occurs=1, max_occurs=1)



Services._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'service'), Service, scope=Services))
Services._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Services._UseForTag(pyxb.namespace.ExpandedName(None, u'service')), min_occurs=1L, max_occurs=None)
    )
Services._ContentModel = pyxb.binding.content.ParticleModel(Services._GroupModel, min_occurs=1, max_occurs=1)



SubjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=SubjectList))
SubjectList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SubjectList._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=0L, max_occurs=None)
    )
SubjectList._ContentModel = pyxb.binding.content.ParticleModel(SubjectList._GroupModel, min_occurs=1, max_occurs=1)



ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'blockedMemberNode'), NodeReference, scope=ReplicationPolicy, documentation=u'The object MUST never be replicated to nodes\n          listed as *blockedMemberNodes*. Where there is a conflict between a\n          *preferredMemberNode* and a *blockedMemberNode* entry, the\n          *blockedMemberNode* entry prevails. '))

ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'preferredMemberNode'), NodeReference, scope=ReplicationPolicy, documentation=u'Preferred Nodes are utilized over other nodes as\n          replication targets, up to the number of replicas requested. If\n          preferred nodes are unavailable, or if insufficient nodes are listed\n          as preferred to meet the requested number of replicas, then the\n          Coordinating Nodes will pick additional replica nodes for the\n          content. '))
ReplicationPolicy._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'preferredMemberNode')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'blockedMemberNode')), min_occurs=0L, max_occurs=None)
    )
ReplicationPolicy._ContentModel = pyxb.binding.content.ParticleModel(ReplicationPolicy._GroupModel, min_occurs=1, max_occurs=1)



Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'familyName'), NonEmptyString, scope=Person, documentation=u'The family name of the *Person*.'))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'isMemberOf'), Subject, scope=Person, documentation=u'A *group* or role in which the *Person* is a member,\n          expressed using the unique :class:`Types.Subject` identifier for\n          that :class:`Types.Group`, and repeatable if they are a member of\n          more than one group. '))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'email'), NonEmptyString, scope=Person, documentation=u'The email address of the *Person*, repeatable if\n          they have more than one email address. '))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'equivalentIdentity'), Subject, scope=Person, documentation=u'An alternative but equivalent identity for the\n          :term:`principal` that has been used in alternate identity systems,\n          repeatable if more than one equivalent identity applies.\n          '))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Person, documentation=u'The unique, immutable identifier for the\n          *Person*.'))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'verified'), pyxb.binding.datatypes.boolean, scope=Person, documentation=u"*true* if the name and email address of the\n          *Person* have been :term:`verified` to ensure that the *givenName*\n          and *familyName* represent the real person's legal name, and that\n          the email address is correct for that person and is in the control\n          of the indicated individual. Verification occurs through an\n          established procedure within DataONE as part of the Identity\n          Management system. A Person can not change their own *verified*\n          field, but rather must be verified and changed through this DataONE\n          established process. "))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'givenName'), NonEmptyString, scope=Person, documentation=u'The given name of the *Person*, repeatable if they\n          have more than one given name.'))
Person._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'givenName')), min_occurs=1L, max_occurs=None),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'familyName')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'email')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'isMemberOf')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'equivalentIdentity')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'verified')), min_occurs=0L, max_occurs=1L)
    )
Person._ContentModel = pyxb.binding.content.ParticleModel(Person._GroupModel, min_occurs=1, max_occurs=1)



NodeReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'allowedObjectFormat'), ObjectFormatIdentifier, scope=NodeReplicationPolicy, documentation=u'An optional, repeatable statement of an object\n          format that this node is willing to replicate, expressed as a\n          :class:`Types.ObjectFormatIdentifier`.'))

NodeReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'maxObjectSize'), pyxb.binding.datatypes.unsignedLong, scope=NodeReplicationPolicy, documentation=u'An optional statement of the maximum size in octets \n          (8-bit bytes) of objects this node is willing to accept for\n          replication.'))

NodeReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'allowedNode'), NodeReference, scope=NodeReplicationPolicy, documentation=u'An optional, repeatable statement of a peer source\n          node from which this node is willing to replicate content, expressed\n          as a :class:`Types.NodeReference`.'))

NodeReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'spaceAllocated'), pyxb.binding.datatypes.unsignedLong, scope=NodeReplicationPolicy, documentation=u'An optional statement of the total space in bytes\n          allocated for replication object storage on this\n          node.'))
NodeReplicationPolicy._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NodeReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'maxObjectSize')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(NodeReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'spaceAllocated')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(NodeReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'allowedNode')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(NodeReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'allowedObjectFormat')), min_occurs=0L, max_occurs=None)
    )
NodeReplicationPolicy._ContentModel = pyxb.binding.content.ParticleModel(NodeReplicationPolicy._GroupModel, min_occurs=1, max_occurs=1)



Service._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'restriction'), ServiceMethodRestriction, scope=Service, documentation=u'A list of method names and :term:`Subjects` with\n          permission to invoke those methods.'))
Service._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Service._UseForTag(pyxb.namespace.ExpandedName(None, u'restriction')), min_occurs=0L, max_occurs=None)
    )
Service._ContentModel = pyxb.binding.content.ParticleModel(Service._GroupModel, min_occurs=1, max_occurs=1)



ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'size'), pyxb.binding.datatypes.unsignedLong, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'checksum'), Checksum, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'formatId'), ObjectFormatIdentifier, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=ObjectInfo))
ObjectInfo._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'formatId')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'checksum')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'size')), min_occurs=1, max_occurs=1)
    )
ObjectInfo._ContentModel = pyxb.binding.content.ParticleModel(ObjectInfo._GroupModel, min_occurs=1, max_occurs=1)



NodeList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'node'), Node, scope=NodeList))
NodeList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NodeList._UseForTag(pyxb.namespace.ExpandedName(None, u'node')), min_occurs=1L, max_occurs=None)
    )
NodeList._ContentModel = pyxb.binding.content.ParticleModel(NodeList._GroupModel, min_occurs=1, max_occurs=1)



SubjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'group'), Group, scope=SubjectInfo))

SubjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'person'), Person, scope=SubjectInfo))
SubjectInfo._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SubjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'person')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SubjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'group')), min_occurs=0L, max_occurs=None)
    )
SubjectInfo._ContentModel = pyxb.binding.content.ParticleModel(SubjectInfo._GroupModel, min_occurs=1, max_occurs=1)



ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'preference'), pyxb.binding.datatypes.int, scope=ObjectLocation, documentation=u'A weighting parameter that provides a hint to the\n          caller for the relative preference for nodes from which the content\n          should be retrieved. Higher values have higher preference.\n          '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), NodeReference, scope=ObjectLocation, documentation=u'Identifier of the :class:`Types.Node` (the same\n          identifier used in the node registry for identifying the node).\n          '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'url'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation=u'The full (absolute) URL that can be used to\n          retrieve the object using the get() method of the rest\n          interface.For example, if identifier was "ABX154", and the\n          node had a base URL of ``http://mn1.dataone.org/mn`` then the value\n          would be \n          ``http://mn1.dataone.org/mn/v1/object/ABX154``'))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'version'), ServiceVersion, scope=ObjectLocation, documentation=u'The version of services implemented on the node.\n          Used with base url to construct a URL for service calls to this\n          node. Note that complete information on services available on a Node\n          is available from the :func:`CNCore.listNodes` service.\n          '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation=u'The current base URL (the *baseURL* element from\n          the :class:`Types.Node` record) for services implemented on the\n          target node. Used with service version to construct a URL for\n          service calls to this node. Note that complete information on\n          services available on a Node is available from the\n          :func:`CNCore.listNodes` service. '))
ObjectLocation._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'nodeIdentifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'baseURL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'version')), min_occurs=1L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'url')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'preference')), min_occurs=0L, max_occurs=1L)
    )
ObjectLocation._ContentModel = pyxb.binding.content.ParticleModel(ObjectLocation._GroupModel, min_occurs=1, max_occurs=1)



AccessPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'allow'), AccessRule, scope=AccessPolicy))
AccessPolicy._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AccessPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'allow')), min_occurs=1L, max_occurs=None)
    )
AccessPolicy._ContentModel = pyxb.binding.content.ParticleModel(AccessPolicy._GroupModel, min_occurs=1, max_occurs=1)



ObjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectInfo'), ObjectInfo, scope=ObjectList))
ObjectList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectInfo')), min_occurs=0L, max_occurs=None)
    )
ObjectList._ContentModel = pyxb.binding.content.ParticleModel(ObjectList._GroupModel, min_occurs=1, max_occurs=1)



ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectLocation'), ObjectLocation, scope=ObjectLocationList, documentation=u'List of nodes from which the object can be\n        retrieved'))

ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=ObjectLocationList, documentation=u'The :term:`identifier` of the object being\n        resolved.'))
ObjectLocationList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectLocation')), min_occurs=0L, max_occurs=None)
    )
ObjectLocationList._ContentModel = pyxb.binding.content.ParticleModel(ObjectLocationList._GroupModel, min_occurs=1, max_occurs=1)



Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'rightsHolder'), Subject, scope=Group, documentation=u'Represents the list of owners of this :term:`group`.\n        All groups are readable by anyone in the DataONE system, but can only\n        be modified by subjects listed in *rightsHolder* fields. Designation\n        as a :term:`rightsHolder` allows the subject, or their equivalent\n        identities, to make changes to the mutable properties of the group,\n        including its name, membership list and rights holder list. The\n        subject of the group itself is immutable. '))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Group, documentation=u'The unique, immutable identifier of the\n          :term:`group`. Group subjects must not be reused, and so they are\n          both immutable and can not be deleted from the DataONE\n          system.'))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'groupName'), NonEmptyString, scope=Group, documentation=u'The name of the Group.'))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'hasMember'), Subject, scope=Group, documentation=u'A :term:`Subject` that is a member of this\n            group, expressed using the unique identifier for that\n            Subject.'))
Group._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Group._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Group._UseForTag(pyxb.namespace.ExpandedName(None, u'groupName')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Group._UseForTag(pyxb.namespace.ExpandedName(None, u'hasMember')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(Group._UseForTag(pyxb.namespace.ExpandedName(None, u'rightsHolder')), min_occurs=1L, max_occurs=None)
    )
Group._ContentModel = pyxb.binding.content.ParticleModel(Group._GroupModel, min_occurs=1, max_occurs=1)



SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'obsoletes'), Identifier, scope=SystemMetadata, documentation=u'The :term:`Identifier` of an object that is a\n          prior version of the object described in this system metadata record\n          and that is obsoleted by this object. When an object is obsoleted,\n          it is removed from all DataONE search indices but is still\n          accessible from the :func:`CNRead.get` service. '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode'), NodeReference, scope=SystemMetadata, documentation=u' A reference to the Member Node that acts as the\n          authoritative source for an object in the system. The\n          *authoritativeMemberNode* will often also be the *originMemberNode*,\n          unless there has been a need to transfer authority for an object to\n          a new node, such as when a Member Node becomes defunct. The\n          *authoritativeMemberNode* has all the rights of the *rightsHolder*\n          to maintain and curate the object, including making any changes\n          necessary. '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'checksum'), Checksum, scope=SystemMetadata, documentation=u' A calculated hash value used to validate object\n          integrity over time and after network transfers. The value is\n          calculated using a standard hashing algorithm that is accepted by\n          DataONE and that is indicated in the included *ChecksumAlgorithm*\n          attribute. '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'submitter'), Subject, scope=SystemMetadata, documentation=u':term:`Subject` who submitted the associated\n          abject to the DataONE Member Node. The Member Node must set this\n          field when it receives the system metadata document from a client\n          (the field is optional from the client perspective, but is required\n          when a MN creates an object). By default, the submitter lacks any\n          rights to modify an object, so care must be taken to set\n          *rightsHolder* and *accessPolicy* correctly with a reference to the\n          subject of the submitter if the submitter is to be able to make\n          further changes to the object.'))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'obsoletedBy'), Identifier, scope=SystemMetadata, documentation=u'The :term:`Identifier` of an object that is a\n          subsequent version of the object described in this system metadata\n          record and that therefore obsoletes this object. When an object is\n          obsoleted, it is removed from all DataONE search indices but is\n          still accessible from the :func:`CNRead.get` service.\n          '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'serialVersion'), pyxb.binding.datatypes.unsignedLong, scope=SystemMetadata, documentation=u' A serial number maintained by the coordinating node\n            to indicate when changes have occurred to *SystemMetadata* to avoid\n            update conflicts. Clients should ensure that they have the most\n            recent version of a *SystemMetadata* document before attempting to\n            update, otherwise an error will be thrown to prevent conflicts. The\n            Coordinating Node must set this optional field when it receives the\n            system metadata document. '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replica'), Replica, scope=SystemMetadata, documentation=u' A container field used to repeatedly provide\n          several metadata fields about each replica that exists in the\n          system, or is being replicated. Note that a *replica* field exists\n          even for the Authoritative/Origin Member Nodes so that the status of\n          those objects can be tracked. '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'archived'), pyxb.binding.datatypes.boolean, scope=SystemMetadata, documentation=u'A boolean flag, set to *true* if the object has\n          been classified as archived. An archived object does not show up in\n          search indexes in DataONE, but is still accessible via the CNRead\n          and MNRead services if associated access polices allow. The field is\n          optional, and if absent, then objects are implied to not be\n          archived, which is the same as setting archived to\n          *false*.'))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'originMemberNode'), NodeReference, scope=SystemMetadata, documentation=u'A reference to the Member Node that originally\n          uploaded the associated object. This value should never change, even\n          if the Member Node ceases to exist. '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'rightsHolder'), Subject, scope=SystemMetadata, documentation=u':term:`Subject` that has ultimate authority for\n          the object and is authorized to make all decisions regarding the\n          disposition and accessibility of the object. The *rightsHolder* has\n          all rights to access the object, update the object, and grant\n          permissions for the object, even if additional access control rules\n          are not specified for the object. Typically, the *rightsHolder*\n          field would be set to the name of the subject submitting an object,\n          so that the person can make further changes later. By default, the\n          *submitter* lacks any rights to modify an object, so care must be\n          taken to set *rightsHolder* and *accessPolicy* correctly with a\n          reference to the subject of the *submitter* if the *submitter* is to\n          be able to make further changes to the object. '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicationPolicy'), ReplicationPolicy, scope=SystemMetadata, documentation=u'A controlled list of policy choices that determine\n          how many replicas should be maintained for a given object and any\n          preferences or requirements as to which Member Nodes should be\n          allowed to house the replicas. The policy determines whether\n          replication is allowed, the number of replicas desired, the list of\n          preferred nodes to hold the replicas, and a list of blocked nodes on\n          which replicas must not exist.'))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateUploaded'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata, documentation=u'Date and time (UTC) that the object was uploaded\n          into the DataONE system, which is typically the time that the object\n          is first created on a Member Node using the :func:`MNStorage.create`\n          operation. Note this is independent of the publication or release\n          date of the object. The Member Node must set this optional field\n          when it receives the system metadata document from a\n          client.'))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'formatId'), ObjectFormatIdentifier, scope=SystemMetadata, documentation=u' Designation of the standard or format that should\n          be used to interpret the contents of the object, drawn from\n          controlled list of formats that are provided by the DataONE\n          :class:`Types.ObjectFormat` service. DataONE maintains a list of\n          formats in use and their canonical FormatIdentifiers. The format\n          identifier for an object should imply its mime type for data objects\n          and metadata type and serialization format for metadata objects.\n          Examples include the namespace of the EML 2.1 metadata\n          specification, the DOCTYPE of the Biological Data Profile, the mime\n          type of ``text/csv`` files, and the canonical name of the NetCDF\n          specification. '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata, documentation=u' Date and time (UTC) that this system metadata\n          record was last modified in the DataONE system. This is the same\n          timestamp as *dateUploaded* until the system metadata is further\n          modified. The Member Node must set this optional field when it\n          receives the system metadata document from a\n          client.'))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=SystemMetadata, documentation=u'The :term:`identifier` is a unique Unicode string\n          that is used to canonically name and identify the object in DataONE.\n          Each object in DataONE is immutable, and therefore all objects must\n          have a unique Identifier. If two objects are related to one another\n          (such as one object is a more recent version of another object),\n          each of these two objects will have unique identifiers. The\n          relationship among the objects is specified in other metadata fields\n          (see *Obsoletes* and *ObsoletedBy*), but this does not preclude the\n          inclusion of version information in the identifier string. However,\n          DataONE treats all Identifiers as opaque and will not try to infer\n          versioning semantics based on the content of the Identifiers --\n          rather, this information is found in the *Obsoletes* and\n          *ObsoletedBy* fields. Note that identifiers are used in a number of\n          REST API calls as parts of the URL path. As such, all special\n          characters such as "/", " ", "+", "\\", "%" must be properly encoded,\n          e.g. "%2F", "%20", "%2B", "%5C", "%25" respectively when used in\n          REST method calls. See RFC3896_ for more details. For example, the\n          :func:`MNRead.get()` call for an object with identifier:``http://some.location.name/mydata.cgi?id=2088``would be:``http://mn1.server.name/mn/v1/object/http:%2F%2Fsome.location.name%2Fmydata.cgi%3Fid%3D2088``.. _RFC3896: http://www.ietf.org/rfc/rfc3896.txt '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'size'), pyxb.binding.datatypes.unsignedLong, scope=SystemMetadata, documentation=u' The size of the object in octets (8-bit bytes).\n          '))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'accessPolicy'), AccessPolicy, scope=SystemMetadata, documentation=u'The *accessPolicy* determines which\n          :term:`Subjects` are allowed to make changes to an object in\n          addition to the *rightsHolder* and *authoritativeMemberNode*. The\n          *accessPolicy* is set for an object during a\n          :func:`MNStorage.create` or :func:`MNStorage.update` call, or when\n          *SystemMetadata* is updated on the Coordinating Node via various\n          mechanisms. This policy replaces any existing policies that might\n          exist for the object. Member Nodes that house an object are\n          obligated to enforce the *accessPolicy* for that\n          object.'))
SystemMetadata._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'serialVersion')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'formatId')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'size')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'checksum')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'submitter')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'rightsHolder')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'accessPolicy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'replicationPolicy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'obsoletes')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'obsoletedBy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'archived')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'dateUploaded')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'originMemberNode')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'replica')), min_occurs=0L, max_occurs=None)
    )
SystemMetadata._ContentModel = pyxb.binding.content.ParticleModel(SystemMetadata._GroupModel, min_occurs=1, max_occurs=1)



ObjectFormatList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectFormat'), ObjectFormat, scope=ObjectFormatList))
ObjectFormatList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectFormatList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectFormat')), min_occurs=1L, max_occurs=None)
    )
ObjectFormatList._ContentModel = pyxb.binding.content.ParticleModel(ObjectFormatList._GroupModel, min_occurs=1, max_occurs=1)



Session._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subjectInfo'), SubjectInfo, scope=Session))

Session._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Session))
Session._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Session._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Session._UseForTag(pyxb.namespace.ExpandedName(None, u'subjectInfo')), min_occurs=0L, max_occurs=1L)
    )
Session._ContentModel = pyxb.binding.content.ParticleModel(Session._GroupModel, min_occurs=1, max_occurs=1)



Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'description'), NonEmptyString, scope=Node, documentation=u'Description of a Node, explaining the community it\n          serves and other relevant information about the node, such as what\n          content is maintained by this node and any other free style notes.\n          '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Node, documentation=u'The :term:`Subject` of this node, which can be\n          repeated as needed. The *Node.subject* represents the identifier of\n          the node that would be found in X.509 certificates used to securely\n          communicate with this node. Thus, it is an :term:`X.509\n          Distinguished Name` that applies to the host on which the Node is\n          operating. When (and if) this hostname changes the new subject for\n          the node would be added to the Node to track the subject that has\n          been used in various access control rules over time.\n          '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'contactSubject'), Subject, scope=Node, documentation=u'The appropriate person or group to contact\n          regarding the disposition, management, and status of this Member\n          Node. The *Node.contactSubject* is an :term:`X.509 Distinguished\n          Name` for a person or group that can be used to look up current\n          contact details (e.g., name, email address) for the contact in the\n          DataONE Identity service. DataONE uses the *contactSubject* to\n          provide notices of interest to DataONE nodes, including information\n          such as policy changes, maintenance updates, node outage\n          notifications, among other information useful for administering a\n          node. Each node that is registered with DataONE must provide at\n          least one *contactSubject* that has been :term:`verified` with\n          DataONE. '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'services'), Services, scope=Node, documentation=u'A list of services that are provided by this node.\n          Used in node descriptions so that nodes can provide metadata about\n          each service they implement and support.'))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=Node, documentation=u'The base URL of the node, indicating the\n           protocol, fully qualified domain name, and path to the implementing\n           service, excluding the version of the API. e.g.\n           ``https://server.example.edu/app/d1/mn`` rather than\n           ``https://server.example.edu/app/d1/mn/v1``'))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'synchronization'), Synchronization, scope=Node, documentation=u'Configuration information for the process by which\n            content is harvested from Member Nodes to Coordinating Nodes. This\n            includes the schedule on which harvesting should occur, and metadata\n            about the last synchronization attempts for the\n            node.'))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), NodeReference, scope=Node, documentation=u'A unique identifier for the node. Although this\n          may initially be the same as the *baseURL*, such practice is not\n          recommended however as this value MUST NOT change for future\n          implementations of the same node, whereas the *baseURL* may change\n          in the future. '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'nodeReplicationPolicy'), NodeReplicationPolicy, scope=Node, documentation=u'The replication policy for this node that expresses\n            constraints on object size, total objects, source nodes, and object\n            format types. A node may want to restrict replication from only\n            certain peer nodes, may have file size limits, total allocated size\n            limits, or may want to focus on being a replica target for\n            domain-specific object formats.'))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), NonEmptyString, scope=Node, documentation=u'A human readable name of the Node. This name can\n          be used as a label in many systems to represent the node, and thus\n          should be short, but understandable. '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ping'), Ping, scope=Node, documentation=u'Stored results from the :func:`MNCore.ping` and\n           :func:`CNCore.ping` methods.'))
Node._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'name')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'description')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'baseURL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'services')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'synchronization')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'nodeReplicationPolicy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'ping')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'contactSubject')), min_occurs=1L, max_occurs=None)
    )
Node._ContentModel = pyxb.binding.content.ParticleModel(Node._GroupModel, min_occurs=1, max_occurs=1)



ChecksumAlgorithmList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'algorithm'), ChecksumAlgorithm, scope=ChecksumAlgorithmList))
ChecksumAlgorithmList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ChecksumAlgorithmList._UseForTag(pyxb.namespace.ExpandedName(None, u'algorithm')), min_occurs=1L, max_occurs=None)
    )
ChecksumAlgorithmList._ContentModel = pyxb.binding.content.ParticleModel(ChecksumAlgorithmList._GroupModel, min_occurs=1, max_occurs=1)



ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'formatType'), pyxb.binding.datatypes.string, scope=ObjectFormat, documentation=u'A string field indicating whether or not this\n          format is :term:`science data` (*DATA*), :term:`science metadata`\n          (*METADATA*) or a :term:`resource map` (*RESOURCE*). If the format\n          is a self-describing data format that includes science metadata,\n          then the field should also be set to science metadata.\n          '))

ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'formatId'), ObjectFormatIdentifier, scope=ObjectFormat, documentation=u' The unique identifier of the object format in the\n          DataONE Object Format Vocabulary. The identifier should comply with\n          DataONE Identifier rules, i.e. no whitespace, only UTF-8 or US-ASCII\n          printable characters.'))

ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'formatName'), pyxb.binding.datatypes.string, scope=ObjectFormat, documentation=u'For objects that are typed using a Document Type\n          Definition, this lists the well-known and accepted named version of\n          the DTD. In other cases, an appropriately unambiguous descriptive\n          name should be chosen.'))
ObjectFormat._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, u'formatId')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, u'formatName')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, u'formatType')), min_occurs=1L, max_occurs=1L)
    )
ObjectFormat._ContentModel = pyxb.binding.content.ParticleModel(ObjectFormat._GroupModel, min_occurs=1, max_occurs=1)


ServiceMethodRestriction._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ServiceMethodRestriction._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=0L, max_occurs=None)
    )
ServiceMethodRestriction._ContentModel = pyxb.binding.content.ParticleModel(ServiceMethodRestriction._GroupModel, min_occurs=1, max_occurs=1)
