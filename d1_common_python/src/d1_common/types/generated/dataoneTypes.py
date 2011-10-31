# ./d1_common/types/generated/dataoneTypes.py
# PyXB bindings for NamespaceModule
# NSM:b5056e9f5bcbaa65eac428b50fd841172c48ddf9
# Generated 2011-10-30 22:14:59.640663 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:e5c40530-0376-11e1-b554-000c294230b4')

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

    """A derived string type with at least length 1 and it must contain non-whitespace."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonEmptyString')
    _Documentation = u'A derived string type with at least length 1 and it must contain non-whitespace.'
NonEmptyString._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1L))
NonEmptyString._CF_pattern = pyxb.binding.facets.CF_pattern()
NonEmptyString._CF_pattern.addPattern(pattern=u'[\\s]*[\\S][\\s\\S]*')
NonEmptyString._InitializeFacetMap(NonEmptyString._CF_minLength,
   NonEmptyString._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'NonEmptyString', NonEmptyString)

# Atomic SimpleTypeDefinition
class CrontabEntry (pyxb.binding.datatypes.token):

    """A single value in the series that forms a single crontab entry."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CrontabEntry')
    _Documentation = u'A single value in the series that forms a single crontab entry.'
CrontabEntry._CF_pattern = pyxb.binding.facets.CF_pattern()
CrontabEntry._CF_pattern.addPattern(pattern=u'([\\?\\*\\d]{1,2}[\\-,]?)+')
CrontabEntry._InitializeFacetMap(CrontabEntry._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'CrontabEntry', CrontabEntry)

# Atomic SimpleTypeDefinition
class NonEmptyString800 (NonEmptyString):

    """ An NonEmptyString800 is a NonEmptyString string 
          with a maximum length of 800.
          """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonEmptyString800')
    _Documentation = u' An NonEmptyString800 is a NonEmptyString string \n          with a maximum length of 800.\n          '
NonEmptyString800._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(800L))
NonEmptyString800._InitializeFacetMap(NonEmptyString800._CF_maxLength)
Namespace.addCategoryObject('typeBinding', u'NonEmptyString800', NonEmptyString800)

# Atomic SimpleTypeDefinition
class NodeType (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """
	      	The type of this node, which is either "mn" for Member Nodes, and
	      	and "cn" for Coordinating Nodes.
	    	"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeType')
    _Documentation = u'\n\t      \tThe type of this node, which is either "mn" for Member Nodes, and\n\t      \tand "cn" for Coordinating Nodes.\n\t    \t'
NodeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=NodeType, enum_prefix=None)
NodeType.mn = NodeType._CF_enumeration.addEnumeration(unicode_value=u'mn')
NodeType.cn = NodeType._CF_enumeration.addEnumeration(unicode_value=u'cn')
NodeType.Monitor = NodeType._CF_enumeration.addEnumeration(unicode_value=u'Monitor')
NodeType._InitializeFacetMap(NodeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'NodeType', NodeType)

# Atomic SimpleTypeDefinition
class NodeState (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """
	      	An indicator of the current node accessibility.  Nodes that are marked "down"
	      	are inaccessible for service operations,  those that are "up" are in the
	      	normal accessible state, and "unknown" indicates that the state has not been
	      	determined yet.
	      	"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeState')
    _Documentation = u'\n\t      \tAn indicator of the current node accessibility.  Nodes that are marked "down"\n\t      \tare inaccessible for service operations,  those that are "up" are in the\n\t      \tnormal accessible state, and "unknown" indicates that the state has not been\n\t      \tdetermined yet.\n\t      \t'
NodeState._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=NodeState, enum_prefix=None)
NodeState.up = NodeState._CF_enumeration.addEnumeration(unicode_value=u'up')
NodeState.down = NodeState._CF_enumeration.addEnumeration(unicode_value=u'down')
NodeState.unknown = NodeState._CF_enumeration.addEnumeration(unicode_value=u'unknown')
NodeState._InitializeFacetMap(NodeState._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'NodeState', NodeState)

# Atomic SimpleTypeDefinition
class ObjectFormatIdentifier (NonEmptyString):

    """A string used to identify an instance of :class:`Types.ObjectFormat` and MUST
          be unique within an instance of :class:`Types.ObjectFormatList`.
          """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectFormatIdentifier')
    _Documentation = u'A string used to identify an instance of :class:`Types.ObjectFormat` and MUST\n          be unique within an instance of :class:`Types.ObjectFormatList`.\n          '
ObjectFormatIdentifier._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ObjectFormatIdentifier', ObjectFormatIdentifier)

# Atomic SimpleTypeDefinition
class ReplicationStatus (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """A controlled string value indicating the current
      state of a replica of an object.  When an object 
      identified needs to be replicated, it is added to the replication
      task queue and is marked as 'queued'; a CN node will then pick up 
      that task and request that it be replicated to a MN and marks that it
      is 'requested'; when a MN finishes replicating the object, it informs
      the CN that it is finished and it is marked as 'completed'; periodically
      the CN checks each replica to be sure it is both available and valid 
      (matching checksum with original), and if it is either unavailable in 
      invalid then it marks it as 'invalidated', which indicates that the 
      replication policy needs to be checked again. 
      """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReplicationStatus')
    _Documentation = u"A controlled string value indicating the current\n      state of a replica of an object.  When an object \n      identified needs to be replicated, it is added to the replication\n      task queue and is marked as 'queued'; a CN node will then pick up \n      that task and request that it be replicated to a MN and marks that it\n      is 'requested'; when a MN finishes replicating the object, it informs\n      the CN that it is finished and it is marked as 'completed'; periodically\n      the CN checks each replica to be sure it is both available and valid \n      (matching checksum with original), and if it is either unavailable in \n      invalid then it marks it as 'invalidated', which indicates that the \n      replication policy needs to be checked again. \n      "
ReplicationStatus._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ReplicationStatus, enum_prefix=None)
ReplicationStatus.queued = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'queued')
ReplicationStatus.requested = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'requested')
ReplicationStatus.completed = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'completed')
ReplicationStatus.invalidated = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'invalidated')
ReplicationStatus._InitializeFacetMap(ReplicationStatus._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ReplicationStatus', ReplicationStatus)

# Atomic SimpleTypeDefinition
class ChecksumAlgorithm (pyxb.binding.datatypes.string):

    """The checksum algorithm used to calculate a checksum.
      DataONE will publish a known list of algorithm names that can be supported,
      but compliant implementations must support at least SHA-1. 
      Valid entries include: SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, MD5The default checksum is *SHA-1*."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ChecksumAlgorithm')
    _Documentation = u'The checksum algorithm used to calculate a checksum.\n      DataONE will publish a known list of algorithm names that can be supported,\n      but compliant implementations must support at least SHA-1. \n      Valid entries include: SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, MD5The default checksum is *SHA-1*.'
ChecksumAlgorithm._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ChecksumAlgorithm', ChecksumAlgorithm)

# Atomic SimpleTypeDefinition
class Event (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """The controlled list of events that are logged, 
      which will include 'CREATE', 'UPDATE', 'DELETE', 'READ', 'REPLICATE',
      'SYNCHRONIZATION_FAILED' and 'REPLICATION_FAILED' events."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Event')
    _Documentation = u"The controlled list of events that are logged, \n      which will include 'CREATE', 'UPDATE', 'DELETE', 'READ', 'REPLICATE',\n      'SYNCHRONIZATION_FAILED' and 'REPLICATION_FAILED' events."
Event._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Event, enum_prefix=None)
Event.create = Event._CF_enumeration.addEnumeration(unicode_value=u'create')
Event.read = Event._CF_enumeration.addEnumeration(unicode_value=u'read')
Event.update = Event._CF_enumeration.addEnumeration(unicode_value=u'update')
Event.delete = Event._CF_enumeration.addEnumeration(unicode_value=u'delete')
Event.replicate = Event._CF_enumeration.addEnumeration(unicode_value=u'replicate')
Event.synchronization_failed = Event._CF_enumeration.addEnumeration(unicode_value=u'synchronization_failed')
Event.replication_failed = Event._CF_enumeration.addEnumeration(unicode_value=u'replication_failed')
Event._InitializeFacetMap(Event._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'Event', Event)

