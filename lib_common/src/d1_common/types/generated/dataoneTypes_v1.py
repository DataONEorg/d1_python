# ./d1_common/types/generated/dataoneTypes_v1.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:b5056e9f5bcbaa65eac428b50fd841172c48ddf9
# Generated 2017-10-17 10:39:46.192050 by PyXB version 1.2.6 using Python 2.7.12.final.0
# Namespace http://ns.dataone.org/service/types/v1


import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:c8cebbca-b359-11e7-b444-080027018ba0')

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

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://ns.dataone.org/service/types/v1', create_if_missing=True)
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


# Atomic simple type: {http://ns.dataone.org/service/types/v1}ChecksumAlgorithm
class ChecksumAlgorithm (pyxb.binding.datatypes.string):

    """The cryptographic hash algorithm used to calculate a
      checksum. DataONE recognizes the Library of Congress list of
      cryptographic hash algorithms that can be used as names in this field,
      and specifically uses the *madsrdf:authoritativeLabel* field as the name
      of the algorithm in this field. See: `Library of Congress Cryptographic
      Algorithm Vocabulary`_. All compliant implementations must support at
      least SHA-1 and MD5, but may support other algorithms as well.Valid entries include: SHA-1, MD5The default checksum is *SHA-1*... _Library of Congress Cryptographic Algorithm Vocabulary: http://id.loc.gov/vocabulary/cryptographicHashFunctions.rdf
      """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ChecksumAlgorithm')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 59, 2)
    _Documentation = 'The cryptographic hash algorithm used to calculate a\n      checksum. DataONE recognizes the Library of Congress list of\n      cryptographic hash algorithms that can be used as names in this field,\n      and specifically uses the *madsrdf:authoritativeLabel* field as the name\n      of the algorithm in this field. See: `Library of Congress Cryptographic\n      Algorithm Vocabulary`_. All compliant implementations must support at\n      least SHA-1 and MD5, but may support other algorithms as well.Valid entries include: SHA-1, MD5The default checksum is *SHA-1*... _Library of Congress Cryptographic Algorithm Vocabulary: http://id.loc.gov/vocabulary/cryptographicHashFunctions.rdf\n      '
ChecksumAlgorithm._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ChecksumAlgorithm', ChecksumAlgorithm)
_module_typeBindings.ChecksumAlgorithm = ChecksumAlgorithm

# Atomic simple type: {http://ns.dataone.org/service/types/v1}CrontabEntry
class CrontabEntry (pyxb.binding.datatypes.token):

    """A single value in the series of values that together
      form a single crontab entry. The format follows the syntax conventions
      defined by the `Quartz Scheduler`_, as excerpted here under the Apache 2 license:.. _Quartz Scheduler: http://www.quartz-scheduler.org/api/2.1.0/org/quartz/CronExpression.html.. include:: Types_crontabentry.txt"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CrontabEntry')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 78, 2)
    _Documentation = 'A single value in the series of values that together\n      form a single crontab entry. The format follows the syntax conventions\n      defined by the `Quartz Scheduler`_, as excerpted here under the Apache 2 license:.. _Quartz Scheduler: http://www.quartz-scheduler.org/api/2.1.0/org/quartz/CronExpression.html.. include:: Types_crontabentry.txt'
CrontabEntry._CF_pattern = pyxb.binding.facets.CF_pattern()
CrontabEntry._CF_pattern.addPattern(pattern='([\\?\\*\\d/#,\\-a-zA-Z])+')
CrontabEntry._InitializeFacetMap(CrontabEntry._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'CrontabEntry', CrontabEntry)
_module_typeBindings.CrontabEntry = CrontabEntry

# Atomic simple type: {http://ns.dataone.org/service/types/v1}CrontabEntrySeconds
class CrontabEntrySeconds (pyxb.binding.datatypes.token):

    """A restriction on the seconds field in a single
      Schedule entry, following the syntax conventions defined by the `Quartz
      Scheduler`_.The wildcard character value is not allowed in this
      (seconds) field as this would create an impractical synchronization
      schedule.. _Quartz Scheduler: http://www.quartz-scheduler.org/api/2.1.0/org/quartz/CronExpression.html"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CrontabEntrySeconds')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 90, 2)
    _Documentation = 'A restriction on the seconds field in a single\n      Schedule entry, following the syntax conventions defined by the `Quartz\n      Scheduler`_.The wildcard character value is not allowed in this\n      (seconds) field as this would create an impractical synchronization\n      schedule.. _Quartz Scheduler: http://www.quartz-scheduler.org/api/2.1.0/org/quartz/CronExpression.html'
CrontabEntrySeconds._CF_pattern = pyxb.binding.facets.CF_pattern()
CrontabEntrySeconds._CF_pattern.addPattern(pattern='[0-5]?\\d')
CrontabEntrySeconds._InitializeFacetMap(CrontabEntrySeconds._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'CrontabEntrySeconds', CrontabEntrySeconds)
_module_typeBindings.CrontabEntrySeconds = CrontabEntrySeconds

# Atomic simple type: {http://ns.dataone.org/service/types/v1}Event
class Event (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """The controlled list of events that are logged, which
      will include *create*, *update*, *delete*, *read*, *replicate*,
      *synchronization_failed* and *replication_failed*
      events."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Event')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 106, 2)
    _Documentation = 'The controlled list of events that are logged, which\n      will include *create*, *update*, *delete*, *read*, *replicate*,\n      *synchronization_failed* and *replication_failed*\n      events.'
Event._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Event, enum_prefix=None)
Event.create = Event._CF_enumeration.addEnumeration(unicode_value='create', tag='create')
Event.read = Event._CF_enumeration.addEnumeration(unicode_value='read', tag='read')
Event.update = Event._CF_enumeration.addEnumeration(unicode_value='update', tag='update')
Event.delete = Event._CF_enumeration.addEnumeration(unicode_value='delete', tag='delete')
Event.replicate = Event._CF_enumeration.addEnumeration(unicode_value='replicate', tag='replicate')
Event.synchronization_failed = Event._CF_enumeration.addEnumeration(unicode_value='synchronization_failed', tag='synchronization_failed')
Event.replication_failed = Event._CF_enumeration.addEnumeration(unicode_value='replication_failed', tag='replication_failed')
Event._InitializeFacetMap(Event._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'Event', Event)
_module_typeBindings.Event = Event

# Atomic simple type: {http://ns.dataone.org/service/types/v1}NodeState
class NodeState (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """An indicator of the current node accessibility. Nodes
      that are marked *down* are inaccessible for service operations, those
      that are *up* are in the normal accessible state, and *unknown*
      indicates that the state has not been determined yet."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NodeState')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 125, 2)
    _Documentation = 'An indicator of the current node accessibility. Nodes\n      that are marked *down* are inaccessible for service operations, those\n      that are *up* are in the normal accessible state, and *unknown*\n      indicates that the state has not been determined yet.'
NodeState._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=NodeState, enum_prefix=None)
NodeState.up = NodeState._CF_enumeration.addEnumeration(unicode_value='up', tag='up')
NodeState.down = NodeState._CF_enumeration.addEnumeration(unicode_value='down', tag='down')
NodeState.unknown = NodeState._CF_enumeration.addEnumeration(unicode_value='unknown', tag='unknown')
NodeState._InitializeFacetMap(NodeState._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'NodeState', NodeState)
_module_typeBindings.NodeState = NodeState

# Atomic simple type: {http://ns.dataone.org/service/types/v1}NodeType
class NodeType (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """The type of this node, which is either *mn* for
      Member Nodes, or *cn* for Coordinating Nodes."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NodeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 140, 2)
    _Documentation = 'The type of this node, which is either *mn* for\n      Member Nodes, or *cn* for Coordinating Nodes.'
NodeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=NodeType, enum_prefix=None)
NodeType.mn = NodeType._CF_enumeration.addEnumeration(unicode_value='mn', tag='mn')
NodeType.cn = NodeType._CF_enumeration.addEnumeration(unicode_value='cn', tag='cn')
NodeType.Monitor = NodeType._CF_enumeration.addEnumeration(unicode_value='Monitor', tag='Monitor')
NodeType._InitializeFacetMap(NodeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'NodeType', NodeType)
_module_typeBindings.NodeType = NodeType

# Atomic simple type: {http://ns.dataone.org/service/types/v1}NonEmptyString
class NonEmptyString (pyxb.binding.datatypes.string):

    """A derived string type with at least length 1 and it
      must contain non-whitespace."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NonEmptyString')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 153, 2)
    _Documentation = 'A derived string type with at least length 1 and it\n      must contain non-whitespace.'
NonEmptyString._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
NonEmptyString._CF_pattern = pyxb.binding.facets.CF_pattern()
NonEmptyString._CF_pattern.addPattern(pattern='[\\s]*[\\S][\\s\\S]*')
NonEmptyString._InitializeFacetMap(NonEmptyString._CF_minLength,
   NonEmptyString._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'NonEmptyString', NonEmptyString)
_module_typeBindings.NonEmptyString = NonEmptyString

# Atomic simple type: {http://ns.dataone.org/service/types/v1}Permission
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

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Permission')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 199, 2)
    _Documentation = 'A string value indicating the set of actions that can\n      be performed on a resource as specified in an access policy. The set of\n      permissions include the ability to read a resource (*read*), modify a\n      resource (*write*), and to change the set of access control policies for\n      a resource (*changePermission*). Permission levels are cumulative, in\n      that write permission implicitly grants read access, and\n      changePermission permission implicitly grants write access (and\n      therefore read as well). If a subject is granted multiple permissions,\n      the highest level of access applies.'
Permission._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Permission, enum_prefix=None)
Permission.read = Permission._CF_enumeration.addEnumeration(unicode_value='read', tag='read')
Permission.write = Permission._CF_enumeration.addEnumeration(unicode_value='write', tag='write')
Permission.changePermission = Permission._CF_enumeration.addEnumeration(unicode_value='changePermission', tag='changePermission')
Permission._InitializeFacetMap(Permission._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'Permission', Permission)
_module_typeBindings.Permission = Permission

# Atomic simple type: {http://ns.dataone.org/service/types/v1}ReplicationStatus
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

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ReplicationStatus')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 219, 2)
    _Documentation = 'An enumerated string value indicating the current\n      state of a replica of an object. When an object identified needs to be\n      replicated, it is added to the replication task queue and is marked as\n      *queued*; a CN will pick up that task and request that it be replicated\n      to a MN and marks that it as *requested*; when a MN finishes replicating\n      the object, it informs the CN that it is finished and it is marked as\n      *completed*. If an MN is unable to complete replication, the\n      replication status is marked as *failed*.Periodically a CN checks each replica to be sure it is\n      both available and valid (matching checksum with original), and if it is\n      either inaccessible or invalid then it marks it as *invalidated*, which\n      indicates that the object replication needs to be invoked\n      again.The replication process is described in Use Case 09\n      (:doc:`/design/UseCases/09_uc`).'
ReplicationStatus._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ReplicationStatus, enum_prefix=None)
ReplicationStatus.queued = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value='queued', tag='queued')
ReplicationStatus.requested = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value='requested', tag='requested')
ReplicationStatus.completed = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value='completed', tag='completed')
ReplicationStatus.failed = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value='failed', tag='failed')
ReplicationStatus.invalidated = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value='invalidated', tag='invalidated')
ReplicationStatus._InitializeFacetMap(ReplicationStatus._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'ReplicationStatus', ReplicationStatus)
_module_typeBindings.ReplicationStatus = ReplicationStatus

# Atomic simple type: {http://ns.dataone.org/service/types/v1}ObjectFormatIdentifier
class ObjectFormatIdentifier (NonEmptyString):

    """A string used to identify an instance of
      :class:`Types.ObjectFormat` and MUST be unique within an instance of
      :class:`Types.ObjectFormatList`. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ObjectFormatIdentifier')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 165, 2)
    _Documentation = 'A string used to identify an instance of\n      :class:`Types.ObjectFormat` and MUST be unique within an instance of\n      :class:`Types.ObjectFormatList`. '
ObjectFormatIdentifier._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ObjectFormatIdentifier', ObjectFormatIdentifier)
_module_typeBindings.ObjectFormatIdentifier = ObjectFormatIdentifier

# Atomic simple type: {http://ns.dataone.org/service/types/v1}NonEmptyString800
class NonEmptyString800 (NonEmptyString):

    """ An NonEmptyString800 is a NonEmptyString string with
      a maximum length of 800 characters."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NonEmptyString800')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 175, 2)
    _Documentation = ' An NonEmptyString800 is a NonEmptyString string with\n      a maximum length of 800 characters.'
NonEmptyString800._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(800))
NonEmptyString800._InitializeFacetMap(NonEmptyString800._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'NonEmptyString800', NonEmptyString800)
_module_typeBindings.NonEmptyString800 = NonEmptyString800

# Atomic simple type: {http://ns.dataone.org/service/types/v1}ServiceName
class ServiceName (NonEmptyString):

    """The name of a service that is available on a
      Node."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ServiceName')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 248, 2)
    _Documentation = 'The name of a service that is available on a\n      Node.'
ServiceName._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ServiceName', ServiceName)
_module_typeBindings.ServiceName = ServiceName

# Atomic simple type: {http://ns.dataone.org/service/types/v1}ServiceVersion
class ServiceVersion (NonEmptyString):

    """The version of a service provided by a Node. Service
      versions are expressed as version labels such as "v1", "v2". DataONE
      services are released only as major service versions; patches to
      services are not indicated in this version label."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ServiceVersion')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 257, 2)
    _Documentation = 'The version of a service provided by a Node. Service\n      versions are expressed as version labels such as "v1", "v2". DataONE\n      services are released only as major service versions; patches to\n      services are not indicated in this version label.'
ServiceVersion._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ServiceVersion', ServiceVersion)
_module_typeBindings.ServiceVersion = ServiceVersion