# Atomic SimpleTypeDefinition
class ServiceName (NonEmptyString):

    """
	      	The name of a service that is available on a Node.
	    	"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceName')
    _Documentation = u'\n\t      \tThe name of a service that is available on a Node.\n\t    \t'
ServiceName._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ServiceName', ServiceName)

# Atomic SimpleTypeDefinition
class ServiceVersion (NonEmptyString):

    """
	      	The version of a service that is available on a Node, expressed using
	      	the symbolic service level that that service implements, such as "v1" or
	      	"v2".  DataONE services are released only as major service versions; patches
	      	to services are not indicated in this version label. 
	    	"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceVersion')
    _Documentation = u'\n\t      \tThe version of a service that is available on a Node, expressed using\n\t      \tthe symbolic service level that that service implements, such as "v1" or\n\t      \t"v2".  DataONE services are released only as major service versions; patches\n\t      \tto services are not indicated in this version label. \n\t    \t'
ServiceVersion._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ServiceVersion', ServiceVersion)

# Atomic SimpleTypeDefinition
class Permission (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """A string value indicating the set of actions that
        can be performed on a resource as specified in an access policy. The
        set of permissions include the ability to read a resource (read), modify a
        resource (write), and to change the set of access control policies
        for a resource (changePermission). In addition, there is a permission
        that controls ability to execute a service (execute), and a 
        permission that controls the ability of a node to receive a replicate of
        an object from another node.
      """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Permission')
    _Documentation = u'A string value indicating the set of actions that\n        can be performed on a resource as specified in an access policy. The\n        set of permissions include the ability to read a resource (read), modify a\n        resource (write), and to change the set of access control policies\n        for a resource (changePermission). In addition, there is a permission\n        that controls ability to execute a service (execute), and a \n        permission that controls the ability of a node to receive a replicate of\n        an object from another node.\n      '
Permission._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Permission, enum_prefix=None)
Permission.read = Permission._CF_enumeration.addEnumeration(unicode_value=u'read')
Permission.write = Permission._CF_enumeration.addEnumeration(unicode_value=u'write')
Permission.changePermission = Permission._CF_enumeration.addEnumeration(unicode_value=u'changePermission')
Permission.execute = Permission._CF_enumeration.addEnumeration(unicode_value=u'execute')
Permission.replicate = Permission._CF_enumeration.addEnumeration(unicode_value=u'replicate')
Permission._InitializeFacetMap(Permission._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'Permission', Permission)

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


# Complex type Person with content type ELEMENT_ONLY
class Person (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Person')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element isMemberOf uses Python identifier isMemberOf
    __isMemberOf = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'isMemberOf'), 'isMemberOf', '__httpns_dataone_orgservicetypesv1_Person_isMemberOf', True)

    
    isMemberOf = property(__isMemberOf.value, __isMemberOf.set, None, u'A group or role in which the Principal is a\n\t\t\t\t\t\tmember, expressed using the\n\t\t\t\t\t\tunique Principal identifier for that group.')

    
    # Element verified uses Python identifier verified
    __verified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'verified'), 'verified', '__httpns_dataone_orgservicetypesv1_Person_verified', False)

    
    verified = property(__verified.value, __verified.set, None, u"True if the name and email address of the Person\n\t\t\t\t\t\thave been verified to ensure that the givenName and familyName\n\t\t\t\t\t\trepresent the real person's legal name, and that the email \n\t\t\t\t\t\taddress is correct for that person and is in the control\n\t\t\t\t\t\tof the indicated individual. Verification occurs through a\n\t\t\t\t\t\testablished procedure within DataONE as part of the Identity \n\t\t\t\t\t\tManagement system.\n\t\t\t\t\t")

    
    # Element equivalentIdentity uses Python identifier equivalentIdentity
    __equivalentIdentity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'equivalentIdentity'), 'equivalentIdentity', '__httpns_dataone_orgservicetypesv1_Person_equivalentIdentity', True)

    
    equivalentIdentity = property(__equivalentIdentity.value, __equivalentIdentity.set, None, u'An alternative but equivalent identity for the\n\t\t\t\t\t\tprincipal that has been\n\t\t\t\t\t\tused in alternate identity systems.')

    
    # Element givenName uses Python identifier givenName
    __givenName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'givenName'), 'givenName', '__httpns_dataone_orgservicetypesv1_Person_givenName', True)

    
    givenName = property(__givenName.value, __givenName.set, None, u'The given name of the Person.')

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Person_subject', False)

    
    subject = property(__subject.value, __subject.set, None, u'The unique identifier for the person.\n\t\t\t\t\t')

    
    # Element familyName uses Python identifier familyName
    __familyName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'familyName'), 'familyName', '__httpns_dataone_orgservicetypesv1_Person_familyName', False)

    
    familyName = property(__familyName.value, __familyName.set, None, u'The family name of the Person.')

    
    # Element email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'email'), 'email', '__httpns_dataone_orgservicetypesv1_Person_email', True)

    
    email = property(__email.value, __email.set, None, u'The email address of the Person.\n\t\t\t\t\t')


    _ElementMap = {
        __isMemberOf.name() : __isMemberOf,
        __verified.name() : __verified,
        __equivalentIdentity.name() : __equivalentIdentity,
        __givenName.name() : __givenName,
        __subject.name() : __subject,
        __familyName.name() : __familyName,
        __email.name() : __email
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Person', Person)


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


# Complex type Schedule with content type EMPTY
class Schedule (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Schedule')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute hour uses Python identifier hour
    __hour = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'hour'), 'hour', '__httpns_dataone_orgservicetypesv1_Schedule_hour', CrontabEntry, required=True)
    
    hour = property(__hour.value, __hour.set, None, None)

    
    # Attribute min uses Python identifier min
    __min = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'min'), 'min', '__httpns_dataone_orgservicetypesv1_Schedule_min', CrontabEntry, required=True)
    
    min = property(__min.value, __min.set, None, None)

    
    # Attribute mon uses Python identifier mon
    __mon = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mon'), 'mon', '__httpns_dataone_orgservicetypesv1_Schedule_mon', CrontabEntry, required=True)
    
    mon = property(__mon.value, __mon.set, None, None)

    
    # Attribute mday uses Python identifier mday
    __mday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mday'), 'mday', '__httpns_dataone_orgservicetypesv1_Schedule_mday', CrontabEntry, required=True)
    
    mday = property(__mday.value, __mday.set, None, None)

    
    # Attribute sec uses Python identifier sec
    __sec = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'sec'), 'sec', '__httpns_dataone_orgservicetypesv1_Schedule_sec', CrontabEntry, required=True)
    
    sec = property(__sec.value, __sec.set, None, None)

    
    # Attribute wday uses Python identifier wday
    __wday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'wday'), 'wday', '__httpns_dataone_orgservicetypesv1_Schedule_wday', CrontabEntry, required=True)
    
    wday = property(__wday.value, __wday.set, None, None)

    
    # Attribute year uses Python identifier year
    __year = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'year'), 'year', '__httpns_dataone_orgservicetypesv1_Schedule_year', CrontabEntry, required=True)
    
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


# Complex type MonitorList with content type ELEMENT_ONLY
class MonitorList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MonitorList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element monitorInfo uses Python identifier monitorInfo
    __monitorInfo = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'monitorInfo'), 'monitorInfo', '__httpns_dataone_orgservicetypesv1_MonitorList_monitorInfo', True)

    
    monitorInfo = property(__monitorInfo.value, __monitorInfo.set, None, None)


    _ElementMap = {
        __monitorInfo.name() : __monitorInfo
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MonitorList', MonitorList)


# Complex type ObjectLocationList with content type ELEMENT_ONLY
class ObjectLocationList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectLocationList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element objectLocation uses Python identifier objectLocation
    __objectLocation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectLocation'), 'objectLocation', '__httpns_dataone_orgservicetypesv1_ObjectLocationList_objectLocation', True)

    
    objectLocation = property(__objectLocation.value, __objectLocation.set, None, u'List of nodes from which the object can be\n                        retrieved')

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_ObjectLocationList_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'The identifier of the object being resolved.\n                    ')


    _ElementMap = {
        __objectLocation.name() : __objectLocation,
        __identifier.name() : __identifier
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectLocationList', ObjectLocationList)


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


# Complex type Group with content type ELEMENT_ONLY
class Group (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Group')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element hasMember uses Python identifier hasMember
    __hasMember = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'hasMember'), 'hasMember', '__httpns_dataone_orgservicetypesv1_Group_hasMember', True)

    
    hasMember = property(__hasMember.value, __hasMember.set, None, u'A Subject that is a member of this group, expressed using the\n                    unique identifier for that Subject.')

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Group_subject', False)

    
    subject = property(__subject.value, __subject.set, None, u'The unique identifier of the group.')

    
    # Element groupName uses Python identifier groupName
    __groupName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'groupName'), 'groupName', '__httpns_dataone_orgservicetypesv1_Group_groupName', False)

    
    groupName = property(__groupName.value, __groupName.set, None, u'The name of the Group.')


    _ElementMap = {
        __hasMember.name() : __hasMember,
        __subject.name() : __subject,
        __groupName.name() : __groupName
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Group', Group)


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


# Complex type ReplicationPolicy with content type ELEMENT_ONLY
class ReplicationPolicy (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReplicationPolicy')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element blockedMemberNode uses Python identifier blockedMemberNode
    __blockedMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'blockedMemberNode'), 'blockedMemberNode', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_blockedMemberNode', True)

    
    blockedMemberNode = property(__blockedMemberNode.value, __blockedMemberNode.set, None, u'The object MUST never be replicated to nodes \n                        listed as blockedMemberNodes. Where there is a conflict between \n                        a preferredMemberNode and a blockedMemberNode entry, the \n                        blockedMemberNode entry prevails.\n                    ')

    
    # Element preferredMemberNode uses Python identifier preferredMemberNode
    __preferredMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'preferredMemberNode'), 'preferredMemberNode', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_preferredMemberNode', True)

    
    preferredMemberNode = property(__preferredMemberNode.value, __preferredMemberNode.set, None, u'Nodes listed here have preference over other nodes for \n                    replication targets.\n                ')

    
    # Attribute replicationAllowed uses Python identifier replicationAllowed
    __replicationAllowed = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'replicationAllowed'), 'replicationAllowed', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_replicationAllowed', pyxb.binding.datatypes.boolean)
    
    replicationAllowed = property(__replicationAllowed.value, __replicationAllowed.set, None, None)

    
    # Attribute numberReplicas uses Python identifier numberReplicas
    __numberReplicas = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'numberReplicas'), 'numberReplicas', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_numberReplicas', pyxb.binding.datatypes.int)
    
    numberReplicas = property(__numberReplicas.value, __numberReplicas.set, None, None)


    _ElementMap = {
        __blockedMemberNode.name() : __blockedMemberNode,
        __preferredMemberNode.name() : __preferredMemberNode
    }
    _AttributeMap = {
        __replicationAllowed.name() : __replicationAllowed,
        __numberReplicas.name() : __numberReplicas
    }
Namespace.addCategoryObject('typeBinding', u'ReplicationPolicy', ReplicationPolicy)


# Complex type ObjectFormat with content type ELEMENT_ONLY
class ObjectFormat (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectFormat')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element formatType uses Python identifier formatType
    __formatType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'formatType'), 'formatType', '__httpns_dataone_orgservicetypesv1_ObjectFormat_formatType', False)

    
    formatType = property(__formatType.value, __formatType.set, None, u'A string field indicating whether or not this \n            format is science data(DATA), science metadata(METADATA) or a \n            resource map(RESOURCE).  If the format is a self-describing data \n            format that includes science metadata, then the field should also be \n            set to science metadata.\n            ')

    
    # Element formatId uses Python identifier formatId
    __formatId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'formatId'), 'formatId', '__httpns_dataone_orgservicetypesv1_ObjectFormat_formatId', False)

    
    formatId = property(__formatId.value, __formatId.set, None, u'\n                  The unique identifier of the object format in the DataONE\n                  Object Format Vocabulary.  The identifier should comply with\n                  DataONE Identifier rules, i.e. no whitespace, only UTF-8 or \n                  US-ASCII printable characters.\n              ')

    
    # Element formatName uses Python identifier formatName
    __formatName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'formatName'), 'formatName', '__httpns_dataone_orgservicetypesv1_ObjectFormat_formatName', False)

    
    formatName = property(__formatName.value, __formatName.set, None, u'\n              For objects that are typed using a Document Type Definition, \n              this lists the well-known and accepted named version of the DTD.\n            ')


    _ElementMap = {
        __formatType.name() : __formatType,
        __formatId.name() : __formatId,
        __formatName.name() : __formatName
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectFormat', ObjectFormat)


# Complex type ServiceMethodRestriction with content type ELEMENT_ONLY
class ServiceMethodRestriction (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceMethodRestriction')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element allowed uses Python identifier allowed
    __allowed = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'allowed'), 'allowed', '__httpns_dataone_orgservicetypesv1_ServiceMethodRestriction_allowed', False)

    
    allowed = property(__allowed.value, __allowed.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesv1_ServiceMethodRestriction_name', pyxb.binding.datatypes.NMTOKEN)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute rest uses Python identifier rest
    __rest = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'rest'), 'rest', '__httpns_dataone_orgservicetypesv1_ServiceMethodRestriction_rest', pyxb.binding.datatypes.token, required=True)
    
    rest = property(__rest.value, __rest.set, None, None)


    _ElementMap = {
        __allowed.name() : __allowed
    }
    _AttributeMap = {
        __name.name() : __name,
        __rest.name() : __rest
    }
Namespace.addCategoryObject('typeBinding', u'ServiceMethodRestriction', ServiceMethodRestriction)