# Atomic simple type: {http://ns.dataone.org/service/types/v1}NonEmptyNoWhitespaceString800
class NonEmptyNoWhitespaceString800 (NonEmptyString800):

    """A NonEmptyNoWhitespaceString800 is a NonEmptyString800
      string that doesn't allow whitespace characters (space, tab, newline,
      carriage return). Unicode whitespace characters outside of the ASCII
      character set need to be checked programmatically."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NonEmptyNoWhitespaceString800')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 186, 2)
    _Documentation = "A NonEmptyNoWhitespaceString800 is a NonEmptyString800\n      string that doesn't allow whitespace characters (space, tab, newline,\n      carriage return). Unicode whitespace characters outside of the ASCII\n      character set need to be checked programmatically."
NonEmptyNoWhitespaceString800._CF_pattern = pyxb.binding.facets.CF_pattern()
NonEmptyNoWhitespaceString800._CF_pattern.addPattern(pattern='\\S+')
NonEmptyNoWhitespaceString800._InitializeFacetMap(NonEmptyNoWhitespaceString800._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'NonEmptyNoWhitespaceString800', NonEmptyNoWhitespaceString800)
_module_typeBindings.NonEmptyNoWhitespaceString800 = NonEmptyNoWhitespaceString800

# Complex type {http://ns.dataone.org/service/types/v1}AccessPolicy with content type ELEMENT_ONLY
class AccessPolicy (pyxb.binding.basis.complexTypeDefinition):
    """A set of rules that specifies as a whole the allowable
      permissions that a given user, group, or system has for accessing a
      resource, including data, metadata, resource map, and service resources.
      An access policy consists of a sequence of allow rules that grant
      permissions to principals, which can be individual users, groups of
      users, symbolic users, or systems and services."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AccessPolicy')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 275, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element allow uses Python identifier allow
    __allow = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allow'), 'allow', '__httpns_dataone_orgservicetypesv1_AccessPolicy_allow', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 285, 6), )

    
    allow = property(__allow.value, __allow.set, None, None)

    _ElementMap.update({
        __allow.name() : __allow
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.AccessPolicy = AccessPolicy
Namespace.addCategoryObject('typeBinding', 'AccessPolicy', AccessPolicy)


# Complex type {http://ns.dataone.org/service/types/v1}AccessRule with content type ELEMENT_ONLY
class AccessRule (pyxb.binding.basis.complexTypeDefinition):
    """A rule that is used to allow a :term:`subject` to
      perform an action (such as read or write) on an object in DataONE. Rules
      are tuples (subject, permission) specifying which permissions are
      allowed for the subjects(s). If a subject is granted multiple
      permissions, the highest level of access applies. The resource on which
      the access control rules are being applied is determined by the
      containing :term:`SystemMetadata` document, or in the case of methods
      such as :func:`CNAuthorization.setAccessPolicy`, by the :term:`pid` in
      the method parameters.Access control rules are specified by the
      :term:`Origin Member Node` when the object is first registered in
      DataONE. If no rules are specified at that time, then the object is
      deemed to be private and the only user with access to the object (read,
      write, or otherwise) is the :term:`Rights Holder`."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AccessRule')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 291, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_AccessRule_subject', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 309, 6), )

    
    subject = property(__subject.value, __subject.set, None, None)

    
    # Element permission uses Python identifier permission
    __permission = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'permission'), 'permission', '__httpns_dataone_orgservicetypesv1_AccessRule_permission', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 311, 6), )

    
    permission = property(__permission.value, __permission.set, None, None)

    _ElementMap.update({
        __subject.name() : __subject,
        __permission.name() : __permission
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.AccessRule = AccessRule
Namespace.addCategoryObject('typeBinding', 'AccessRule', AccessRule)


# Complex type {http://ns.dataone.org/service/types/v1}ChecksumAlgorithmList with content type ELEMENT_ONLY
class ChecksumAlgorithmList (pyxb.binding.basis.complexTypeDefinition):
    """Represents a list of :term:`checksum`
      algorithms."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ChecksumAlgorithmList')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 337, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element algorithm uses Python identifier algorithm
    __algorithm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'algorithm'), 'algorithm', '__httpns_dataone_orgservicetypesv1_ChecksumAlgorithmList_algorithm', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 343, 6), )

    
    algorithm = property(__algorithm.value, __algorithm.set, None, None)

    _ElementMap.update({
        __algorithm.name() : __algorithm
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ChecksumAlgorithmList = ChecksumAlgorithmList
Namespace.addCategoryObject('typeBinding', 'ChecksumAlgorithmList', ChecksumAlgorithmList)


# Complex type {http://ns.dataone.org/service/types/v1}Group with content type ELEMENT_ONLY
class Group (pyxb.binding.basis.complexTypeDefinition):
    """Group represents metadata about a :term:`Subject` that
      represents a collection of other Subjects. Groups provide a convenient
      mechanism to express access rules for certain roles that are not
      necessarily tied to particular :term:`principals` over
      time."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Group')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 349, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Group_subject', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 358, 6), )

    
    subject = property(__subject.value, __subject.set, None, 'The unique, immutable identifier of the\n          :term:`group`. Group subjects must not be reused, and so they are\n          both immutable and can not be deleted from the DataONE\n          system.')

    
    # Element groupName uses Python identifier groupName
    __groupName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'groupName'), 'groupName', '__httpns_dataone_orgservicetypesv1_Group_groupName', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 366, 6), )

    
    groupName = property(__groupName.value, __groupName.set, None, 'The name of the Group.')

    
    # Element hasMember uses Python identifier hasMember
    __hasMember = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'hasMember'), 'hasMember', '__httpns_dataone_orgservicetypesv1_Group_hasMember', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 372, 6), )

    
    hasMember = property(__hasMember.value, __hasMember.set, None, 'A :term:`Subject` that is a member of this\n            group, expressed using the unique identifier for that\n            Subject.')

    
    # Element rightsHolder uses Python identifier rightsHolder
    __rightsHolder = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rightsHolder'), 'rightsHolder', '__httpns_dataone_orgservicetypesv1_Group_rightsHolder', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 380, 4), )

    
    rightsHolder = property(__rightsHolder.value, __rightsHolder.set, None, 'Represents the list of owners of this :term:`group`.\n        All groups are readable by anyone in the DataONE system, but can only\n        be modified by subjects listed in *rightsHolder* fields. Designation\n        as a :term:`rightsHolder` allows the subject, or their equivalent\n        identities, to make changes to the mutable properties of the group,\n        including its name, membership list and rights holder list. The\n        subject of the group itself is immutable. ')

    _ElementMap.update({
        __subject.name() : __subject,
        __groupName.name() : __groupName,
        __hasMember.name() : __hasMember,
        __rightsHolder.name() : __rightsHolder
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Group = Group
Namespace.addCategoryObject('typeBinding', 'Group', Group)


# Complex type {http://ns.dataone.org/service/types/v1}LogEntry with content type ELEMENT_ONLY
class LogEntry (pyxb.binding.basis.complexTypeDefinition):
    """A single log entry as reported by a Member Node or
      Coordinating Node through the :func:`MNCore.getLogRecords` or
      :func:`CNCore.getLogRecords` methods."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LogEntry')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 437, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element entryId uses Python identifier entryId
    __entryId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'entryId'), 'entryId', '__httpns_dataone_orgservicetypesv1_LogEntry_entryId', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 444, 6), )

    
    entryId = property(__entryId.value, __entryId.set, None, 'A unique identifier for this log entry. The\n          identifier should be unique for a particular node; This is not drawn\n          from the same value space as other identifiers in DataONE, and so is\n          not subjec to the same restrictions.')

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_LogEntry_identifier', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 453, 6), )

    
    identifier = property(__identifier.value, __identifier.set, None, 'The :term:`identifier` of the object that was the\n          target of the operation which generated this log entry.')

    
    # Element ipAddress uses Python identifier ipAddress
    __ipAddress = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ipAddress'), 'ipAddress', '__httpns_dataone_orgservicetypesv1_LogEntry_ipAddress', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 460, 6), )

    
    ipAddress = property(__ipAddress.value, __ipAddress.set, None, 'The IP address, as reported by the service receiving\n          the request, of the request origin.')

    
    # Element userAgent uses Python identifier userAgent
    __userAgent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'userAgent'), 'userAgent', '__httpns_dataone_orgservicetypesv1_LogEntry_userAgent', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 467, 6), )

    
    userAgent = property(__userAgent.value, __userAgent.set, None, 'The user agent of the client making the request, as\n          reported in the User-Agent HTTP header.')

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_LogEntry_subject', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 474, 6), )

    
    subject = property(__subject.value, __subject.set, None, 'The :term:`Subject` used for making the request.\n          This may be the DataONE :term:`public` user if the request is not\n          authenticated, otherwise it will be the *Subject* of the certificate\n          used for authenticating the request.')

    
    # Element event uses Python identifier event
    __event = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'event'), 'event', '__httpns_dataone_orgservicetypesv1_LogEntry_event', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 483, 6), )

    
    event = property(__event.value, __event.set, None, 'An entry from the :class:`Types.Event` enumeration\n          indicating the type of operation that triggered the log message.')

    
    # Element dateLogged uses Python identifier dateLogged
    __dateLogged = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dateLogged'), 'dateLogged', '__httpns_dataone_orgservicetypesv1_LogEntry_dateLogged', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 490, 6), )

    
    dateLogged = property(__dateLogged.value, __dateLogged.set, None, 'A :class:`Types.DateTime` time stamp indicating when\n          the event triggering the log message ocurred. Note that all time\n          stamps in DataONE are in UTC.')

    
    # Element nodeIdentifier uses Python identifier nodeIdentifier
    __nodeIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'nodeIdentifier'), 'nodeIdentifier', '__httpns_dataone_orgservicetypesv1_LogEntry_nodeIdentifier', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 498, 6), )

    
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