# Complex type MonitorInfo with content type ELEMENT_ONLY
class MonitorInfo (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MonitorInfo')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element count uses Python identifier count
    __count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'count'), 'count', '__httpns_dataone_orgservicetypesv1_MonitorInfo_count', False)

    
    count = property(__count.value, __count.set, None, None)

    
    # Element date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'date'), 'date', '__httpns_dataone_orgservicetypesv1_MonitorInfo_date', False)

    
    date = property(__date.value, __date.set, None, None)


    _ElementMap = {
        __count.name() : __count,
        __date.name() : __date
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MonitorInfo', MonitorInfo)


# Complex type Identifier with content type SIMPLE
class Identifier (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = NonEmptyString800
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Identifier')
    # Base type is NonEmptyString800

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Identifier', Identifier)


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


# Complex type Ping with content type EMPTY
class Ping (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Ping')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute lastSuccess uses Python identifier lastSuccess
    __lastSuccess = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'lastSuccess'), 'lastSuccess', '__httpns_dataone_orgservicetypesv1_Ping_lastSuccess', pyxb.binding.datatypes.dateTime)
    
    lastSuccess = property(__lastSuccess.value, __lastSuccess.set, None, u'\n                    The date time value of the last time a successful ping was performed.\n                ')

    
    # Attribute success uses Python identifier success
    __success = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'success'), 'success', '__httpns_dataone_orgservicetypesv1_Ping_success', pyxb.binding.datatypes.boolean)
    
    success = property(__success.value, __success.set, None, u'A boolean flag indicating TRUE if the node was reached by the last \n                    :func:`MNCore.ping` call, otherwise FALSE')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __lastSuccess.name() : __lastSuccess,
        __success.name() : __success
    }
Namespace.addCategoryObject('typeBinding', u'Ping', Ping)


# Complex type Slice with content type EMPTY
class Slice (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Slice')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute count uses Python identifier count
    __count = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'count'), 'count', '__httpns_dataone_orgservicetypesv1_Slice_count', pyxb.binding.datatypes.int, required=True)
    
    count = property(__count.value, __count.set, None, None)

    
    # Attribute start uses Python identifier start
    __start = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'start'), 'start', '__httpns_dataone_orgservicetypesv1_Slice_start', pyxb.binding.datatypes.int, required=True)
    
    start = property(__start.value, __start.set, None, None)

    
    # Attribute total uses Python identifier total
    __total = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'total'), 'total', '__httpns_dataone_orgservicetypesv1_Slice_total', pyxb.binding.datatypes.int, required=True)
    
    total = property(__total.value, __total.set, None, None)


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


# Complex type Node with content type ELEMENT_ONLY
class Node (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Node')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ping uses Python identifier ping
    __ping = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ping'), 'ping', '__httpns_dataone_orgservicetypesv1_Node_ping', False)

    
    ping = property(__ping.value, __ping.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_Node_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'A unique identifier for the node. This may initially be the same as the\n                        baseURL, however this value should not change for future implementations of the same\n                        node, whereas the baseURL may change in the future. \n                    ')

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesv1_Node_name', False)

    
    name = property(__name.value, __name.set, None, u'A human readable name of the Node. \n                        The name of the node is being used in Mercury currently to assign a path,\n                        so format should be consistent with dataone directory naming conventions\n                    ')

    
    # Element contactSubject uses Python identifier contactSubject
    __contactSubject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'contactSubject'), 'contactSubject', '__httpns_dataone_orgservicetypesv1_Node_contactSubject', True)

    
    contactSubject = property(__contactSubject.value, __contactSubject.set, None, u'The appropriate person or group to contact regarding the disposition, \n                    management, and status of this Member Node. The Node.contactSubject is\n                    an X.509 Distinguished Name for a person or group that can be used to look up current \n                    contact details (e.g., name, email address) for the contact in the DataONE Identity service.\n                    DataONE uses the subjectContact to provide notices of interest to DataONE nodes, including \n                    information such as policy changes, maintenance updates, node outage notifications, among \n                    other information useful for administering a node. Each node that is registered with DataONE\n                    must provide at least one subjectContact that has been verified with DataONE.\n                    ')

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__httpns_dataone_orgservicetypesv1_Node_description', False)

    
    description = property(__description.value, __description.set, None, u'Description of content maintained by this node and any other free style\n                        notes. May be we should allow CDATA element with the purpose of using for display\n                    ')

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Node_subject', True)

    
    subject = property(__subject.value, __subject.set, None, u'The Subject of this node, which can be repeated as needed.  \n                    The Node.subject represents the identifier of the node that would be found in X.509 \n                    certificates that would be used to securely communicate with this node.  Thus, it is\n                    an X.509 Distinguished Name that applies to the host on which the Node is operating. \n                    When (and if) this hostname changes the new subject for the node would be added to the\n                    Node to track the subject that has been used in various access control rules over time.\n                    ')

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'baseURL'), 'baseURL', '__httpns_dataone_orgservicetypesv1_Node_baseURL', False)

    
    baseURL = property(__baseURL.value, __baseURL.set, None, None)

    
    # Element services uses Python identifier services
    __services = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'services'), 'services', '__httpns_dataone_orgservicetypesv1_Node_services', False)

    
    services = property(__services.value, __services.set, None, None)

    
    # Element synchronization uses Python identifier synchronization
    __synchronization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'synchronization'), 'synchronization', '__httpns_dataone_orgservicetypesv1_Node_synchronization', False)

    
    synchronization = property(__synchronization.value, __synchronization.set, None, None)

    
    # Attribute synchronize uses Python identifier synchronize
    __synchronize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'synchronize'), 'synchronize', '__httpns_dataone_orgservicetypesv1_Node_synchronize', pyxb.binding.datatypes.boolean, required=True)
    
    synchronize = property(__synchronize.value, __synchronize.set, None, None)

    
    # Attribute state uses Python identifier state
    __state = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'state'), 'state', '__httpns_dataone_orgservicetypesv1_Node_state', NodeState, required=True)
    
    state = property(__state.value, __state.set, None, None)

    
    # Attribute replicate uses Python identifier replicate
    __replicate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'replicate'), 'replicate', '__httpns_dataone_orgservicetypesv1_Node_replicate', pyxb.binding.datatypes.boolean, required=True)
    
    replicate = property(__replicate.value, __replicate.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'type'), 'type', '__httpns_dataone_orgservicetypesv1_Node_type', NodeType, required=True)
    
    type = property(__type.value, __type.set, None, None)


    _ElementMap = {
        __ping.name() : __ping,
        __identifier.name() : __identifier,
        __name.name() : __name,
        __contactSubject.name() : __contactSubject,
        __description.name() : __description,
        __subject.name() : __subject,
        __baseURL.name() : __baseURL,
        __services.name() : __services,
        __synchronization.name() : __synchronization
    }
    _AttributeMap = {
        __synchronize.name() : __synchronize,
        __state.name() : __state,
        __replicate.name() : __replicate,
        __type.name() : __type
    }
Namespace.addCategoryObject('typeBinding', u'Node', Node)


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


# Complex type ObjectLocation with content type ELEMENT_ONLY
class ObjectLocation (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectLocation')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element preference uses Python identifier preference
    __preference = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'preference'), 'preference', '__httpns_dataone_orgservicetypesv1_ObjectLocation_preference', False)

    
    preference = property(__preference.value, __preference.set, None, u'A weighting parameter that provides a hint to the caller \n                        for the relative preference for nodes from which the content should be retrieved.\n                    ')

    
    # Element nodeIdentifier uses Python identifier nodeIdentifier
    __nodeIdentifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), 'nodeIdentifier', '__httpns_dataone_orgservicetypesv1_ObjectLocation_nodeIdentifier', False)

    
    nodeIdentifier = property(__nodeIdentifier.value, __nodeIdentifier.set, None, u'Identifier of the node (the same identifier used\n                        in the node registry for identifying the node.\n                    ')

    
    # Element url uses Python identifier url
    __url = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'url'), 'url', '__httpns_dataone_orgservicetypesv1_ObjectLocation_url', False)

    
    url = property(__url.value, __url.set, None, u'The full (absolute) URL that can be used to\n                        retrieve the object using the get() method of the rest interface.\n                    For example, if identifer\n                        was "ABX154", and the node had a base URL of ``http://mn1.dataone.org/mn``\n                        then the value would be ``http://mn1.dataone.org/mn/object/ABX154``')

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'baseURL'), 'baseURL', '__httpns_dataone_orgservicetypesv1_ObjectLocation_baseURL', False)

    
    baseURL = property(__baseURL.value, __baseURL.set, None, u'The current base URL for services implemented on the target node.\n                    ')


    _ElementMap = {
        __preference.name() : __preference,
        __nodeIdentifier.name() : __nodeIdentifier,
        __url.name() : __url,
        __baseURL.name() : __baseURL
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectLocation', ObjectLocation)


# Complex type Replica with content type ELEMENT_ONLY
class Replica (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Replica')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element replicaVerified uses Python identifier replicaVerified
    __replicaVerified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicaVerified'), 'replicaVerified', '__httpns_dataone_orgservicetypesv1_Replica_replicaVerified', False)

    
    replicaVerified = property(__replicaVerified.value, __replicaVerified.set, None, None)

    
    # Element replicaMemberNode uses Python identifier replicaMemberNode
    __replicaMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicaMemberNode'), 'replicaMemberNode', '__httpns_dataone_orgservicetypesv1_Replica_replicaMemberNode', False)

    
    replicaMemberNode = property(__replicaMemberNode.value, __replicaMemberNode.set, None, None)

    
    # Element replicationStatus uses Python identifier replicationStatus
    __replicationStatus = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicationStatus'), 'replicationStatus', '__httpns_dataone_orgservicetypesv1_Replica_replicationStatus', False)

    
    replicationStatus = property(__replicationStatus.value, __replicationStatus.set, None, None)


    _ElementMap = {
        __replicaVerified.name() : __replicaVerified,
        __replicaMemberNode.name() : __replicaMemberNode,
        __replicationStatus.name() : __replicationStatus
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Replica', Replica)


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


# Complex type Synchronization with content type ELEMENT_ONLY
class Synchronization (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Synchronization')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element lastCompleteHarvest uses Python identifier lastCompleteHarvest
    __lastCompleteHarvest = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), 'lastCompleteHarvest', '__httpns_dataone_orgservicetypesv1_Synchronization_lastCompleteHarvest', False)

    
    lastCompleteHarvest = property(__lastCompleteHarvest.value, __lastCompleteHarvest.set, None, u'The last time all the data from a node was pulled from a member node\n                    ')

    
    # Element schedule uses Python identifier schedule
    __schedule = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'schedule'), 'schedule', '__httpns_dataone_orgservicetypesv1_Synchronization_schedule', False)

    
    schedule = property(__schedule.value, __schedule.set, None, None)

    
    # Element lastHarvested uses Python identifier lastHarvested
    __lastHarvested = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastHarvested'), 'lastHarvested', '__httpns_dataone_orgservicetypesv1_Synchronization_lastHarvested', False)

    
    lastHarvested = property(__lastHarvested.value, __lastHarvested.set, None, u'The last time the mn sychronization daemon ran and found new data to synchronize\n                    ')


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
    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_LogEntry_subject', False)

    
    subject = property(__subject.value, __subject.set, None, None)

    
    # Element dateLogged uses Python identifier dateLogged
    __dateLogged = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateLogged'), 'dateLogged', '__httpns_dataone_orgservicetypesv1_LogEntry_dateLogged', False)

    
    dateLogged = property(__dateLogged.value, __dateLogged.set, None, None)

    
    # Element memberNode uses Python identifier memberNode
    __memberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'memberNode'), 'memberNode', '__httpns_dataone_orgservicetypesv1_LogEntry_memberNode', False)

    
    memberNode = property(__memberNode.value, __memberNode.set, None, None)

    
    # Element event uses Python identifier event
    __event = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'event'), 'event', '__httpns_dataone_orgservicetypesv1_LogEntry_event', False)

    
    event = property(__event.value, __event.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_LogEntry_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element ipAddress uses Python identifier ipAddress
    __ipAddress = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ipAddress'), 'ipAddress', '__httpns_dataone_orgservicetypesv1_LogEntry_ipAddress', False)

    
    ipAddress = property(__ipAddress.value, __ipAddress.set, None, None)

    
    # Element entryId uses Python identifier entryId
    __entryId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'entryId'), 'entryId', '__httpns_dataone_orgservicetypesv1_LogEntry_entryId', False)

    
    entryId = property(__entryId.value, __entryId.set, None, None)

    
    # Element userAgent uses Python identifier userAgent
    __userAgent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'userAgent'), 'userAgent', '__httpns_dataone_orgservicetypesv1_LogEntry_userAgent', False)

    
    userAgent = property(__userAgent.value, __userAgent.set, None, None)


    _ElementMap = {
        __subject.name() : __subject,
        __dateLogged.name() : __dateLogged,
        __memberNode.name() : __memberNode,
        __event.name() : __event,
        __identifier.name() : __identifier,
        __ipAddress.name() : __ipAddress,
        __entryId.name() : __entryId,
        __userAgent.name() : __userAgent
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LogEntry', LogEntry)


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


# Complex type SystemMetadata with content type ELEMENT_ONLY
class SystemMetadata (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SystemMetadata')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element dateUploaded uses Python identifier dateUploaded
    __dateUploaded = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateUploaded'), 'dateUploaded', '__httpns_dataone_orgservicetypesv1_SystemMetadata_dateUploaded', False)

    
    dateUploaded = property(__dateUploaded.value, __dateUploaded.set, None, None)

    
    # Element submitter uses Python identifier submitter
    __submitter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'submitter'), 'submitter', '__httpns_dataone_orgservicetypesv1_SystemMetadata_submitter', False)

    
    submitter = property(__submitter.value, __submitter.set, None, None)

    
    # Element rightsHolder uses Python identifier rightsHolder
    __rightsHolder = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'rightsHolder'), 'rightsHolder', '__httpns_dataone_orgservicetypesv1_SystemMetadata_rightsHolder', False)

    
    rightsHolder = property(__rightsHolder.value, __rightsHolder.set, None, None)

    
    # Element serialVersion uses Python identifier serialVersion
    __serialVersion = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'serialVersion'), 'serialVersion', '__httpns_dataone_orgservicetypesv1_SystemMetadata_serialVersion', False)

    
    serialVersion = property(__serialVersion.value, __serialVersion.set, None, None)

    
    # Element accessPolicy uses Python identifier accessPolicy
    __accessPolicy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'accessPolicy'), 'accessPolicy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_accessPolicy', False)

    
    accessPolicy = property(__accessPolicy.value, __accessPolicy.set, None, None)

    
    # Element replicationPolicy uses Python identifier replicationPolicy
    __replicationPolicy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicationPolicy'), 'replicationPolicy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_replicationPolicy', False)

    
    replicationPolicy = property(__replicationPolicy.value, __replicationPolicy.set, None, None)

    
    # Element originMemberNode uses Python identifier originMemberNode
    __originMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'originMemberNode'), 'originMemberNode', '__httpns_dataone_orgservicetypesv1_SystemMetadata_originMemberNode', False)

    
    originMemberNode = property(__originMemberNode.value, __originMemberNode.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_SystemMetadata_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element authoritativeMemberNode uses Python identifier authoritativeMemberNode
    __authoritativeMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode'), 'authoritativeMemberNode', '__httpns_dataone_orgservicetypesv1_SystemMetadata_authoritativeMemberNode', False)

    
    authoritativeMemberNode = property(__authoritativeMemberNode.value, __authoritativeMemberNode.set, None, None)

    
    # Element replica uses Python identifier replica
    __replica = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replica'), 'replica', '__httpns_dataone_orgservicetypesv1_SystemMetadata_replica', True)

    
    replica = property(__replica.value, __replica.set, None, None)

    
    # Element formatId uses Python identifier formatId
    __formatId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'formatId'), 'formatId', '__httpns_dataone_orgservicetypesv1_SystemMetadata_formatId', False)

    
    formatId = property(__formatId.value, __formatId.set, None, None)

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__httpns_dataone_orgservicetypesv1_SystemMetadata_checksum', False)

    
    checksum = property(__checksum.value, __checksum.set, None, None)

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpns_dataone_orgservicetypesv1_SystemMetadata_dateSysMetadataModified', False)

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, None)

    
    # Element size uses Python identifier size
    __size = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'size'), 'size', '__httpns_dataone_orgservicetypesv1_SystemMetadata_size', False)

    
    size = property(__size.value, __size.set, None, None)

    
    # Element obsoletes uses Python identifier obsoletes
    __obsoletes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'obsoletes'), 'obsoletes', '__httpns_dataone_orgservicetypesv1_SystemMetadata_obsoletes', False)

    
    obsoletes = property(__obsoletes.value, __obsoletes.set, None, None)

    
    # Element obsoletedBy uses Python identifier obsoletedBy
    __obsoletedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'obsoletedBy'), 'obsoletedBy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_obsoletedBy', False)

    
    obsoletedBy = property(__obsoletedBy.value, __obsoletedBy.set, None, None)


    _ElementMap = {
        __dateUploaded.name() : __dateUploaded,
        __submitter.name() : __submitter,
        __rightsHolder.name() : __rightsHolder,
        __serialVersion.name() : __serialVersion,
        __accessPolicy.name() : __accessPolicy,
        __replicationPolicy.name() : __replicationPolicy,
        __originMemberNode.name() : __originMemberNode,
        __identifier.name() : __identifier,
        __authoritativeMemberNode.name() : __authoritativeMemberNode,
        __replica.name() : __replica,
        __formatId.name() : __formatId,
        __checksum.name() : __checksum,
        __dateSysMetadataModified.name() : __dateSysMetadataModified,
        __size.name() : __size,
        __obsoletes.name() : __obsoletes,
        __obsoletedBy.name() : __obsoletedBy
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SystemMetadata', SystemMetadata)


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


# Complex type Service with content type ELEMENT_ONLY
class Service (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Service')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element restriction uses Python identifier restriction
    __restriction = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'restriction'), 'restriction', '__httpns_dataone_orgservicetypesv1_Service_restriction', True)

    
    restriction = property(__restriction.value, __restriction.set, None, None)

    
    # Attribute available uses Python identifier available
    __available = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'available'), 'available', '__httpns_dataone_orgservicetypesv1_Service_available', pyxb.binding.datatypes.boolean)
    
    available = property(__available.value, __available.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpns_dataone_orgservicetypesv1_Service_version', ServiceVersion, required=True)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesv1_Service_name', ServiceName, required=True)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __restriction.name() : __restriction
    }
    _AttributeMap = {
        __available.name() : __available,
        __version.name() : __version,
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'Service', Service)