# Complex type {http://ns.dataone.org/service/types/v1}NodeReplicationPolicy with content type ELEMENT_ONLY
class NodeReplicationPolicy (pyxb.binding.basis.complexTypeDefinition):
    """The overall replication policy for the node that
      expresses constraints on object size, total objects, source nodes, and
      object format types. A node may choose to restrict replication from only
      certain peer nodes, may have file size limits, total allocated size
      limits, or may want to focus on being a :term:`replication target` for
      domain-specific object formats."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NodeReplicationPolicy')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 645, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element maxObjectSize uses Python identifier maxObjectSize
    __maxObjectSize = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'maxObjectSize'), 'maxObjectSize', '__httpns_dataone_orgservicetypesv1_NodeReplicationPolicy_maxObjectSize', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 655, 6), )

    
    maxObjectSize = property(__maxObjectSize.value, __maxObjectSize.set, None, 'An optional statement of the maximum size in octets\n          (8-bit bytes) of objects this node is willing to accept for\n          replication.')

    
    # Element spaceAllocated uses Python identifier spaceAllocated
    __spaceAllocated = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'spaceAllocated'), 'spaceAllocated', '__httpns_dataone_orgservicetypesv1_NodeReplicationPolicy_spaceAllocated', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 663, 6), )

    
    spaceAllocated = property(__spaceAllocated.value, __spaceAllocated.set, None, 'An optional statement of the total space in bytes\n          allocated for replication object storage on this\n          node.')

    
    # Element allowedNode uses Python identifier allowedNode
    __allowedNode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allowedNode'), 'allowedNode', '__httpns_dataone_orgservicetypesv1_NodeReplicationPolicy_allowedNode', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 671, 6), )

    
    allowedNode = property(__allowedNode.value, __allowedNode.set, None, 'An optional, repeatable statement of a peer source\n          node from which this node is willing to replicate content, expressed\n          as a :class:`Types.NodeReference`.')

    
    # Element allowedObjectFormat uses Python identifier allowedObjectFormat
    __allowedObjectFormat = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allowedObjectFormat'), 'allowedObjectFormat', '__httpns_dataone_orgservicetypesv1_NodeReplicationPolicy_allowedObjectFormat', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 679, 6), )

    
    allowedObjectFormat = property(__allowedObjectFormat.value, __allowedObjectFormat.set, None, 'An optional, repeatable statement of an object\n          format that this node is willing to replicate, expressed as a\n          :class:`Types.ObjectFormatIdentifier`.')

    _ElementMap.update({
        __maxObjectSize.name() : __maxObjectSize,
        __spaceAllocated.name() : __spaceAllocated,
        __allowedNode.name() : __allowedNode,
        __allowedObjectFormat.name() : __allowedObjectFormat
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.NodeReplicationPolicy = NodeReplicationPolicy
Namespace.addCategoryObject('typeBinding', 'NodeReplicationPolicy', NodeReplicationPolicy)


# Complex type {http://ns.dataone.org/service/types/v1}NodeList with content type ELEMENT_ONLY
class NodeList (pyxb.binding.basis.complexTypeDefinition):
    """ A list of :class:`Types.Node` entries returned by
      :func:`CNCore.listNodes()`.NodeList is described in
       :mod:`NodeList`."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NodeList')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 691, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element node uses Python identifier node
    __node = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'node'), 'node', '__httpns_dataone_orgservicetypesv1_NodeList_node', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 699, 6), )

    
    node = property(__node.value, __node.set, None, None)

    _ElementMap.update({
        __node.name() : __node
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.NodeList = NodeList
Namespace.addCategoryObject('typeBinding', 'NodeList', NodeList)


# Complex type {http://ns.dataone.org/service/types/v1}ObjectFormat with content type ELEMENT_ONLY
class ObjectFormat (pyxb.binding.basis.complexTypeDefinition):
    """One value from the DataONE Object Format Vocabulary
      which is returned by :func:`CNCore.getFormat()`.An *ObjectFormat* is the structure returned from the
      :func:`CNCore.getFormat()` method of the CN REST interface. It provides
      the unique identifier and the name associated with the object format.
      Future versions may contain additional structured content from external
      common typing systems. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ObjectFormat')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 719, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element formatId uses Python identifier formatId
    __formatId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'formatId'), 'formatId', '__httpns_dataone_orgservicetypesv1_ObjectFormat_formatId', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 730, 6), )

    
    formatId = property(__formatId.value, __formatId.set, None, ' The unique identifier of the object format in the\n          DataONE Object Format Vocabulary. The identifier should comply with\n          DataONE Identifier rules, i.e. no whitespace, only UTF-8 or US-ASCII\n          printable characters.')

    
    # Element formatName uses Python identifier formatName
    __formatName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'formatName'), 'formatName', '__httpns_dataone_orgservicetypesv1_ObjectFormat_formatName', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 739, 6), )

    
    formatName = property(__formatName.value, __formatName.set, None, 'For objects that are typed using a Document Type\n          Definition, this lists the well-known and accepted named version of\n          the DTD. In other cases, an appropriately unambiguous descriptive\n          name should be chosen.')

    
    # Element formatType uses Python identifier formatType
    __formatType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'formatType'), 'formatType', '__httpns_dataone_orgservicetypesv1_ObjectFormat_formatType', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 748, 6), )

    
    formatType = property(__formatType.value, __formatType.set, None, 'A string field indicating whether or not this\n          format is :term:`science data` (*DATA*), :term:`science metadata`\n          (*METADATA*) or a :term:`resource map` (*RESOURCE*). If the format\n          is a self-describing data format that includes science metadata,\n          then the field should also be set to science metadata.\n          ')

    _ElementMap.update({
        __formatId.name() : __formatId,
        __formatName.name() : __formatName,
        __formatType.name() : __formatType
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ObjectFormat = ObjectFormat
Namespace.addCategoryObject('typeBinding', 'ObjectFormat', ObjectFormat)


# Complex type {http://ns.dataone.org/service/types/v1}ObjectInfo with content type ELEMENT_ONLY
class ObjectInfo (pyxb.binding.basis.complexTypeDefinition):
    """Metadata about an object, representing a subset of the
      metadata found in :class:`Types.SystemMetadata`."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ObjectInfo')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 784, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_ObjectInfo_identifier', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 790, 8), )

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element formatId uses Python identifier formatId
    __formatId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'formatId'), 'formatId', '__httpns_dataone_orgservicetypesv1_ObjectInfo_formatId', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 792, 8), )

    
    formatId = property(__formatId.value, __formatId.set, None, None)

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'checksum'), 'checksum', '__httpns_dataone_orgservicetypesv1_ObjectInfo_checksum', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 793, 8), )

    
    checksum = property(__checksum.value, __checksum.set, None, None)

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpns_dataone_orgservicetypesv1_ObjectInfo_dateSysMetadataModified', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 795, 8), )

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, None)

    
    # Element size uses Python identifier size
    __size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'size'), 'size', '__httpns_dataone_orgservicetypesv1_ObjectInfo_size', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 796, 8), )

    
    size = property(__size.value, __size.set, None, None)

    _ElementMap.update({
        __identifier.name() : __identifier,
        __formatId.name() : __formatId,
        __checksum.name() : __checksum,
        __dateSysMetadataModified.name() : __dateSysMetadataModified,
        __size.name() : __size
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ObjectInfo = ObjectInfo
Namespace.addCategoryObject('typeBinding', 'ObjectInfo', ObjectInfo)


# Complex type {http://ns.dataone.org/service/types/v1}ObjectLocation with content type ELEMENT_ONLY
class ObjectLocation (pyxb.binding.basis.complexTypeDefinition):
    """Portion of an :class:`Types.ObjectLocationList`
      indicating the node from which the object can be retrieved. The
      principal information on each location is found in the *nodeIdentifier*,
      all other fields are provided for convenience, but could also be looked
      up from the :class:`Types.NodeList` information obtained from
      :func:`CNCore.listNodes`."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ObjectLocation')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 817, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element nodeIdentifier uses Python identifier nodeIdentifier
    __nodeIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'nodeIdentifier'), 'nodeIdentifier', '__httpns_dataone_orgservicetypesv1_ObjectLocation_nodeIdentifier', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 827, 6), )

    
    nodeIdentifier = property(__nodeIdentifier.value, __nodeIdentifier.set, None, 'Identifier of the :class:`Types.Node` (the same\n          identifier used in the node registry for identifying the node).\n          ')

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'baseURL'), 'baseURL', '__httpns_dataone_orgservicetypesv1_ObjectLocation_baseURL', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 835, 6), )

    
    baseURL = property(__baseURL.value, __baseURL.set, None, 'The current base URL (the *baseURL* element from\n          the :class:`Types.Node` record) for services implemented on the\n          target node. Used with service version to construct a URL for\n          service calls to this node. Note that complete information on\n          services available on a Node is available from the\n          :func:`CNCore.listNodes` service. ')

    
    # Element version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpns_dataone_orgservicetypesv1_ObjectLocation_version', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 845, 6), )

    
    version = property(__version.value, __version.set, None, 'The version of services implemented on the node.\n          Used with base url to construct a URL for service calls to this\n          node. Note that complete information on services available on a Node\n          is available from the :func:`CNCore.listNodes` service.\n          ')

    
    # Element url uses Python identifier url
    __url = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'url'), 'url', '__httpns_dataone_orgservicetypesv1_ObjectLocation_url', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 855, 6), )

    
    url = property(__url.value, __url.set, None, 'The full (absolute) URL that can be used to\n          retrieve the object using the get() method of the rest\n          interface.For example, if identifier was "ABX154", and the\n          node had a base URL of ``http://mn1.dataone.org/mn`` then the value\n          would be\n          ``http://mn1.dataone.org/mn/v1/object/ABX154``')

    
    # Element preference uses Python identifier preference
    __preference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'preference'), 'preference', '__httpns_dataone_orgservicetypesv1_ObjectLocation_preference', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 866, 6), )

    
    preference = property(__preference.value, __preference.set, None, 'A weighting parameter that provides a hint to the\n          caller for the relative preference for nodes from which the content\n          should be retrieved. Higher values have higher preference.\n          ')

    _ElementMap.update({
        __nodeIdentifier.name() : __nodeIdentifier,
        __baseURL.name() : __baseURL,
        __version.name() : __version,
        __url.name() : __url,
        __preference.name() : __preference
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ObjectLocation = ObjectLocation
Namespace.addCategoryObject('typeBinding', 'ObjectLocation', ObjectLocation)


# Complex type {http://ns.dataone.org/service/types/v1}ObjectLocationList with content type ELEMENT_ONLY
class ObjectLocationList (pyxb.binding.basis.complexTypeDefinition):
    """An *ObjectLocationList* is the structure returned from
      the :func:`CNRead.resolve` method of the CN REST interface. It provides
      a list of locations from which the specified object can be retrieved.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ObjectLocationList')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 878, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_ObjectLocationList_identifier', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 886, 4), )

    
    identifier = property(__identifier.value, __identifier.set, None, 'The :term:`identifier` of the object being\n        resolved.')

    
    # Element objectLocation uses Python identifier objectLocation
    __objectLocation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'objectLocation'), 'objectLocation', '__httpns_dataone_orgservicetypesv1_ObjectLocationList_objectLocation', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 893, 4), )

    
    objectLocation = property(__objectLocation.value, __objectLocation.set, None, 'List of nodes from which the object can be\n        retrieved')

    _ElementMap.update({
        __identifier.name() : __identifier,
        __objectLocation.name() : __objectLocation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ObjectLocationList = ObjectLocationList
Namespace.addCategoryObject('typeBinding', 'ObjectLocationList', ObjectLocationList)


# Complex type {http://ns.dataone.org/service/types/v1}Person with content type ELEMENT_ONLY
class Person (pyxb.binding.basis.complexTypeDefinition):
    """*Person* represents metadata about a :term:`Principal`
      that is a person and that can be used by clients and nodes for
      :class:`Types.AccessPolicy` information. The mutable properties of a
      *Person* instance can only be changed by itself (i.e., the Subject
      identifying the Person instance) and by the Coordinating Node identity,
      but can be read by any identity in the DataONE system.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Person')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 904, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Person_subject', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 915, 6), )

    
    subject = property(__subject.value, __subject.set, None, 'The unique, immutable identifier for the\n          *Person*.')

    
    # Element givenName uses Python identifier givenName
    __givenName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'givenName'), 'givenName', '__httpns_dataone_orgservicetypesv1_Person_givenName', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 922, 6), )

    
    givenName = property(__givenName.value, __givenName.set, None, 'The given name of the *Person*, repeatable if they\n          have more than one given name.')

    
    # Element familyName uses Python identifier familyName
    __familyName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'familyName'), 'familyName', '__httpns_dataone_orgservicetypesv1_Person_familyName', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 929, 6), )

    
    familyName = property(__familyName.value, __familyName.set, None, 'The family name of the *Person*.')

    
    # Element email uses Python identifier email
    __email = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'email'), 'email', '__httpns_dataone_orgservicetypesv1_Person_email', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 935, 6), )

    
    email = property(__email.value, __email.set, None, 'The email address of the *Person*, repeatable if\n          they have more than one email address. ')

    
    # Element isMemberOf uses Python identifier isMemberOf
    __isMemberOf = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'isMemberOf'), 'isMemberOf', '__httpns_dataone_orgservicetypesv1_Person_isMemberOf', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 942, 6), )

    
    isMemberOf = property(__isMemberOf.value, __isMemberOf.set, None, 'A *group* or role in which the *Person* is a member,\n          expressed using the unique :class:`Types.Subject` identifier for\n          that :class:`Types.Group`, and repeatable if they are a member of\n          more than one group. ')

    
    # Element equivalentIdentity uses Python identifier equivalentIdentity
    __equivalentIdentity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'equivalentIdentity'), 'equivalentIdentity', '__httpns_dataone_orgservicetypesv1_Person_equivalentIdentity', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 951, 6), )

    
    equivalentIdentity = property(__equivalentIdentity.value, __equivalentIdentity.set, None, 'An alternative but equivalent identity for the\n          :term:`principal` that has been used in alternate identity systems,\n          repeatable if more than one equivalent identity applies.\n          ')

    
    # Element verified uses Python identifier verified
    __verified = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'verified'), 'verified', '__httpns_dataone_orgservicetypesv1_Person_verified', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 960, 6), )

    
    verified = property(__verified.value, __verified.set, None, "*true* if the name and email address of the\n          *Person* have been :term:`verified` to ensure that the *givenName*\n          and *familyName* represent the real person's legal name, and that\n          the email address is correct for that person and is in the control\n          of the indicated individual. Verification occurs through an\n          established procedure within DataONE as part of the Identity\n          Management system. A Person can not change their own *verified*\n          field, but rather must be verified and changed through this DataONE\n          established process. ")

    _ElementMap.update({
        __subject.name() : __subject,
        __givenName.name() : __givenName,
        __familyName.name() : __familyName,
        __email.name() : __email,
        __isMemberOf.name() : __isMemberOf,
        __equivalentIdentity.name() : __equivalentIdentity,
        __verified.name() : __verified
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Person = Person
Namespace.addCategoryObject('typeBinding', 'Person', Person)


# Complex type {http://ns.dataone.org/service/types/v1}Ping with content type EMPTY
class Ping (pyxb.binding.basis.complexTypeDefinition):
    """Store results from the :func:`MNCore.ping`
      method."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Ping')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 986, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute success uses Python identifier success
    __success = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'success'), 'success', '__httpns_dataone_orgservicetypesv1_Ping_success', pyxb.binding.datatypes.boolean)
    __success._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 991, 4)
    __success._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 991, 4)
    
    success = property(__success.value, __success.set, None, 'A boolean flag indicating *true* if the node was\n        reached by the last :func:`MNCore.ping` or :func:`CNCore.ping` call,\n        otherwise *false*.')

    
    # Attribute lastSuccess uses Python identifier lastSuccess
    __lastSuccess = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'lastSuccess'), 'lastSuccess', '__httpns_dataone_orgservicetypesv1_Ping_lastSuccess', pyxb.binding.datatypes.dateTime)
    __lastSuccess._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 998, 4)
    __lastSuccess._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 998, 4)
    
    lastSuccess = property(__lastSuccess.value, __lastSuccess.set, None, 'The date time value (UTC) of the last time a\n        successful ping was performed.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __success.name() : __success,
        __lastSuccess.name() : __lastSuccess
    })
_module_typeBindings.Ping = Ping
Namespace.addCategoryObject('typeBinding', 'Ping', Ping)


# Complex type {http://ns.dataone.org/service/types/v1}Replica with content type ELEMENT_ONLY
class Replica (pyxb.binding.basis.complexTypeDefinition):
    """Replica information that describes the existence of a
      replica of some object managed by the DataONE infrastructure, and its
      status."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Replica')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1007, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element replicaMemberNode uses Python identifier replicaMemberNode
    __replicaMemberNode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'replicaMemberNode'), 'replicaMemberNode', '__httpns_dataone_orgservicetypesv1_Replica_replicaMemberNode', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1014, 6), )

    
    replicaMemberNode = property(__replicaMemberNode.value, __replicaMemberNode.set, None, 'A reference to the Member Node that houses this\n          replica, regardless of whether it has arrived at the Member Node or\n          not. See *replicationStatus* to determine if the replica is\n          completely transferred. ')

    
    # Element replicationStatus uses Python identifier replicationStatus
    __replicationStatus = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'replicationStatus'), 'replicationStatus', '__httpns_dataone_orgservicetypesv1_Replica_replicationStatus', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1022, 6), )

    
    replicationStatus = property(__replicationStatus.value, __replicationStatus.set, None, ' The current status of this replica, indicating\n          the stage of replication process for the object. Only *completed*\n          replicas should be considered as available. ')

    
    # Element replicaVerified uses Python identifier replicaVerified
    __replicaVerified = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'replicaVerified'), 'replicaVerified', '__httpns_dataone_orgservicetypesv1_Replica_replicaVerified', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1029, 6), )

    
    replicaVerified = property(__replicaVerified.value, __replicaVerified.set, None, ' The last date and time on which the integrity of\n          a replica was verified by the coordinating node. Verification occurs\n          by checking that the checksum of the stored object matches the\n          checksum recorded for the object in the system\n          metadata.')

    _ElementMap.update({
        __replicaMemberNode.name() : __replicaMemberNode,
        __replicationStatus.name() : __replicationStatus,
        __replicaVerified.name() : __replicaVerified
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Replica = Replica
Namespace.addCategoryObject('typeBinding', 'Replica', Replica)


# Complex type {http://ns.dataone.org/service/types/v1}ReplicationPolicy with content type ELEMENT_ONLY
class ReplicationPolicy (pyxb.binding.basis.complexTypeDefinition):
    """The *ReplicationPolicy* for an object defines if
      replication should be attempted for this object, and if so, how many
      replicas should be maintained. It also permits specification of
      preferred and blocked nodes as potential replication targets.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ReplicationPolicy')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1042, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element preferredMemberNode uses Python identifier preferredMemberNode
    __preferredMemberNode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'preferredMemberNode'), 'preferredMemberNode', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_preferredMemberNode', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1051, 6), )

    
    preferredMemberNode = property(__preferredMemberNode.value, __preferredMemberNode.set, None, 'Preferred Nodes are utilized over other nodes as\n          replication targets, up to the number of replicas requested. If\n          preferred nodes are unavailable, or if insufficient nodes are listed\n          as preferred to meet the requested number of replicas, then the\n          Coordinating Nodes will pick additional replica nodes for the\n          content. ')

    
    # Element blockedMemberNode uses Python identifier blockedMemberNode
    __blockedMemberNode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'blockedMemberNode'), 'blockedMemberNode', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_blockedMemberNode', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1062, 6), )

    
    blockedMemberNode = property(__blockedMemberNode.value, __blockedMemberNode.set, None, 'The object MUST never be replicated to nodes\n          listed as *blockedMemberNodes*. Where there is a conflict between a\n          *preferredMemberNode* and a *blockedMemberNode* entry, the\n          *blockedMemberNode* entry prevails. ')

    
    # Attribute replicationAllowed uses Python identifier replicationAllowed
    __replicationAllowed = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'replicationAllowed'), 'replicationAllowed', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_replicationAllowed', pyxb.binding.datatypes.boolean)
    __replicationAllowed._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1072, 4)
    __replicationAllowed._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1072, 4)
    
    replicationAllowed = property(__replicationAllowed.value, __replicationAllowed.set, None, 'A boolean flag indicating if the object should be\n        replicated (*true*, default) or not (*false*).')

    
    # Attribute numberReplicas uses Python identifier numberReplicas
    __numberReplicas = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'numberReplicas'), 'numberReplicas', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_numberReplicas', pyxb.binding.datatypes.int)
    __numberReplicas._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1078, 4)
    __numberReplicas._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1078, 4)
    
    numberReplicas = property(__numberReplicas.value, __numberReplicas.set, None, 'An integer indicating the number of replicas\n        targeted for this object. Defaults to 3.')

    _ElementMap.update({
        __preferredMemberNode.name() : __preferredMemberNode,
        __blockedMemberNode.name() : __blockedMemberNode
    })
    _AttributeMap.update({
        __replicationAllowed.name() : __replicationAllowed,
        __numberReplicas.name() : __numberReplicas
    })