accessPolicy = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'accessPolicy'), AccessPolicy)
Namespace.addCategoryObject('elementBinding', accessPolicy.name().localName(), accessPolicy)

monitorList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'monitorList'), MonitorList)
Namespace.addCategoryObject('elementBinding', monitorList.name().localName(), monitorList)

objectLocationList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectLocationList'), ObjectLocationList)
Namespace.addCategoryObject('elementBinding', objectLocationList.name().localName(), objectLocationList)

person = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'person'), Person)
Namespace.addCategoryObject('elementBinding', person.name().localName(), person)

subjectInfo = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subjectInfo'), SubjectInfo)
Namespace.addCategoryObject('elementBinding', subjectInfo.name().localName(), subjectInfo)

log = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'log'), Log)
Namespace.addCategoryObject('elementBinding', log.name().localName(), log)

objectList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectList'), ObjectList)
Namespace.addCategoryObject('elementBinding', objectList.name().localName(), objectList)

nodeReference = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'nodeReference'), NodeReference)
Namespace.addCategoryObject('elementBinding', nodeReference.name().localName(), nodeReference)

subjectList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subjectList'), SubjectList)
Namespace.addCategoryObject('elementBinding', subjectList.name().localName(), subjectList)

identifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'identifier'), Identifier)
Namespace.addCategoryObject('elementBinding', identifier.name().localName(), identifier)

node = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'node'), Node)
Namespace.addCategoryObject('elementBinding', node.name().localName(), node)

objectFormatList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectFormatList'), ObjectFormatList)
Namespace.addCategoryObject('elementBinding', objectFormatList.name().localName(), objectFormatList)

subject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subject'), Subject)
Namespace.addCategoryObject('elementBinding', subject.name().localName(), subject)

checksum = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'checksum'), Checksum)
Namespace.addCategoryObject('elementBinding', checksum.name().localName(), checksum)

systemMetadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'systemMetadata'), SystemMetadata)
Namespace.addCategoryObject('elementBinding', systemMetadata.name().localName(), systemMetadata)

nodeList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'nodeList'), NodeList)
Namespace.addCategoryObject('elementBinding', nodeList.name().localName(), nodeList)

objectFormat = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectFormat'), ObjectFormat)
Namespace.addCategoryObject('elementBinding', objectFormat.name().localName(), objectFormat)

session = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'session'), Session)
Namespace.addCategoryObject('elementBinding', session.name().localName(), session)



Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'isMemberOf'), Subject, scope=Person, documentation=u'A group or role in which the Principal is a\n\t\t\t\t\t\tmember, expressed using the\n\t\t\t\t\t\tunique Principal identifier for that group.'))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'verified'), pyxb.binding.datatypes.boolean, scope=Person, documentation=u"True if the name and email address of the Person\n\t\t\t\t\t\thave been verified to ensure that the givenName and familyName\n\t\t\t\t\t\trepresent the real person's legal name, and that the email \n\t\t\t\t\t\taddress is correct for that person and is in the control\n\t\t\t\t\t\tof the indicated individual. Verification occurs through a\n\t\t\t\t\t\testablished procedure within DataONE as part of the Identity \n\t\t\t\t\t\tManagement system.\n\t\t\t\t\t"))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'equivalentIdentity'), Subject, scope=Person, documentation=u'An alternative but equivalent identity for the\n\t\t\t\t\t\tprincipal that has been\n\t\t\t\t\t\tused in alternate identity systems.'))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'givenName'), NonEmptyString, scope=Person, documentation=u'The given name of the Person.'))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Person, documentation=u'The unique identifier for the person.\n\t\t\t\t\t'))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'familyName'), NonEmptyString, scope=Person, documentation=u'The family name of the Person.'))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'email'), NonEmptyString, scope=Person, documentation=u'The email address of the Person.\n\t\t\t\t\t'))
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



AccessPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'allow'), AccessRule, scope=AccessPolicy))
AccessPolicy._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AccessPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'allow')), min_occurs=1L, max_occurs=None)
    )
AccessPolicy._ContentModel = pyxb.binding.content.ParticleModel(AccessPolicy._GroupModel, min_occurs=1, max_occurs=1)



MonitorList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'monitorInfo'), MonitorInfo, scope=MonitorList))
MonitorList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MonitorList._UseForTag(pyxb.namespace.ExpandedName(None, u'monitorInfo')), min_occurs=0L, max_occurs=None)
    )
MonitorList._ContentModel = pyxb.binding.content.ParticleModel(MonitorList._GroupModel, min_occurs=1, max_occurs=1)



ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectLocation'), ObjectLocation, scope=ObjectLocationList, documentation=u'List of nodes from which the object can be\n                        retrieved'))

ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=ObjectLocationList, documentation=u'The identifier of the object being resolved.\n                    '))
ObjectLocationList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectLocation')), min_occurs=0L, max_occurs=None)
    )
ObjectLocationList._ContentModel = pyxb.binding.content.ParticleModel(ObjectLocationList._GroupModel, min_occurs=1, max_occurs=1)



SubjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'group'), Group, scope=SubjectInfo))

SubjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'person'), Person, scope=SubjectInfo))
SubjectInfo._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SubjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'person')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SubjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'group')), min_occurs=0L, max_occurs=None)
    )
SubjectInfo._ContentModel = pyxb.binding.content.ParticleModel(SubjectInfo._GroupModel, min_occurs=1, max_occurs=1)



Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'hasMember'), Subject, scope=Group, documentation=u'A Subject that is a member of this group, expressed using the\n                    unique identifier for that Subject.'))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Group, documentation=u'The unique identifier of the group.'))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'groupName'), NonEmptyString, scope=Group, documentation=u'The name of the Group.'))
Group._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Group._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Group._UseForTag(pyxb.namespace.ExpandedName(None, u'groupName')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Group._UseForTag(pyxb.namespace.ExpandedName(None, u'hasMember')), min_occurs=0L, max_occurs=None)
    )
Group._ContentModel = pyxb.binding.content.ParticleModel(Group._GroupModel, min_occurs=1, max_occurs=1)



SubjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=SubjectList))
SubjectList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SubjectList._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=0L, max_occurs=None)
    )
SubjectList._ContentModel = pyxb.binding.content.ParticleModel(SubjectList._GroupModel, min_occurs=1, max_occurs=1)



ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'blockedMemberNode'), NodeReference, scope=ReplicationPolicy, documentation=u'The object MUST never be replicated to nodes \n                        listed as blockedMemberNodes. Where there is a conflict between \n                        a preferredMemberNode and a blockedMemberNode entry, the \n                        blockedMemberNode entry prevails.\n                    '))

ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'preferredMemberNode'), NodeReference, scope=ReplicationPolicy, documentation=u'Nodes listed here have preference over other nodes for \n                    replication targets.\n                '))
ReplicationPolicy._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'preferredMemberNode')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'blockedMemberNode')), min_occurs=0L, max_occurs=None)
    )
ReplicationPolicy._ContentModel = pyxb.binding.content.ParticleModel(ReplicationPolicy._GroupModel, min_occurs=1, max_occurs=1)



ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'formatType'), pyxb.binding.datatypes.string, scope=ObjectFormat, documentation=u'A string field indicating whether or not this \n            format is science data(DATA), science metadata(METADATA) or a \n            resource map(RESOURCE).  If the format is a self-describing data \n            format that includes science metadata, then the field should also be \n            set to science metadata.\n            '))

ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'formatId'), ObjectFormatIdentifier, scope=ObjectFormat, documentation=u'\n                  The unique identifier of the object format in the DataONE\n                  Object Format Vocabulary.  The identifier should comply with\n                  DataONE Identifier rules, i.e. no whitespace, only UTF-8 or \n                  US-ASCII printable characters.\n              '))

ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'formatName'), pyxb.binding.datatypes.string, scope=ObjectFormat, documentation=u'\n              For objects that are typed using a Document Type Definition, \n              this lists the well-known and accepted named version of the DTD.\n            '))
ObjectFormat._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, u'formatId')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, u'formatName')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, u'formatType')), min_occurs=1L, max_occurs=1L)
    )
ObjectFormat._ContentModel = pyxb.binding.content.ParticleModel(ObjectFormat._GroupModel, min_occurs=1, max_occurs=1)



ServiceMethodRestriction._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'allowed'), SubjectList, scope=ServiceMethodRestriction))
ServiceMethodRestriction._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ServiceMethodRestriction._UseForTag(pyxb.namespace.ExpandedName(None, u'allowed')), min_occurs=1L, max_occurs=1L)
    )
ServiceMethodRestriction._ContentModel = pyxb.binding.content.ParticleModel(ServiceMethodRestriction._GroupModel, min_occurs=1, max_occurs=1)



MonitorInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'count'), pyxb.binding.datatypes.int, scope=MonitorInfo))

MonitorInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'date'), pyxb.binding.datatypes.date, scope=MonitorInfo))
MonitorInfo._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MonitorInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'date')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(MonitorInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'count')), min_occurs=1L, max_occurs=1L)
    )
MonitorInfo._ContentModel = pyxb.binding.content.ParticleModel(MonitorInfo._GroupModel, min_occurs=1, max_occurs=1)



Services._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'service'), Service, scope=Services))
Services._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Services._UseForTag(pyxb.namespace.ExpandedName(None, u'service')), min_occurs=1L, max_occurs=None)
    )
Services._ContentModel = pyxb.binding.content.ParticleModel(Services._GroupModel, min_occurs=1, max_occurs=1)



Log._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'logEntry'), LogEntry, scope=Log))
Log._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Log._UseForTag(pyxb.namespace.ExpandedName(None, u'logEntry')), min_occurs=0L, max_occurs=None)
    )