_module_typeBindings.ReplicationPolicy = ReplicationPolicy
Namespace.addCategoryObject('typeBinding', 'ReplicationPolicy', ReplicationPolicy)


# Complex type {http://ns.dataone.org/service/types/v1}Services with content type ELEMENT_ONLY
class Services (pyxb.binding.basis.complexTypeDefinition):
    """A list of services that are provided by a node. Used
      in Node descriptions so that Nodes can provide metadata about each
      service they implement and support. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Services')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1153, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element service uses Python identifier service
    __service = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'service'), 'service', '__httpns_dataone_orgservicetypesv1_Services_service', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1160, 6), )

    
    service = property(__service.value, __service.set, None, None)

    _ElementMap.update({
        __service.name() : __service
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Services = Services
Namespace.addCategoryObject('typeBinding', 'Services', Services)


# Complex type {http://ns.dataone.org/service/types/v1}Session with content type ELEMENT_ONLY
class Session (pyxb.binding.basis.complexTypeDefinition):
    """Information about the authenticated session for a
      service transaction. Session data is retrieved from the SSL client
      certificate and populated in the *Session* object. The subject
      represents the person or system that authenticated successfully, and the
      *subjectInfo* contains a listing of alternate identities (both Persons
      and Groups) that are also valid identities for this user. The
      *subjectInfo* should include at least one :class:`Types.Person` or
      :class:`Types.Group` entry that provides the attributes of the subject
      that was authenticated."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Session')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1166, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Session_subject', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1179, 6), )

    
    subject = property(__subject.value, __subject.set, None, None)

    
    # Element subjectInfo uses Python identifier subjectInfo
    __subjectInfo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'subjectInfo'), 'subjectInfo', '__httpns_dataone_orgservicetypesv1_Session_subjectInfo', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1181, 6), )

    
    subjectInfo = property(__subjectInfo.value, __subjectInfo.set, None, None)

    _ElementMap.update({
        __subject.name() : __subject,
        __subjectInfo.name() : __subjectInfo
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Session = Session
Namespace.addCategoryObject('typeBinding', 'Session', Session)


# Complex type {http://ns.dataone.org/service/types/v1}Slice with content type EMPTY
class Slice (pyxb.binding.basis.complexTypeDefinition):
    """An abstract type used as a common base for other types
      that need to include *count*, *start*, and *total* attributes to
      indicate which slice of a list is represented by a set of
      records.The first element in a list is always index 0, i.e.
      list indexes are zero-based."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Slice')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1205, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute count uses Python identifier count
    __count = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'count'), 'count', '__httpns_dataone_orgservicetypesv1_Slice_count', pyxb.binding.datatypes.int, required=True)
    __count._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1214, 4)
    __count._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1214, 4)
    
    count = property(__count.value, __count.set, None, 'The number of entries in the\n        slice.')

    
    # Attribute start uses Python identifier start
    __start = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'start'), 'start', '__httpns_dataone_orgservicetypesv1_Slice_start', pyxb.binding.datatypes.int, required=True)
    __start._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1220, 4)
    __start._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1220, 4)
    
    start = property(__start.value, __start.set, None, 'The zero-based index of the first element in the\n        slice.')

    
    # Attribute total uses Python identifier total
    __total = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'total'), 'total', '__httpns_dataone_orgservicetypesv1_Slice_total', pyxb.binding.datatypes.int, required=True)
    __total._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1226, 4)
    __total._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1226, 4)
    
    total = property(__total.value, __total.set, None, 'The total number of entries in the source list from\n        which the slice was extracted.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __count.name() : __count,
        __start.name() : __start,
        __total.name() : __total
    })
_module_typeBindings.Slice = Slice
Namespace.addCategoryObject('typeBinding', 'Slice', Slice)


# Complex type {http://ns.dataone.org/service/types/v1}Synchronization with content type ELEMENT_ONLY
class Synchronization (pyxb.binding.basis.complexTypeDefinition):
    """Configuration information for the process by which
      metadata is harvested from Member Nodes to Coordinating Nodes, including
      the schedule on which harvesting should occur, and information about the
      last :term:`synchronization` attempts for the node. Member Nodes
      providing *Synchronization* information only need to provide the
      *schedule*. Coordinating Nodes must set values for the *lastHarvested*
      and *lastCompleteHarvest* fields."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Synchronization')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1235, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element schedule uses Python identifier schedule
    __schedule = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'schedule'), 'schedule', '__httpns_dataone_orgservicetypesv1_Synchronization_schedule', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1246, 6), )

    
    schedule = property(__schedule.value, __schedule.set, None, 'An entry set by the Member Node indicating the\n          frequency for which synchronization should occur. This setting will\n          be influenced by the frequency with which content is updated on the\n          Member Node and the acceptable latency for detection and subsequent\n          processing of new content.')

    
    # Element lastHarvested uses Python identifier lastHarvested
    __lastHarvested = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'lastHarvested'), 'lastHarvested', '__httpns_dataone_orgservicetypesv1_Synchronization_lastHarvested', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1256, 6), )

    
    lastHarvested = property(__lastHarvested.value, __lastHarvested.set, None, 'The most recent modification date (UTC) of objects\n          checked during the last harvest of the node.')

    
    # Element lastCompleteHarvest uses Python identifier lastCompleteHarvest
    __lastCompleteHarvest = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'lastCompleteHarvest'), 'lastCompleteHarvest', '__httpns_dataone_orgservicetypesv1_Synchronization_lastCompleteHarvest', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1263, 6), )

    
    lastCompleteHarvest = property(__lastCompleteHarvest.value, __lastCompleteHarvest.set, None, 'The last time (UTC) all the data from a node was\n          pulled from a member node during a complete synchronization\n          process.')

    _ElementMap.update({
        __schedule.name() : __schedule,
        __lastHarvested.name() : __lastHarvested,
        __lastCompleteHarvest.name() : __lastCompleteHarvest
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Synchronization = Synchronization
Namespace.addCategoryObject('typeBinding', 'Synchronization', Synchronization)


# Complex type {http://ns.dataone.org/service/types/v1}SubjectInfo with content type ELEMENT_ONLY
class SubjectInfo (pyxb.binding.basis.complexTypeDefinition):
    """A list of :term:`Subjects`, including both
      :class:`Types.Person` and :class:`Types.Group` entries returned from
      the :func:`CNIdentity.getSubjectInfo` service and
      :func:`CNIdentity.listSubjects` services."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SubjectInfo')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1297, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element person uses Python identifier person
    __person = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'person'), 'person', '__httpns_dataone_orgservicetypesv1_SubjectInfo_person', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1305, 6), )

    
    person = property(__person.value, __person.set, None, None)

    
    # Element group uses Python identifier group
    __group = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'group'), 'group', '__httpns_dataone_orgservicetypesv1_SubjectInfo_group', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1306, 6), )

    
    group = property(__group.value, __group.set, None, None)

    _ElementMap.update({
        __person.name() : __person,
        __group.name() : __group
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SubjectInfo = SubjectInfo
Namespace.addCategoryObject('typeBinding', 'SubjectInfo', SubjectInfo)


# Complex type {http://ns.dataone.org/service/types/v1}SubjectList with content type ELEMENT_ONLY
class SubjectList (pyxb.binding.basis.complexTypeDefinition):
    """ A list of :term:`Subjects` used for identity/group
      management"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SubjectList')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1311, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_SubjectList_subject', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1317, 6), )

    
    subject = property(__subject.value, __subject.set, None, None)

    _ElementMap.update({
        __subject.name() : __subject
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SubjectList = SubjectList
Namespace.addCategoryObject('typeBinding', 'SubjectList', SubjectList)


# Complex type {http://ns.dataone.org/service/types/v1}SystemMetadata with content type ELEMENT_ONLY
class SystemMetadata (pyxb.binding.basis.complexTypeDefinition):
    """ System metadata (often referred to as
      :term:`sysmeta`) is the information used by DataONE to track and manage
      objects across the distributed Coordinating and Member Nodes of the
      network. System metadata documents contain low level information (e.g.
      size, type, owner, access control rules) about managed objects such as
      science data, science metadata, and resource map objects and the
      relationships between objects (e.g. *obsoletes* and
      *obsoletedBy*). The information is maintained dynamically by
      Coordinating Nodes and is mutable in that it reflects the current state
      of an object in the system. Initial properties of system metadata are
      generated by clients and Member Nodes. After object synchronization, the
      Coordinating Nodes hold authoritative copies of system metadata. Mirror
      copies of system metadata are maintained at each of the Coordinating
      nodes.  System metadata are considered operational
      information needed to run DataONE, and can be read by all Coordinating
      Nodes and Member Nodes in the course of service provision. In order to
      reduce issues with third-party tracking of data status information,
      users can read system metadata for an object if they have the access
      rights to read the corresponding object which a system metadata record
      describes.  System Metadata elements are partitioned into two
      classes: metadata elements that must be provided by client software to
      the DataONE system, and elements that are generated by DataONE itself in
      the course of managing objects. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SystemMetadata')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1323, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element serialVersion uses Python identifier serialVersion
    __serialVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'serialVersion'), 'serialVersion', '__httpns_dataone_orgservicetypesv1_SystemMetadata_serialVersion', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1354, 6), )

    
    serialVersion = property(__serialVersion.value, __serialVersion.set, None, ' A serial number maintained by the coordinating node\n            to indicate when changes have occurred to *SystemMetadata* to avoid\n            update conflicts. Clients should ensure that they have the most\n            recent version of a *SystemMetadata* document before attempting to\n            update, otherwise an error will be thrown to prevent conflicts. The\n            Coordinating Node must set this optional field when it receives the\n            system metadata document. ')

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_SystemMetadata_identifier', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1366, 6), )

    
    identifier = property(__identifier.value, __identifier.set, None, 'The :term:`identifier` is a unique Unicode string\n          that is used to canonically name and identify the object in DataONE.\n          Each object in DataONE is immutable, and therefore all objects must\n          have a unique Identifier. If two objects are related to one another\n          (such as one object is a more recent version of another object),\n          each of these two objects will have unique identifiers. The\n          relationship among the objects is specified in other metadata fields\n          (see *Obsoletes* and *ObsoletedBy*), but this does not preclude the\n          inclusion of version information in the identifier string. However,\n          DataONE treats all Identifiers as opaque and will not try to infer\n          versioning semantics based on the content of the Identifiers --\n          rather, this information is found in the *Obsoletes* and\n          *ObsoletedBy* fields. Note that identifiers are used in a number of\n          REST API calls as parts of the URL path. As such, all special\n          characters such as "/", " ", "+", "\\", "%" must be properly encoded,\n          e.g. "%2F", "%20", "%2B", "%5C", "%25" respectively when used in\n          REST method calls. See RFC3896_ for more details. For example, the\n          :func:`MNRead.get()` call for an object with identifier:``http://some.location.name/mydata.cgi?id=2088``would be:``http://mn1.server.name/mn/v1/object/http:%2F%2Fsome.location.name%2Fmydata.cgi%3Fid%3D2088``.. _RFC3896: http://www.ietf.org/rfc/rfc3896.txt ')

    
    # Element formatId uses Python identifier formatId
    __formatId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'formatId'), 'formatId', '__httpns_dataone_orgservicetypesv1_SystemMetadata_formatId', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1392, 6), )

    
    formatId = property(__formatId.value, __formatId.set, None, ' Designation of the standard or format that should\n          be used to interpret the contents of the object, drawn from\n          controlled list of formats that are provided by the DataONE\n          :class:`Types.ObjectFormat` service. DataONE maintains a list of\n          formats in use and their canonical FormatIdentifiers. The format\n          identifier for an object should imply its mime type for data objects\n          and metadata type and serialization format for metadata objects.\n          Examples include the namespace of the EML 2.1 metadata\n          specification, the DOCTYPE of the Biological Data Profile, the mime\n          type of ``text/csv`` files, and the canonical name of the NetCDF\n          specification. ')

    
    # Element size uses Python identifier size
    __size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'size'), 'size', '__httpns_dataone_orgservicetypesv1_SystemMetadata_size', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1407, 6), )

    
    size = property(__size.value, __size.set, None, ' The size of the object in octets (8-bit bytes).\n          ')

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'checksum'), 'checksum', '__httpns_dataone_orgservicetypesv1_SystemMetadata_checksum', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1413, 6), )

    
    checksum = property(__checksum.value, __checksum.set, None, ' A calculated hash value used to validate object\n          integrity over time and after network transfers. The value is\n          calculated using a standard hashing algorithm that is accepted by\n          DataONE and that is indicated in the included *ChecksumAlgorithm*\n          attribute. ')

    
    # Element submitter uses Python identifier submitter
    __submitter = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'submitter'), 'submitter', '__httpns_dataone_orgservicetypesv1_SystemMetadata_submitter', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1422, 6), )

    
    submitter = property(__submitter.value, __submitter.set, None, ':term:`Subject` who submitted the associated\n          abject to the DataONE Member Node. The Member Node must set this\n          field when it receives the system metadata document from a client\n          (the field is optional from the client perspective, but is required\n          when a MN creates an object). By default, the submitter lacks any\n          rights to modify an object, so care must be taken to set\n          *rightsHolder* and *accessPolicy* correctly with a reference to the\n          subject of the submitter if the submitter is to be able to make\n          further changes to the object.')

    
    # Element rightsHolder uses Python identifier rightsHolder
    __rightsHolder = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rightsHolder'), 'rightsHolder', '__httpns_dataone_orgservicetypesv1_SystemMetadata_rightsHolder', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1435, 6), )

    
    rightsHolder = property(__rightsHolder.value, __rightsHolder.set, None, ':term:`Subject` that has ultimate authority for\n          the object and is authorized to make all decisions regarding the\n          disposition and accessibility of the object. The *rightsHolder* has\n          all rights to access the object, update the object, and grant\n          permissions for the object, even if additional access control rules\n          are not specified for the object. Typically, the *rightsHolder*\n          field would be set to the name of the subject submitting an object,\n          so that the person can make further changes later. By default, the\n          *submitter* lacks any rights to modify an object, so care must be\n          taken to set *rightsHolder* and *accessPolicy* correctly with a\n          reference to the subject of the *submitter* if the *submitter* is to\n          be able to make further changes to the object. ')

    
    # Element accessPolicy uses Python identifier accessPolicy
    __accessPolicy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'accessPolicy'), 'accessPolicy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_accessPolicy', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1451, 6), )

    
    accessPolicy = property(__accessPolicy.value, __accessPolicy.set, None, 'The *accessPolicy* determines which\n          :term:`Subjects` are allowed to make changes to an object in\n          addition to the *rightsHolder* and *authoritativeMemberNode*. The\n          *accessPolicy* is set for an object during a\n          :func:`MNStorage.create` or :func:`MNStorage.update` call, or when\n          *SystemMetadata* is updated on the Coordinating Node via various\n          mechanisms. This policy replaces any existing policies that might\n          exist for the object. Member Nodes that house an object are\n          obligated to enforce the *accessPolicy* for that\n          object.')

    
    # Element replicationPolicy uses Python identifier replicationPolicy
    __replicationPolicy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'replicationPolicy'), 'replicationPolicy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_replicationPolicy', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1466, 6), )

    
    replicationPolicy = property(__replicationPolicy.value, __replicationPolicy.set, None, 'A controlled list of policy choices that determine\n          how many replicas should be maintained for a given object and any\n          preferences or requirements as to which Member Nodes should be\n          allowed to house the replicas. The policy determines whether\n          replication is allowed, the number of replicas desired, the list of\n          preferred nodes to hold the replicas, and a list of blocked nodes on\n          which replicas must not exist.')

    
    # Element obsoletes uses Python identifier obsoletes
    __obsoletes = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'obsoletes'), 'obsoletes', '__httpns_dataone_orgservicetypesv1_SystemMetadata_obsoletes', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1478, 6), )

    
    obsoletes = property(__obsoletes.value, __obsoletes.set, None, 'The :term:`Identifier` of an object that is a\n          prior version of the object described in this system metadata record\n          and that is obsoleted by this object. When an object is obsoleted,\n          it is removed from all DataONE search indices but is still\n          accessible from the :func:`CNRead.get` service. ')

    
    # Element obsoletedBy uses Python identifier obsoletedBy
    __obsoletedBy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'obsoletedBy'), 'obsoletedBy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_obsoletedBy', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1488, 6), )

    
    obsoletedBy = property(__obsoletedBy.value, __obsoletedBy.set, None, 'The :term:`Identifier` of an object that is a\n          subsequent version of the object described in this system metadata\n          record and that therefore obsoletes this object. When an object is\n          obsoleted, it is removed from all DataONE search indices but is\n          still accessible from the :func:`CNRead.get` service.\n          ')

    
    # Element archived uses Python identifier archived
    __archived = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'archived'), 'archived', '__httpns_dataone_orgservicetypesv1_SystemMetadata_archived', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1499, 6), )

    
    archived = property(__archived.value, __archived.set, None, 'A boolean flag, set to *true* if the object has\n          been classified as archived. An archived object does not show up in\n          search indexes in DataONE, but is still accessible via the CNRead\n          and MNRead services if associated access polices allow. The field is\n          optional, and if absent, then objects are implied to not be\n          archived, which is the same as setting archived to\n          *false*.')

    
    # Element dateUploaded uses Python identifier dateUploaded
    __dateUploaded = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dateUploaded'), 'dateUploaded', '__httpns_dataone_orgservicetypesv1_SystemMetadata_dateUploaded', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1510, 6), )

    
    dateUploaded = property(__dateUploaded.value, __dateUploaded.set, None, 'Date and time (UTC) that the object was uploaded\n          into the DataONE system, which is typically the time that the object\n          is first created on a Member Node using the :func:`MNStorage.create`\n          operation. Note this is independent of the publication or release\n          date of the object. The Member Node must set this optional field\n          when it receives the system metadata document from a\n          client.')

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpns_dataone_orgservicetypesv1_SystemMetadata_dateSysMetadataModified', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1522, 6), )

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, ' Date and time (UTC) that this system metadata\n          record was last modified in the DataONE system. This is the same\n          timestamp as *dateUploaded* until the system metadata is further\n          modified. The Member Node must set this optional field when it\n          receives the system metadata document from a\n          client.')

    
    # Element originMemberNode uses Python identifier originMemberNode
    __originMemberNode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'originMemberNode'), 'originMemberNode', '__httpns_dataone_orgservicetypesv1_SystemMetadata_originMemberNode', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1533, 6), )

    
    originMemberNode = property(__originMemberNode.value, __originMemberNode.set, None, 'A reference to the Member Node that originally\n          uploaded the associated object. This value should never change, even\n          if the Member Node ceases to exist. ')

    
    # Element authoritativeMemberNode uses Python identifier authoritativeMemberNode
    __authoritativeMemberNode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'authoritativeMemberNode'), 'authoritativeMemberNode', '__httpns_dataone_orgservicetypesv1_SystemMetadata_authoritativeMemberNode', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1541, 6), )

    
    authoritativeMemberNode = property(__authoritativeMemberNode.value, __authoritativeMemberNode.set, None, ' A reference to the Member Node that acts as the\n          authoritative source for an object in the system. The\n          *authoritativeMemberNode* will often also be the *originMemberNode*,\n          unless there has been a need to transfer authority for an object to\n          a new node, such as when a Member Node becomes defunct. The\n          *authoritativeMemberNode* has all the rights of the *rightsHolder*\n          to maintain and curate the object, including making any changes\n          necessary. ')

    
    # Element replica uses Python identifier replica
    __replica = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'replica'), 'replica', '__httpns_dataone_orgservicetypesv1_SystemMetadata_replica', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1554, 6), )

    
    replica = property(__replica.value, __replica.set, None, ' A container field used to repeatedly provide\n          several metadata fields about each replica that exists in the\n          system, or is being replicated. Note that a *replica* field exists\n          even for the Authoritative/Origin Member Nodes so that the status of\n          those objects can be tracked. ')

    _ElementMap.update({
        __serialVersion.name() : __serialVersion,
        __identifier.name() : __identifier,
        __formatId.name() : __formatId,
        __size.name() : __size,
        __checksum.name() : __checksum,
        __submitter.name() : __submitter,
        __rightsHolder.name() : __rightsHolder,
        __accessPolicy.name() : __accessPolicy,
        __replicationPolicy.name() : __replicationPolicy,
        __obsoletes.name() : __obsoletes,
        __obsoletedBy.name() : __obsoletedBy,
        __archived.name() : __archived,
        __dateUploaded.name() : __dateUploaded,
        __dateSysMetadataModified.name() : __dateSysMetadataModified,
        __originMemberNode.name() : __originMemberNode,
        __authoritativeMemberNode.name() : __authoritativeMemberNode,
        __replica.name() : __replica
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.SystemMetadata = SystemMetadata
Namespace.addCategoryObject('typeBinding', 'SystemMetadata', SystemMetadata)


# Complex type {http://ns.dataone.org/service/types/v1}Checksum with content type SIMPLE
class Checksum (pyxb.binding.basis.complexTypeDefinition):
    """Represents the value of a computed :term:`checksum`
      expressed as a hexadecimal formatted version of the message digest. Note
      that these hex values should be treated as case-insensitive strings, in
      that leading zeros must be preserved, and digests can use a mixture of
      upper and lower case letters to represent the hex values. Comparison
      algorithms MUST be able to handle any variant of these representations
      (e.g., by performing a case-insensitive string match on hex digests from
      the same algorithm)."""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Checksum')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 317, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute algorithm uses Python identifier algorithm
    __algorithm = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'algorithm'), 'algorithm', '__httpns_dataone_orgservicetypesv1_Checksum_algorithm', _module_typeBindings.ChecksumAlgorithm, required=True)
    __algorithm._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 330, 8)
    __algorithm._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 330, 8)
    
    algorithm = property(__algorithm.value, __algorithm.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __algorithm.name() : __algorithm
    })
_module_typeBindings.Checksum = Checksum
Namespace.addCategoryObject('typeBinding', 'Checksum', Checksum)


# Complex type {http://ns.dataone.org/service/types/v1}Log with content type ELEMENT_ONLY
class Log (Slice):
    """Represents a collection of :class:`Types.LogEntry`
      elements, used to transfer log information between DataONE
      components."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Log')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 420, 2)
    _ElementMap = Slice._ElementMap.copy()
    _AttributeMap = Slice._AttributeMap.copy()
    # Base type is Slice
    
    # Element logEntry uses Python identifier logEntry
    __logEntry = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'logEntry'), 'logEntry', '__httpns_dataone_orgservicetypesv1_Log_logEntry', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 429, 10), )

    
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


# Complex type {http://ns.dataone.org/service/types/v1}Node with content type ELEMENT_ONLY
class Node (pyxb.binding.basis.complexTypeDefinition):
    """A set of values that describe a member or coordinating
      node, its Internet location, and the services it supports. Several nodes
      may exist on a single physical device or hostname. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Node')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 509, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_Node_identifier', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 516, 6), )

    
    identifier = property(__identifier.value, __identifier.set, None, 'A unique identifier for the node of the form\n          ``urn:node:NODEID`` where NODEID is the node specific identifier.\n          This value MUST NOT change for future implementations of the\n          same node, whereas the *baseURL* may change in the future.\n          ')

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpns_dataone_orgservicetypesv1_Node_name', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 526, 6), )

    
    name = property(__name.value, __name.set, None, 'A human readable name of the Node. This name can\n          be used as a label in many systems to represent the node, and thus\n          should be short, but understandable. ')

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'description'), 'description', '__httpns_dataone_orgservicetypesv1_Node_description', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 533, 6), )

    
    description = property(__description.value, __description.set, None, 'Description of a Node, explaining the community it\n          serves and other relevant information about the node, such as what\n          content is maintained by this node and any other free style notes.\n          ')

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'baseURL'), 'baseURL', '__httpns_dataone_orgservicetypesv1_Node_baseURL', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 542, 6), )

    
    baseURL = property(__baseURL.value, __baseURL.set, None, 'The base URL of the node, indicating the\n           protocol, fully qualified domain name, and path to the implementing\n           service, excluding the version of the API. e.g.\n           ``https://server.example.edu/app/d1/mn`` rather than\n           ``https://server.example.edu/app/d1/mn/v1``')

    
    # Element services uses Python identifier services
    __services = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'services'), 'services', '__httpns_dataone_orgservicetypesv1_Node_services', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 551, 6), )

    
    services = property(__services.value, __services.set, None, 'A list of services that are provided by this node.\n          Used in node descriptions so that nodes can provide metadata about\n          each service they implement and support.')

    
    # Element synchronization uses Python identifier synchronization
    __synchronization = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'synchronization'), 'synchronization', '__httpns_dataone_orgservicetypesv1_Node_synchronization', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 558, 6), )

    
    synchronization = property(__synchronization.value, __synchronization.set, None, 'Configuration information for the process by which\n            content is harvested from Member Nodes to Coordinating Nodes. This\n            includes the schedule on which harvesting should occur, and metadata\n            about the last synchronization attempts for the\n            node.')

    
    # Element nodeReplicationPolicy uses Python identifier nodeReplicationPolicy
    __nodeReplicationPolicy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'nodeReplicationPolicy'), 'nodeReplicationPolicy', '__httpns_dataone_orgservicetypesv1_Node_nodeReplicationPolicy', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 568, 6), )

    
    nodeReplicationPolicy = property(__nodeReplicationPolicy.value, __nodeReplicationPolicy.set, None, 'The replication policy for this node that expresses\n            constraints on object size, total objects, source nodes, and object\n            format types. A node may want to restrict replication from only\n            certain peer nodes, may have file size limits, total allocated size\n            limits, or may want to focus on being a replica target for\n            domain-specific object formats.')

    
    # Element ping uses Python identifier ping
    __ping = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ping'), 'ping', '__httpns_dataone_orgservicetypesv1_Node_ping', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 579, 6), )

    
    ping = property(__ping.value, __ping.set, None, 'Stored results from the :func:`MNCore.ping` and\n           :func:`CNCore.ping` methods.')

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Node_subject', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 585, 6), )

    
    subject = property(__subject.value, __subject.set, None, 'The :term:`Subject` of this node, which can be\n          repeated as needed. The *Node.subject* represents the identifier of\n          the node that would be found in X.509 certificates used to securely\n          communicate with this node. Thus, it is an :term:`X.509\n          Distinguished Name` that applies to the host on which the Node is\n          operating. When (and if) this hostname changes the new subject for\n          the node would be added to the Node to track the subject that has\n          been used in various access control rules over time.\n          ')

    
    # Element contactSubject uses Python identifier contactSubject
    __contactSubject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'contactSubject'), 'contactSubject', '__httpns_dataone_orgservicetypesv1_Node_contactSubject', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 599, 6), )

    
    contactSubject = property(__contactSubject.value, __contactSubject.set, None, 'The appropriate person or group to contact\n          regarding the disposition, management, and status of this Member\n          Node. The *Node.contactSubject* is an :term:`X.509 Distinguished\n          Name` for a person or group that can be used to look up current\n          contact details (e.g., name, email address) for the contact in the\n          DataONE Identity service. DataONE uses the *contactSubject* to\n          provide notices of interest to DataONE nodes, including information\n          such as policy changes, maintenance updates, node outage\n          notifications, among other information useful for administering a\n          node. Each node that is registered with DataONE must provide at\n          least one *contactSubject* that has been :term:`verified` with\n          DataONE. ')

    
    # Attribute replicate uses Python identifier replicate
    __replicate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'replicate'), 'replicate', '__httpns_dataone_orgservicetypesv1_Node_replicate', pyxb.binding.datatypes.boolean, required=True)
    __replicate._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 617, 4)
    __replicate._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 617, 4)
    
    replicate = property(__replicate.value, __replicate.set, None, 'Set to *true* if the node is willing to be a\n        :term:`replication target`, otherwise *false*.')

    
    # Attribute synchronize uses Python identifier synchronize
    __synchronize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'synchronize'), 'synchronize', '__httpns_dataone_orgservicetypesv1_Node_synchronize', pyxb.binding.datatypes.boolean, required=True)
    __synchronize._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 623, 4)
    __synchronize._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 623, 4)
    
    synchronize = property(__synchronize.value, __synchronize.set, None, 'Set to *true* if the node should be\n        :term:`synchronized` by a Coordinating Node, otherwise\n        *false*.')

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpns_dataone_orgservicetypesv1_Node_type', _module_typeBindings.NodeType, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 630, 4)
    __type._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 630, 4)
    
    type = property(__type.value, __type.set, None, 'The type of the node (Coordinating, Member), chosen\n        from the :class:`Types.NodeType` type.')

    
    # Attribute state uses Python identifier state
    __state = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'state'), 'state', '__httpns_dataone_orgservicetypesv1_Node_state', _module_typeBindings.NodeState, required=True)
    __state._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 636, 4)
    __state._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 636, 4)
    
    state = property(__state.value, __state.set, None, 'The state of the node (*up*, *down*), chosen from\n        the :class:`Types.NodeState` type.')

    _ElementMap.update({
        __identifier.name() : __identifier,
        __name.name() : __name,
        __description.name() : __description,
        __baseURL.name() : __baseURL,
        __services.name() : __services,
        __synchronization.name() : __synchronization,
        __nodeReplicationPolicy.name() : __nodeReplicationPolicy,
        __ping.name() : __ping,
        __subject.name() : __subject,
        __contactSubject.name() : __contactSubject
    })
    _AttributeMap.update({
        __replicate.name() : __replicate,
        __synchronize.name() : __synchronize,
        __type.name() : __type,
        __state.name() : __state
    })
_module_typeBindings.Node = Node
Namespace.addCategoryObject('typeBinding', 'Node', Node)


# Complex type {http://ns.dataone.org/service/types/v1}NodeReference with content type SIMPLE
class NodeReference (pyxb.binding.basis.complexTypeDefinition):
    """A unique identifier for a DataONE Node. The
      *NodeReference* must be unique across nodes, and must always be
      assigned to one Member or Coordinating Node instance even in the event of
      the *BaseURL* or other characteristics changing."""
    _TypeDefinition = NonEmptyString
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NodeReference')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 705, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is NonEmptyString
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.NodeReference = NodeReference
Namespace.addCategoryObject('typeBinding', 'NodeReference', NodeReference)


# Complex type {http://ns.dataone.org/service/types/v1}ObjectFormatList with content type ELEMENT_ONLY
class ObjectFormatList (Slice):
    """An ObjectFormatList is the structure returned from the
      :func:`CNCore.listFormats()` method of the CN REST interface. It
      provides a list of named object formats defined in the DataONE system.
      Each :class:`Types.ObjectFormat` returned in the list describes the
      object format via its name, and future versions may contain additional
      structured content from common external typing systems.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ObjectFormatList')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 763, 2)
    _ElementMap = Slice._ElementMap.copy()
    _AttributeMap = Slice._AttributeMap.copy()
    # Base type is Slice
    
    # Element objectFormat uses Python identifier objectFormat
    __objectFormat = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'objectFormat'), 'objectFormat', '__httpns_dataone_orgservicetypesv1_ObjectFormatList_objectFormat', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 776, 10), )

    
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