Log._ContentModel = pyxb.binding.content.ParticleModel(Log._GroupModel, min_occurs=1, max_occurs=1)



Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ping'), Ping, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), NodeReference, scope=Node, documentation=u'A unique identifier for the node. This may initially be the same as the\n                        baseURL, however this value should not change for future implementations of the same\n                        node, whereas the baseURL may change in the future. \n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), NonEmptyString, scope=Node, documentation=u'A human readable name of the Node. \n                        The name of the node is being used in Mercury currently to assign a path,\n                        so format should be consistent with dataone directory naming conventions\n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'contactSubject'), Subject, scope=Node, documentation=u'The appropriate person or group to contact regarding the disposition, \n                    management, and status of this Member Node. The Node.contactSubject is\n                    an X.509 Distinguished Name for a person or group that can be used to look up current \n                    contact details (e.g., name, email address) for the contact in the DataONE Identity service.\n                    DataONE uses the subjectContact to provide notices of interest to DataONE nodes, including \n                    information such as policy changes, maintenance updates, node outage notifications, among \n                    other information useful for administering a node. Each node that is registered with DataONE\n                    must provide at least one subjectContact that has been verified with DataONE.\n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'description'), NonEmptyString, scope=Node, documentation=u'Description of content maintained by this node and any other free style\n                        notes. May be we should allow CDATA element with the purpose of using for display\n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Node, documentation=u'The Subject of this node, which can be repeated as needed.  \n                    The Node.subject represents the identifier of the node that would be found in X.509 \n                    certificates that would be used to securely communicate with this node.  Thus, it is\n                    an X.509 Distinguished Name that applies to the host on which the Node is operating. \n                    When (and if) this hostname changes the new subject for the node would be added to the\n                    Node to track the subject that has been used in various access control rules over time.\n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'services'), Services, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'synchronization'), Synchronization, scope=Node))
Node._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'name')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'description')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'baseURL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'services')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'synchronization')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'ping')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'contactSubject')), min_occurs=1L, max_occurs=None)
    )
Node._ContentModel = pyxb.binding.content.ParticleModel(Node._GroupModel, min_occurs=1, max_occurs=1)



ObjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectInfo'), ObjectInfo, scope=ObjectList))
ObjectList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectInfo')), min_occurs=0L, max_occurs=None)
    )
ObjectList._ContentModel = pyxb.binding.content.ParticleModel(ObjectList._GroupModel, min_occurs=1, max_occurs=1)



ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'preference'), pyxb.binding.datatypes.int, scope=ObjectLocation, documentation=u'A weighting parameter that provides a hint to the caller \n                        for the relative preference for nodes from which the content should be retrieved.\n                    '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), NodeReference, scope=ObjectLocation, documentation=u'Identifier of the node (the same identifier used\n                        in the node registry for identifying the node.\n                    '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'url'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation=u'The full (absolute) URL that can be used to\n                        retrieve the object using the get() method of the rest interface.\n                    For example, if identifer\n                        was "ABX154", and the node had a base URL of ``http://mn1.dataone.org/mn``\n                        then the value would be ``http://mn1.dataone.org/mn/object/ABX154``'))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation=u'The current base URL for services implemented on the target node.\n                    '))
ObjectLocation._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'nodeIdentifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'baseURL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'url')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'preference')), min_occurs=0L, max_occurs=1L)
    )
ObjectLocation._ContentModel = pyxb.binding.content.ParticleModel(ObjectLocation._GroupModel, min_occurs=1, max_occurs=1)



Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicaVerified'), pyxb.binding.datatypes.dateTime, scope=Replica))

Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicaMemberNode'), NodeReference, scope=Replica))

Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicationStatus'), ReplicationStatus, scope=Replica))
Replica._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicaMemberNode')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicationStatus')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicaVerified')), min_occurs=1, max_occurs=1)
    )
Replica._ContentModel = pyxb.binding.content.ParticleModel(Replica._GroupModel, min_occurs=1, max_occurs=1)



ObjectFormatList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectFormat'), ObjectFormat, scope=ObjectFormatList))
ObjectFormatList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectFormatList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectFormat')), min_occurs=1L, max_occurs=None)
    )
ObjectFormatList._ContentModel = pyxb.binding.content.ParticleModel(ObjectFormatList._GroupModel, min_occurs=1, max_occurs=1)



AccessRule._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'permission'), Permission, scope=AccessRule))

AccessRule._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=AccessRule))
AccessRule._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AccessRule._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AccessRule._UseForTag(pyxb.namespace.ExpandedName(None, u'permission')), min_occurs=1L, max_occurs=None)
    )
AccessRule._ContentModel = pyxb.binding.content.ParticleModel(AccessRule._GroupModel, min_occurs=1, max_occurs=1)



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



Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation=u'The last time all the data from a node was pulled from a member node\n                    '))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'schedule'), Schedule, scope=Synchronization))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastHarvested'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation=u'The last time the mn sychronization daemon ran and found new data to synchronize\n                    '))
Synchronization._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'schedule')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastHarvested')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest')), min_occurs=1L, max_occurs=1L)
    )
Synchronization._ContentModel = pyxb.binding.content.ParticleModel(Synchronization._GroupModel, min_occurs=1, max_occurs=1)



LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateLogged'), pyxb.binding.datatypes.dateTime, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'memberNode'), NodeReference, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'event'), Event, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ipAddress'), pyxb.binding.datatypes.string, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'entryId'), Identifier, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'userAgent'), pyxb.binding.datatypes.string, scope=LogEntry))
LogEntry._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'entryId')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'ipAddress')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'userAgent')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'event')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'dateLogged')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LogEntry._UseForTag(pyxb.namespace.ExpandedName(None, u'memberNode')), min_occurs=1L, max_occurs=1L)
    )
LogEntry._ContentModel = pyxb.binding.content.ParticleModel(LogEntry._GroupModel, min_occurs=1, max_occurs=1)



SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateUploaded'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'submitter'), Subject, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'rightsHolder'), Subject, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'serialVersion'), pyxb.binding.datatypes.unsignedLong, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'accessPolicy'), AccessPolicy, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicationPolicy'), ReplicationPolicy, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'originMemberNode'), NodeReference, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode'), NodeReference, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replica'), Replica, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'formatId'), ObjectFormatIdentifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'checksum'), Checksum, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'size'), pyxb.binding.datatypes.unsignedLong, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'obsoletes'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'obsoletedBy'), Identifier, scope=SystemMetadata))
SystemMetadata._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'serialVersion')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'formatId')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'size')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'checksum')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'submitter')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'rightsHolder')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'accessPolicy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'replicationPolicy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'obsoletes')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'obsoletedBy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'dateUploaded')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'originMemberNode')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'replica')), min_occurs=0L, max_occurs=None)
    )
SystemMetadata._ContentModel = pyxb.binding.content.ParticleModel(SystemMetadata._GroupModel, min_occurs=1, max_occurs=1)



NodeList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'node'), Node, scope=NodeList))
NodeList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NodeList._UseForTag(pyxb.namespace.ExpandedName(None, u'node')), min_occurs=1L, max_occurs=None)
    )
NodeList._ContentModel = pyxb.binding.content.ParticleModel(NodeList._GroupModel, min_occurs=1, max_occurs=1)



Session._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subjectInfo'), SubjectInfo, scope=Session))

Session._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Session))
Session._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Session._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Session._UseForTag(pyxb.namespace.ExpandedName(None, u'subjectInfo')), min_occurs=0L, max_occurs=1L)
    )
Session._ContentModel = pyxb.binding.content.ParticleModel(Session._GroupModel, min_occurs=1, max_occurs=1)



Service._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'restriction'), ServiceMethodRestriction, scope=Service))
Service._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Service._UseForTag(pyxb.namespace.ExpandedName(None, u'restriction')), min_occurs=0L, max_occurs=None)
    )
Service._ContentModel = pyxb.binding.content.ParticleModel(Service._GroupModel, min_occurs=1, max_occurs=1)