# Complex type {http://ns.dataone.org/service/types/v1}ObjectList with content type ELEMENT_ONLY
class ObjectList (Slice):
    """A list of object locations (nodes) from which the
      object can be retrieved. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ObjectList')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 801, 2)
    _ElementMap = Slice._ElementMap.copy()
    _AttributeMap = Slice._AttributeMap.copy()
    # Base type is Slice
    
    # Element objectInfo uses Python identifier objectInfo
    __objectInfo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'objectInfo'), 'objectInfo', '__httpns_dataone_orgservicetypesv1_ObjectList_objectInfo', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 809, 10), )

    
    objectInfo = property(__objectInfo.value, __objectInfo.set, None, None)

    
    # Attribute count inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute start inherited from {http://ns.dataone.org/service/types/v1}Slice
    
    # Attribute total inherited from {http://ns.dataone.org/service/types/v1}Slice
    _ElementMap.update({
        __objectInfo.name() : __objectInfo
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ObjectList = ObjectList
Namespace.addCategoryObject('typeBinding', 'ObjectList', ObjectList)


# Complex type {http://ns.dataone.org/service/types/v1}ServiceMethodRestriction with content type ELEMENT_ONLY
class ServiceMethodRestriction (SubjectList):
    """Describes an optional restriction policy for a given
      method. If this element exists for a service method, its use is
      restricted, and only :term:`Subjects` listed in the list are allowed to
      invoke the method named in the *methodName*
      attribute."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ServiceMethodRestriction')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1132, 2)
    _ElementMap = SubjectList._ElementMap.copy()
    _AttributeMap = SubjectList._AttributeMap.copy()
    # Base type is SubjectList
    
    # Element subject (subject) inherited from {http://ns.dataone.org/service/types/v1}SubjectList
    
    # Attribute methodName uses Python identifier methodName
    __methodName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'methodName'), 'methodName', '__httpns_dataone_orgservicetypesv1_ServiceMethodRestriction_methodName', pyxb.binding.datatypes.string, required=True)
    __methodName._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1142, 6)
    __methodName._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1142, 6)
    
    methodName = property(__methodName.value, __methodName.set, None, 'The formal name of the method in this *Service*\n          which is to be restricted.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __methodName.name() : __methodName
    })
_module_typeBindings.ServiceMethodRestriction = ServiceMethodRestriction
Namespace.addCategoryObject('typeBinding', 'ServiceMethodRestriction', ServiceMethodRestriction)


# Complex type {http://ns.dataone.org/service/types/v1}Schedule with content type EMPTY
class Schedule (pyxb.binding.basis.complexTypeDefinition):
    """The schedule on which :term:`synchronization` will run
      for a particular node. Syntax for each time slot follows the syntax
      conventions defined by the Quartz Scheduler
      (http://www.quartz-scheduler.org/api/2.1.0/org/quartz/CronExpression.html)
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Schedule')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1187, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute hour uses Python identifier hour
    __hour = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'hour'), 'hour', '__httpns_dataone_orgservicetypesv1_Schedule_hour', _module_typeBindings.CrontabEntry, required=True)
    __hour._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1195, 4)
    __hour._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1195, 4)
    
    hour = property(__hour.value, __hour.set, None, None)

    
    # Attribute mday uses Python identifier mday
    __mday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'mday'), 'mday', '__httpns_dataone_orgservicetypesv1_Schedule_mday', _module_typeBindings.CrontabEntry, required=True)
    __mday._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1196, 4)
    __mday._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1196, 4)
    
    mday = property(__mday.value, __mday.set, None, None)

    
    # Attribute min uses Python identifier min
    __min = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'min'), 'min', '__httpns_dataone_orgservicetypesv1_Schedule_min', _module_typeBindings.CrontabEntry, required=True)
    __min._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1197, 4)
    __min._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1197, 4)
    
    min = property(__min.value, __min.set, None, None)

    
    # Attribute mon uses Python identifier mon
    __mon = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'mon'), 'mon', '__httpns_dataone_orgservicetypesv1_Schedule_mon', _module_typeBindings.CrontabEntry, required=True)
    __mon._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1198, 4)
    __mon._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1198, 4)
    
    mon = property(__mon.value, __mon.set, None, None)

    
    # Attribute sec uses Python identifier sec
    __sec = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sec'), 'sec', '__httpns_dataone_orgservicetypesv1_Schedule_sec', _module_typeBindings.CrontabEntrySeconds, required=True)
    __sec._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1199, 4)
    __sec._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1199, 4)
    
    sec = property(__sec.value, __sec.set, None, None)

    
    # Attribute wday uses Python identifier wday
    __wday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'wday'), 'wday', '__httpns_dataone_orgservicetypesv1_Schedule_wday', _module_typeBindings.CrontabEntry, required=True)
    __wday._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1200, 4)
    __wday._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1200, 4)
    
    wday = property(__wday.value, __wday.set, None, None)

    
    # Attribute year uses Python identifier year
    __year = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'year'), 'year', '__httpns_dataone_orgservicetypesv1_Schedule_year', _module_typeBindings.CrontabEntry, required=True)
    __year._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1201, 4)
    __year._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1201, 4)
    
    year = property(__year.value, __year.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __hour.name() : __hour,
        __mday.name() : __mday,
        __min.name() : __min,
        __mon.name() : __mon,
        __sec.name() : __sec,
        __wday.name() : __wday,
        __year.name() : __year
    })
_module_typeBindings.Schedule = Schedule
Namespace.addCategoryObject('typeBinding', 'Schedule', Schedule)


# Complex type {http://ns.dataone.org/service/types/v1}Subject with content type SIMPLE
class Subject (pyxb.binding.basis.complexTypeDefinition):
    """An identifier for a Person (user), Group,
      Organization, or System.The :term:`Subject` is a string that provides a formal
      name to identify a user or group in the DataONE Identity Management
      Service. The *subject* is represented by a unique, persistent,
      non-reassignable identifier string that follows the same constraints as
      :class:`Types.Identifier`. Subjects are immutable and can not be
      deleted."""
    _TypeDefinition = NonEmptyString
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Subject')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1275, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is NonEmptyString
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Subject = Subject
Namespace.addCategoryObject('typeBinding', 'Subject', Subject)


# Complex type {http://ns.dataone.org/service/types/v1}Service with content type ELEMENT_ONLY
class Service (pyxb.binding.basis.complexTypeDefinition):
    """The available Dataone Service APIs that are exposed on
      a Node. Without a restriction, all service methods are available to all
      callers. Restrictions may be placed on individual methods of the service
      to limit the service to a certain set of :term:`Subjects`. Enforcement
      of these service restrictions is incumbent on the Node service
      implementation."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Service')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1087, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element restriction uses Python identifier restriction
    __restriction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'restriction'), 'restriction', '__httpns_dataone_orgservicetypesv1_Service_restriction', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1097, 6), )

    
    restriction = property(__restriction.value, __restriction.set, None, 'A list of method names and :term:`Subjects` with\n          permission to invoke those methods.')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpns_dataone_orgservicetypesv1_Service_name', _module_typeBindings.ServiceName, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1105, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1105, 4)
    
    name = property(__name.value, __name.set, None, 'The name of the service. The valid list of entries\n        for Member Nodes includes: *MNCore*, *MNRead*, *MNAuthorization*,\n        *MNStorage*, and *MNReplication*. The valid list of entries for\n        Coordinating Nodes includes: *CNCore*, *CNRead*, *CNAuthorization*,\n        *CNIdentity*, *CNReplication*, and *CNRegister*.')

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpns_dataone_orgservicetypesv1_Service_version', _module_typeBindings.ServiceVersion, required=True)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1114, 4)
    __version._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1114, 4)
    
    version = property(__version.value, __version.set, None, 'Version of the service supported by the node.\n        Version is expressed in whole steps, no minor version identifiers are\n        used. For example, the version 1.0.0 API would be indicated by the\n        value "v1"')

    
    # Attribute available uses Python identifier available
    __available = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'available'), 'available', '__httpns_dataone_orgservicetypesv1_Service_available', pyxb.binding.datatypes.boolean)
    __available._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1122, 4)
    __available._UseLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1122, 4)
    
    available = property(__available.value, __available.set, None, 'A boolean flag indicating if the service is\n        available (*true*, default) or otherwise (*false*).\n        ')

    _ElementMap.update({
        __restriction.name() : __restriction
    })
    _AttributeMap.update({
        __name.name() : __name,
        __version.name() : __version,
        __available.name() : __available
    })
_module_typeBindings.Service = Service
Namespace.addCategoryObject('typeBinding', 'Service', Service)


# Complex type {http://ns.dataone.org/service/types/v1}Identifier with content type SIMPLE
class Identifier (pyxb.binding.basis.complexTypeDefinition):
    """An :term:`identifier` (:term:`PID`) in the DataONE
      system that is used to uniquely and globally identify an object.
      Identifiers can not be reused once assigned. Identifiers can not be
      deleted from the DataONE system.Identifiers are represented by a Unicode
      string of printable characters, excluding :term:`whitespace`. All
      representations of identifiers must be encoded in 7-bit ASCII or
      UTF-8.Identifiers have a maximum length of 800 characters,
      and a variety of other properties designed for preservation and
      longevity. Some discussion on this is described in the `PID
      documentation`_ and in decision `ticket 577`_. .. _ticket 577: https://redmine.dataone.org/issues/577
      .. _PID documentation: https://releases.dataone.org/online/api-documentation-v2.0.1/design/PIDs.html
      """
    _TypeDefinition = NonEmptyNoWhitespaceString800
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Identifier')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 396, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is NonEmptyNoWhitespaceString800
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Identifier = Identifier
Namespace.addCategoryObject('typeBinding', 'Identifier', Identifier)


accessPolicy = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'accessPolicy'), AccessPolicy, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1580, 2))
Namespace.addCategoryObject('elementBinding', accessPolicy.name().localName(), accessPolicy)

accessRule = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'accessRule'), AccessRule, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1581, 2))
Namespace.addCategoryObject('elementBinding', accessRule.name().localName(), accessRule)

checksumAlgorithmList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'checksumAlgorithmList'), ChecksumAlgorithmList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1583, 2))
Namespace.addCategoryObject('elementBinding', checksumAlgorithmList.name().localName(), checksumAlgorithmList)

group = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'group'), Group, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1584, 2))
Namespace.addCategoryObject('elementBinding', group.name().localName(), group)

logEntry = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'logEntry'), LogEntry, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1587, 2))
Namespace.addCategoryObject('elementBinding', logEntry.name().localName(), logEntry)

nodeList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'nodeList'), NodeList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1589, 2))
Namespace.addCategoryObject('elementBinding', nodeList.name().localName(), nodeList)

nodeReplicationPolicy = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'nodeReplicationPolicy'), NodeReplicationPolicy, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1591, 2))
Namespace.addCategoryObject('elementBinding', nodeReplicationPolicy.name().localName(), nodeReplicationPolicy)

objectInfo = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectInfo'), ObjectInfo, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1592, 2))
Namespace.addCategoryObject('elementBinding', objectInfo.name().localName(), objectInfo)

objectLocationList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectLocationList'), ObjectLocationList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1594, 2))
Namespace.addCategoryObject('elementBinding', objectLocationList.name().localName(), objectLocationList)

objectFormat = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectFormat'), ObjectFormat, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1595, 2))
Namespace.addCategoryObject('elementBinding', objectFormat.name().localName(), objectFormat)

person = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'person'), Person, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1597, 2))
Namespace.addCategoryObject('elementBinding', person.name().localName(), person)

replica = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'replica'), Replica, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1598, 2))
Namespace.addCategoryObject('elementBinding', replica.name().localName(), replica)

replicationPolicy = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'replicationPolicy'), ReplicationPolicy, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1599, 2))
Namespace.addCategoryObject('elementBinding', replicationPolicy.name().localName(), replicationPolicy)

services = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'services'), Services, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1602, 2))
Namespace.addCategoryObject('elementBinding', services.name().localName(), services)

session = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'session'), Session, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1604, 2))
Namespace.addCategoryObject('elementBinding', session.name().localName(), session)

subjectList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subjectList'), SubjectList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1606, 2))
Namespace.addCategoryObject('elementBinding', subjectList.name().localName(), subjectList)

subjectInfo = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subjectInfo'), SubjectInfo, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1607, 2))
Namespace.addCategoryObject('elementBinding', subjectInfo.name().localName(), subjectInfo)

synchronization = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'synchronization'), Synchronization, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1608, 2))
Namespace.addCategoryObject('elementBinding', synchronization.name().localName(), synchronization)

systemMetadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'systemMetadata'), SystemMetadata, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1609, 2))
Namespace.addCategoryObject('elementBinding', systemMetadata.name().localName(), systemMetadata)

checksum = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'checksum'), Checksum, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1582, 2))
Namespace.addCategoryObject('elementBinding', checksum.name().localName(), checksum)

log = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'log'), Log, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1586, 2))
Namespace.addCategoryObject('elementBinding', log.name().localName(), log)

node = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'node'), Node, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1588, 2))
Namespace.addCategoryObject('elementBinding', node.name().localName(), node)

nodeReference = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'nodeReference'), NodeReference, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1590, 2))
Namespace.addCategoryObject('elementBinding', nodeReference.name().localName(), nodeReference)

objectList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectList'), ObjectList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1593, 2))
Namespace.addCategoryObject('elementBinding', objectList.name().localName(), objectList)

objectFormatList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectFormatList'), ObjectFormatList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1596, 2))
Namespace.addCategoryObject('elementBinding', objectFormatList.name().localName(), objectFormatList)

schedule = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'schedule'), Schedule, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1600, 2))
Namespace.addCategoryObject('elementBinding', schedule.name().localName(), schedule)

serviceMethodRestriction = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'serviceMethodRestriction'), ServiceMethodRestriction, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1603, 2))
Namespace.addCategoryObject('elementBinding', serviceMethodRestriction.name().localName(), serviceMethodRestriction)

subject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'subject'), Subject, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1605, 2))
Namespace.addCategoryObject('elementBinding', subject.name().localName(), subject)

service = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'service'), Service, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1601, 2))
Namespace.addCategoryObject('elementBinding', service.name().localName(), service)

identifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'identifier'), Identifier, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1585, 2))
Namespace.addCategoryObject('elementBinding', identifier.name().localName(), identifier)



AccessPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allow'), AccessRule, scope=AccessPolicy, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 285, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AccessPolicy._UseForTag(pyxb.namespace.ExpandedName(None, 'allow')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 285, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AccessPolicy._Automaton = _BuildAutomaton()




AccessRule._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'subject'), Subject, scope=AccessRule, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 309, 6)))

AccessRule._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'permission'), Permission, scope=AccessRule, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 311, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AccessRule._UseForTag(pyxb.namespace.ExpandedName(None, 'subject')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 309, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AccessRule._UseForTag(pyxb.namespace.ExpandedName(None, 'permission')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 311, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AccessRule._Automaton = _BuildAutomaton_()




ChecksumAlgorithmList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'algorithm'), ChecksumAlgorithm, scope=ChecksumAlgorithmList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 343, 6)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ChecksumAlgorithmList._UseForTag(pyxb.namespace.ExpandedName(None, 'algorithm')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 343, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ChecksumAlgorithmList._Automaton = _BuildAutomaton_2()




Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'subject'), Subject, scope=Group, documentation='The unique, immutable identifier of the\n          :term:`group`. Group subjects must not be reused, and so they are\n          both immutable and can not be deleted from the DataONE\n          system.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 358, 6)))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'groupName'), NonEmptyString, scope=Group, documentation='The name of the Group.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 366, 6)))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hasMember'), Subject, scope=Group, documentation='A :term:`Subject` that is a member of this\n            group, expressed using the unique identifier for that\n            Subject.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 372, 6)))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rightsHolder'), Subject, scope=Group, documentation='Represents the list of owners of this :term:`group`.\n        All groups are readable by anyone in the DataONE system, but can only\n        be modified by subjects listed in *rightsHolder* fields. Designation\n        as a :term:`rightsHolder` allows the subject, or their equivalent\n        identities, to make changes to the mutable properties of the group,\n        including its name, membership list and rights holder list. The\n        subject of the group itself is immutable. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 380, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 372, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Group._UseForTag(pyxb.namespace.ExpandedName(None, 'subject')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 358, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Group._UseForTag(pyxb.namespace.ExpandedName(None, 'groupName')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 366, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Group._UseForTag(pyxb.namespace.ExpandedName(None, 'hasMember')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 372, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Group._UseForTag(pyxb.namespace.ExpandedName(None, 'rightsHolder')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 380, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Group._Automaton = _BuildAutomaton_3()




LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'entryId'), NonEmptyString, scope=LogEntry, documentation='A unique identifier for this log entry. The\n          identifier should be unique for a particular node; This is not drawn\n          from the same value space as other identifiers in DataONE, and so is\n          not subjec to the same restrictions.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 444, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'identifier'), Identifier, scope=LogEntry, documentation='The :term:`identifier` of the object that was the\n          target of the operation which generated this log entry.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 453, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ipAddress'), pyxb.binding.datatypes.string, scope=LogEntry, documentation='The IP address, as reported by the service receiving\n          the request, of the request origin.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 460, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'userAgent'), pyxb.binding.datatypes.string, scope=LogEntry, documentation='The user agent of the client making the request, as\n          reported in the User-Agent HTTP header.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 467, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'subject'), Subject, scope=LogEntry, documentation='The :term:`Subject` used for making the request.\n          This may be the DataONE :term:`public` user if the request is not\n          authenticated, otherwise it will be the *Subject* of the certificate\n          used for authenticating the request.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 474, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'event'), Event, scope=LogEntry, documentation='An entry from the :class:`Types.Event` enumeration\n          indicating the type of operation that triggered the log message.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 483, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dateLogged'), pyxb.binding.datatypes.dateTime, scope=LogEntry, documentation='A :class:`Types.DateTime` time stamp indicating when\n          the event triggering the log message ocurred. Note that all time\n          stamps in DataONE are in UTC.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 490, 6)))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'nodeIdentifier'), NodeReference, scope=LogEntry, documentation='The unique identifier for the node where the log\n          message was generated.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 498, 6)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'entryId')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 444, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'identifier')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 453, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'ipAddress')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 460, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'userAgent')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 467, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'subject')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 474, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'event')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 483, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'dateLogged')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 490, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, 'nodeIdentifier')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 498, 6))
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
LogEntry._Automaton = _BuildAutomaton_4()




NodeReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'maxObjectSize'), pyxb.binding.datatypes.unsignedLong, scope=NodeReplicationPolicy, documentation='An optional statement of the maximum size in octets\n          (8-bit bytes) of objects this node is willing to accept for\n          replication.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 655, 6)))

NodeReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'spaceAllocated'), pyxb.binding.datatypes.unsignedLong, scope=NodeReplicationPolicy, documentation='An optional statement of the total space in bytes\n          allocated for replication object storage on this\n          node.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 663, 6)))

NodeReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allowedNode'), NodeReference, scope=NodeReplicationPolicy, documentation='An optional, repeatable statement of a peer source\n          node from which this node is willing to replicate content, expressed\n          as a :class:`Types.NodeReference`.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 671, 6)))

NodeReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allowedObjectFormat'), ObjectFormatIdentifier, scope=NodeReplicationPolicy, documentation='An optional, repeatable statement of an object\n          format that this node is willing to replicate, expressed as a\n          :class:`Types.ObjectFormatIdentifier`.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 679, 6)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 655, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 663, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 671, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 679, 6))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(NodeReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, 'maxObjectSize')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 655, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(NodeReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, 'spaceAllocated')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 663, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(NodeReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, 'allowedNode')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 671, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(NodeReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, 'allowedObjectFormat')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 679, 6))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
NodeReplicationPolicy._Automaton = _BuildAutomaton_5()




NodeList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'node'), Node, scope=NodeList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 699, 6)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(NodeList._UseForTag(pyxb.namespace.ExpandedName(None, 'node')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 699, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
NodeList._Automaton = _BuildAutomaton_6()




ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'formatId'), ObjectFormatIdentifier, scope=ObjectFormat, documentation=' The unique identifier of the object format in the\n          DataONE Object Format Vocabulary. The identifier should comply with\n          DataONE Identifier rules, i.e. no whitespace, only UTF-8 or US-ASCII\n          printable characters.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 730, 6)))

ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'formatName'), pyxb.binding.datatypes.string, scope=ObjectFormat, documentation='For objects that are typed using a Document Type\n          Definition, this lists the well-known and accepted named version of\n          the DTD. In other cases, an appropriately unambiguous descriptive\n          name should be chosen.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 739, 6)))

ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'formatType'), pyxb.binding.datatypes.string, scope=ObjectFormat, documentation='A string field indicating whether or not this\n          format is :term:`science data` (*DATA*), :term:`science metadata`\n          (*METADATA*) or a :term:`resource map` (*RESOURCE*). If the format\n          is a self-describing data format that includes science metadata,\n          then the field should also be set to science metadata.\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 748, 6)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
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
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ObjectFormat._Automaton = _BuildAutomaton_7()




ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'identifier'), Identifier, scope=ObjectInfo, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 790, 8)))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'formatId'), ObjectFormatIdentifier, scope=ObjectInfo, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 792, 8)))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'checksum'), Checksum, scope=ObjectInfo, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 793, 8)))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=ObjectInfo, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 795, 8)))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'size'), pyxb.binding.datatypes.unsignedLong, scope=ObjectInfo, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 796, 8)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, 'identifier')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 790, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, 'formatId')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 792, 8))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, 'checksum')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 793, 8))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, 'dateSysMetadataModified')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 795, 8))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, 'size')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 796, 8))
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ObjectInfo._Automaton = _BuildAutomaton_8()




ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'nodeIdentifier'), NodeReference, scope=ObjectLocation, documentation='Identifier of the :class:`Types.Node` (the same\n          identifier used in the node registry for identifying the node).\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 827, 6)))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'baseURL'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation='The current base URL (the *baseURL* element from\n          the :class:`Types.Node` record) for services implemented on the\n          target node. Used with service version to construct a URL for\n          service calls to this node. Note that complete information on\n          services available on a Node is available from the\n          :func:`CNCore.listNodes` service. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 835, 6)))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'version'), ServiceVersion, scope=ObjectLocation, documentation='The version of services implemented on the node.\n          Used with base url to construct a URL for service calls to this\n          node. Note that complete information on services available on a Node\n          is available from the :func:`CNCore.listNodes` service.\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 845, 6)))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'url'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation='The full (absolute) URL that can be used to\n          retrieve the object using the get() method of the rest\n          interface.For example, if identifier was "ABX154", and the\n          node had a base URL of ``http://mn1.dataone.org/mn`` then the value\n          would be\n          ``http://mn1.dataone.org/mn/v1/object/ABX154``', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 855, 6)))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'preference'), pyxb.binding.datatypes.int, scope=ObjectLocation, documentation='A weighting parameter that provides a hint to the\n          caller for the relative preference for nodes from which the content\n          should be retrieved. Higher values have higher preference.\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 866, 6)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 866, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, 'nodeIdentifier')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 827, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, 'baseURL')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 835, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, 'version')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 845, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, 'url')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 855, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, 'preference')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 866, 6))
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
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ObjectLocation._Automaton = _BuildAutomaton_9()




ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'identifier'), Identifier, scope=ObjectLocationList, documentation='The :term:`identifier` of the object being\n        resolved.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 886, 4)))

ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'objectLocation'), ObjectLocation, scope=ObjectLocationList, documentation='List of nodes from which the object can be\n        retrieved', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 893, 4)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 893, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, 'identifier')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 886, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, 'objectLocation')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 893, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ObjectLocationList._Automaton = _BuildAutomaton_10()




Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'subject'), Subject, scope=Person, documentation='The unique, immutable identifier for the\n          *Person*.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 915, 6)))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'givenName'), NonEmptyString, scope=Person, documentation='The given name of the *Person*, repeatable if they\n          have more than one given name.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 922, 6)))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'familyName'), NonEmptyString, scope=Person, documentation='The family name of the *Person*.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 929, 6)))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'email'), NonEmptyString, scope=Person, documentation='The email address of the *Person*, repeatable if\n          they have more than one email address. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 935, 6)))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'isMemberOf'), Subject, scope=Person, documentation='A *group* or role in which the *Person* is a member,\n          expressed using the unique :class:`Types.Subject` identifier for\n          that :class:`Types.Group`, and repeatable if they are a member of\n          more than one group. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 942, 6)))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'equivalentIdentity'), Subject, scope=Person, documentation='An alternative but equivalent identity for the\n          :term:`principal` that has been used in alternate identity systems,\n          repeatable if more than one equivalent identity applies.\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 951, 6)))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'verified'), pyxb.binding.datatypes.boolean, scope=Person, documentation="*true* if the name and email address of the\n          *Person* have been :term:`verified` to ensure that the *givenName*\n          and *familyName* represent the real person's legal name, and that\n          the email address is correct for that person and is in the control\n          of the indicated individual. Verification occurs through an\n          established procedure within DataONE as part of the Identity\n          Management system. A Person can not change their own *verified*\n          field, but rather must be verified and changed through this DataONE\n          established process. ", location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 960, 6)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 935, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 942, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 951, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 960, 6))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Person._UseForTag(pyxb.namespace.ExpandedName(None, 'subject')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 915, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Person._UseForTag(pyxb.namespace.ExpandedName(None, 'givenName')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 922, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Person._UseForTag(pyxb.namespace.ExpandedName(None, 'familyName')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 929, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Person._UseForTag(pyxb.namespace.ExpandedName(None, 'email')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 935, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Person._UseForTag(pyxb.namespace.ExpandedName(None, 'isMemberOf')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 942, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(Person._UseForTag(pyxb.namespace.ExpandedName(None, 'equivalentIdentity')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 951, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(Person._UseForTag(pyxb.namespace.ExpandedName(None, 'verified')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 960, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Person._Automaton = _BuildAutomaton_11()




Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'replicaMemberNode'), NodeReference, scope=Replica, documentation='A reference to the Member Node that houses this\n          replica, regardless of whether it has arrived at the Member Node or\n          not. See *replicationStatus* to determine if the replica is\n          completely transferred. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1014, 6)))

Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'replicationStatus'), ReplicationStatus, scope=Replica, documentation=' The current status of this replica, indicating\n          the stage of replication process for the object. Only *completed*\n          replicas should be considered as available. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1022, 6)))

Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'replicaVerified'), pyxb.binding.datatypes.dateTime, scope=Replica, documentation=' The last date and time on which the integrity of\n          a replica was verified by the coordinating node. Verification occurs\n          by checking that the checksum of the stored object matches the\n          checksum recorded for the object in the system\n          metadata.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1029, 6)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Replica._UseForTag(pyxb.namespace.ExpandedName(None, 'replicaMemberNode')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1014, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Replica._UseForTag(pyxb.namespace.ExpandedName(None, 'replicationStatus')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1022, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Replica._UseForTag(pyxb.namespace.ExpandedName(None, 'replicaVerified')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1029, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Replica._Automaton = _BuildAutomaton_12()




ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'preferredMemberNode'), NodeReference, scope=ReplicationPolicy, documentation='Preferred Nodes are utilized over other nodes as\n          replication targets, up to the number of replicas requested. If\n          preferred nodes are unavailable, or if insufficient nodes are listed\n          as preferred to meet the requested number of replicas, then the\n          Coordinating Nodes will pick additional replica nodes for the\n          content. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1051, 6)))

ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'blockedMemberNode'), NodeReference, scope=ReplicationPolicy, documentation='The object MUST never be replicated to nodes\n          listed as *blockedMemberNodes*. Where there is a conflict between a\n          *preferredMemberNode* and a *blockedMemberNode* entry, the\n          *blockedMemberNode* entry prevails. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1062, 6)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1051, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1062, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, 'preferredMemberNode')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1051, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, 'blockedMemberNode')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1062, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ReplicationPolicy._Automaton = _BuildAutomaton_13()




Services._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'service'), Service, scope=Services, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1160, 6)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Services._UseForTag(pyxb.namespace.ExpandedName(None, 'service')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1160, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Services._Automaton = _BuildAutomaton_14()




Session._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'subject'), Subject, scope=Session, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1179, 6)))

Session._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'subjectInfo'), SubjectInfo, scope=Session, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1181, 6)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1181, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Session._UseForTag(pyxb.namespace.ExpandedName(None, 'subject')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1179, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Session._UseForTag(pyxb.namespace.ExpandedName(None, 'subjectInfo')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1181, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Session._Automaton = _BuildAutomaton_15()




Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'schedule'), Schedule, scope=Synchronization, documentation='An entry set by the Member Node indicating the\n          frequency for which synchronization should occur. This setting will\n          be influenced by the frequency with which content is updated on the\n          Member Node and the acceptable latency for detection and subsequent\n          processing of new content.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1246, 6)))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'lastHarvested'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation='The most recent modification date (UTC) of objects\n          checked during the last harvest of the node.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1256, 6)))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'lastCompleteHarvest'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation='The last time (UTC) all the data from a node was\n          pulled from a member node during a complete synchronization\n          process.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1263, 6)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1256, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1263, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, 'schedule')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1246, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, 'lastHarvested')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1256, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, 'lastCompleteHarvest')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1263, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Synchronization._Automaton = _BuildAutomaton_16()




SubjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'person'), Person, scope=SubjectInfo, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1305, 6)))

SubjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'group'), Group, scope=SubjectInfo, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1306, 6)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1305, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1306, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, 'person')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1305, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(SubjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, 'group')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1306, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SubjectInfo._Automaton = _BuildAutomaton_17()




SubjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'subject'), Subject, scope=SubjectList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1317, 6)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1317, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubjectList._UseForTag(pyxb.namespace.ExpandedName(None, 'subject')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1317, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SubjectList._Automaton = _BuildAutomaton_18()




SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'serialVersion'), pyxb.binding.datatypes.unsignedLong, scope=SystemMetadata, documentation=' A serial number maintained by the coordinating node\n            to indicate when changes have occurred to *SystemMetadata* to avoid\n            update conflicts. Clients should ensure that they have the most\n            recent version of a *SystemMetadata* document before attempting to\n            update, otherwise an error will be thrown to prevent conflicts. The\n            Coordinating Node must set this optional field when it receives the\n            system metadata document. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1354, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'identifier'), Identifier, scope=SystemMetadata, documentation='The :term:`identifier` is a unique Unicode string\n          that is used to canonically name and identify the object in DataONE.\n          Each object in DataONE is immutable, and therefore all objects must\n          have a unique Identifier. If two objects are related to one another\n          (such as one object is a more recent version of another object),\n          each of these two objects will have unique identifiers. The\n          relationship among the objects is specified in other metadata fields\n          (see *Obsoletes* and *ObsoletedBy*), but this does not preclude the\n          inclusion of version information in the identifier string. However,\n          DataONE treats all Identifiers as opaque and will not try to infer\n          versioning semantics based on the content of the Identifiers --\n          rather, this information is found in the *Obsoletes* and\n          *ObsoletedBy* fields. Note that identifiers are used in a number of\n          REST API calls as parts of the URL path. As such, all special\n          characters such as "/", " ", "+", "\\", "%" must be properly encoded,\n          e.g. "%2F", "%20", "%2B", "%5C", "%25" respectively when used in\n          REST method calls. See RFC3896_ for more details. For example, the\n          :func:`MNRead.get()` call for an object with identifier:``http://some.location.name/mydata.cgi?id=2088``would be:``http://mn1.server.name/mn/v1/object/http:%2F%2Fsome.location.name%2Fmydata.cgi%3Fid%3D2088``.. _RFC3896: http://www.ietf.org/rfc/rfc3896.txt ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1366, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'formatId'), ObjectFormatIdentifier, scope=SystemMetadata, documentation=' Designation of the standard or format that should\n          be used to interpret the contents of the object, drawn from\n          controlled list of formats that are provided by the DataONE\n          :class:`Types.ObjectFormat` service. DataONE maintains a list of\n          formats in use and their canonical FormatIdentifiers. The format\n          identifier for an object should imply its mime type for data objects\n          and metadata type and serialization format for metadata objects.\n          Examples include the namespace of the EML 2.1 metadata\n          specification, the DOCTYPE of the Biological Data Profile, the mime\n          type of ``text/csv`` files, and the canonical name of the NetCDF\n          specification. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1392, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'size'), pyxb.binding.datatypes.unsignedLong, scope=SystemMetadata, documentation=' The size of the object in octets (8-bit bytes).\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1407, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'checksum'), Checksum, scope=SystemMetadata, documentation=' A calculated hash value used to validate object\n          integrity over time and after network transfers. The value is\n          calculated using a standard hashing algorithm that is accepted by\n          DataONE and that is indicated in the included *ChecksumAlgorithm*\n          attribute. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1413, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'submitter'), Subject, scope=SystemMetadata, documentation=':term:`Subject` who submitted the associated\n          abject to the DataONE Member Node. The Member Node must set this\n          field when it receives the system metadata document from a client\n          (the field is optional from the client perspective, but is required\n          when a MN creates an object). By default, the submitter lacks any\n          rights to modify an object, so care must be taken to set\n          *rightsHolder* and *accessPolicy* correctly with a reference to the\n          subject of the submitter if the submitter is to be able to make\n          further changes to the object.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1422, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rightsHolder'), Subject, scope=SystemMetadata, documentation=':term:`Subject` that has ultimate authority for\n          the object and is authorized to make all decisions regarding the\n          disposition and accessibility of the object. The *rightsHolder* has\n          all rights to access the object, update the object, and grant\n          permissions for the object, even if additional access control rules\n          are not specified for the object. Typically, the *rightsHolder*\n          field would be set to the name of the subject submitting an object,\n          so that the person can make further changes later. By default, the\n          *submitter* lacks any rights to modify an object, so care must be\n          taken to set *rightsHolder* and *accessPolicy* correctly with a\n          reference to the subject of the *submitter* if the *submitter* is to\n          be able to make further changes to the object. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1435, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'accessPolicy'), AccessPolicy, scope=SystemMetadata, documentation='The *accessPolicy* determines which\n          :term:`Subjects` are allowed to make changes to an object in\n          addition to the *rightsHolder* and *authoritativeMemberNode*. The\n          *accessPolicy* is set for an object during a\n          :func:`MNStorage.create` or :func:`MNStorage.update` call, or when\n          *SystemMetadata* is updated on the Coordinating Node via various\n          mechanisms. This policy replaces any existing policies that might\n          exist for the object. Member Nodes that house an object are\n          obligated to enforce the *accessPolicy* for that\n          object.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1451, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'replicationPolicy'), ReplicationPolicy, scope=SystemMetadata, documentation='A controlled list of policy choices that determine\n          how many replicas should be maintained for a given object and any\n          preferences or requirements as to which Member Nodes should be\n          allowed to house the replicas. The policy determines whether\n          replication is allowed, the number of replicas desired, the list of\n          preferred nodes to hold the replicas, and a list of blocked nodes on\n          which replicas must not exist.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1466, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'obsoletes'), Identifier, scope=SystemMetadata, documentation='The :term:`Identifier` of an object that is a\n          prior version of the object described in this system metadata record\n          and that is obsoleted by this object. When an object is obsoleted,\n          it is removed from all DataONE search indices but is still\n          accessible from the :func:`CNRead.get` service. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1478, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'obsoletedBy'), Identifier, scope=SystemMetadata, documentation='The :term:`Identifier` of an object that is a\n          subsequent version of the object described in this system metadata\n          record and that therefore obsoletes this object. When an object is\n          obsoleted, it is removed from all DataONE search indices but is\n          still accessible from the :func:`CNRead.get` service.\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1488, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'archived'), pyxb.binding.datatypes.boolean, scope=SystemMetadata, documentation='A boolean flag, set to *true* if the object has\n          been classified as archived. An archived object does not show up in\n          search indexes in DataONE, but is still accessible via the CNRead\n          and MNRead services if associated access polices allow. The field is\n          optional, and if absent, then objects are implied to not be\n          archived, which is the same as setting archived to\n          *false*.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1499, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dateUploaded'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata, documentation='Date and time (UTC) that the object was uploaded\n          into the DataONE system, which is typically the time that the object\n          is first created on a Member Node using the :func:`MNStorage.create`\n          operation. Note this is independent of the publication or release\n          date of the object. The Member Node must set this optional field\n          when it receives the system metadata document from a\n          client.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1510, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata, documentation=' Date and time (UTC) that this system metadata\n          record was last modified in the DataONE system. This is the same\n          timestamp as *dateUploaded* until the system metadata is further\n          modified. The Member Node must set this optional field when it\n          receives the system metadata document from a\n          client.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1522, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'originMemberNode'), NodeReference, scope=SystemMetadata, documentation='A reference to the Member Node that originally\n          uploaded the associated object. This value should never change, even\n          if the Member Node ceases to exist. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1533, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'authoritativeMemberNode'), NodeReference, scope=SystemMetadata, documentation=' A reference to the Member Node that acts as the\n          authoritative source for an object in the system. The\n          *authoritativeMemberNode* will often also be the *originMemberNode*,\n          unless there has been a need to transfer authority for an object to\n          a new node, such as when a Member Node becomes defunct. The\n          *authoritativeMemberNode* has all the rights of the *rightsHolder*\n          to maintain and curate the object, including making any changes\n          necessary. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1541, 6)))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'replica'), Replica, scope=SystemMetadata, documentation=' A container field used to repeatedly provide\n          several metadata fields about each replica that exists in the\n          system, or is being replicated. Note that a *replica* field exists\n          even for the Authoritative/Origin Member Nodes so that the status of\n          those objects can be tracked. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1554, 6)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
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
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, True) ]))
    st_16._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SystemMetadata._Automaton = _BuildAutomaton_19()




Log._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'logEntry'), LogEntry, scope=Log, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 429, 10)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 429, 10))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Log._UseForTag(pyxb.namespace.ExpandedName(None, 'logEntry')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 429, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Log._Automaton = _BuildAutomaton_20()




Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'identifier'), NodeReference, scope=Node, documentation='A unique identifier for the node of the form\n          ``urn:node:NODEID`` where NODEID is the node specific identifier.\n          This value MUST NOT change for future implementations of the\n          same node, whereas the *baseURL* may change in the future.\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 516, 6)))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'name'), NonEmptyString, scope=Node, documentation='A human readable name of the Node. This name can\n          be used as a label in many systems to represent the node, and thus\n          should be short, but understandable. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 526, 6)))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'description'), NonEmptyString, scope=Node, documentation='Description of a Node, explaining the community it\n          serves and other relevant information about the node, such as what\n          content is maintained by this node and any other free style notes.\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 533, 6)))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'baseURL'), pyxb.binding.datatypes.anyURI, scope=Node, documentation='The base URL of the node, indicating the\n           protocol, fully qualified domain name, and path to the implementing\n           service, excluding the version of the API. e.g.\n           ``https://server.example.edu/app/d1/mn`` rather than\n           ``https://server.example.edu/app/d1/mn/v1``', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 542, 6)))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'services'), Services, scope=Node, documentation='A list of services that are provided by this node.\n          Used in node descriptions so that nodes can provide metadata about\n          each service they implement and support.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 551, 6)))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'synchronization'), Synchronization, scope=Node, documentation='Configuration information for the process by which\n            content is harvested from Member Nodes to Coordinating Nodes. This\n            includes the schedule on which harvesting should occur, and metadata\n            about the last synchronization attempts for the\n            node.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 558, 6)))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'nodeReplicationPolicy'), NodeReplicationPolicy, scope=Node, documentation='The replication policy for this node that expresses\n            constraints on object size, total objects, source nodes, and object\n            format types. A node may want to restrict replication from only\n            certain peer nodes, may have file size limits, total allocated size\n            limits, or may want to focus on being a replica target for\n            domain-specific object formats.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 568, 6)))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ping'), Ping, scope=Node, documentation='Stored results from the :func:`MNCore.ping` and\n           :func:`CNCore.ping` methods.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 579, 6)))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'subject'), Subject, scope=Node, documentation='The :term:`Subject` of this node, which can be\n          repeated as needed. The *Node.subject* represents the identifier of\n          the node that would be found in X.509 certificates used to securely\n          communicate with this node. Thus, it is an :term:`X.509\n          Distinguished Name` that applies to the host on which the Node is\n          operating. When (and if) this hostname changes the new subject for\n          the node would be added to the Node to track the subject that has\n          been used in various access control rules over time.\n          ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 585, 6)))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'contactSubject'), Subject, scope=Node, documentation='The appropriate person or group to contact\n          regarding the disposition, management, and status of this Member\n          Node. The *Node.contactSubject* is an :term:`X.509 Distinguished\n          Name` for a person or group that can be used to look up current\n          contact details (e.g., name, email address) for the contact in the\n          DataONE Identity service. DataONE uses the *contactSubject* to\n          provide notices of interest to DataONE nodes, including information\n          such as policy changes, maintenance updates, node outage\n          notifications, among other information useful for administering a\n          node. Each node that is registered with DataONE must provide at\n          least one *contactSubject* that has been :term:`verified` with\n          DataONE. ', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 599, 6)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
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
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Node._Automaton = _BuildAutomaton_21()




ObjectFormatList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'objectFormat'), ObjectFormat, scope=ObjectFormatList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 776, 10)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ObjectFormatList._UseForTag(pyxb.namespace.ExpandedName(None, 'objectFormat')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 776, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ObjectFormatList._Automaton = _BuildAutomaton_22()




ObjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'objectInfo'), ObjectInfo, scope=ObjectList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 809, 10)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 809, 10))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ObjectList._UseForTag(pyxb.namespace.ExpandedName(None, 'objectInfo')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 809, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ObjectList._Automaton = _BuildAutomaton_23()




def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1317, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ServiceMethodRestriction._UseForTag(pyxb.namespace.ExpandedName(None, 'subject')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1317, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ServiceMethodRestriction._Automaton = _BuildAutomaton_24()




Service._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'restriction'), ServiceMethodRestriction, scope=Service, documentation='A list of method names and :term:`Subjects` with\n          permission to invoke those methods.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1097, 6)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1097, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Service._UseForTag(pyxb.namespace.ExpandedName(None, 'restriction')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes.xsd', 1097, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Service._Automaton = _BuildAutomaton_25()

