# ./d1_common/types/generated/dataoneTypes.py
# PyXB bindings for NamespaceModule
# NSM:b5056e9f5bcbaa65eac428b50fd841172c48ddf9
# Generated 2011-07-29 10:02:51.900739 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:3662afba-b9fc-11e0-b70d-000c294230b4')

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
class NonEmptyString (pyxb.binding.datatypes.string):

    """A derived string type with at least length 1 and it must contain non-whitespace."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonEmptyString')
    _Documentation = u'A derived string type with at least length 1 and it must contain non-whitespace.'
NonEmptyString._CF_pattern = pyxb.binding.facets.CF_pattern()
NonEmptyString._CF_pattern.addPattern(pattern=u'[\\s]*[\\S][\\s\\S]*')
NonEmptyString._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1L))
NonEmptyString._InitializeFacetMap(NonEmptyString._CF_pattern,
   NonEmptyString._CF_minLength)
Namespace.addCategoryObject('typeBinding', u'NonEmptyString', NonEmptyString)

# Atomic SimpleTypeDefinition
class ServiceVersion (NonEmptyString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceVersion')
    _Documentation = None
ServiceVersion._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ServiceVersion', ServiceVersion)

# Atomic SimpleTypeDefinition
class ChecksumAlgorithm (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ChecksumAlgorithm')
    _Documentation = None
ChecksumAlgorithm._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ChecksumAlgorithm, enum_prefix=None)
ChecksumAlgorithm.SHA_1 = ChecksumAlgorithm._CF_enumeration.addEnumeration(unicode_value=u'SHA-1')
ChecksumAlgorithm.SHA_224 = ChecksumAlgorithm._CF_enumeration.addEnumeration(unicode_value=u'SHA-224')
ChecksumAlgorithm.SHA_256 = ChecksumAlgorithm._CF_enumeration.addEnumeration(unicode_value=u'SHA-256')
ChecksumAlgorithm.SHA_384 = ChecksumAlgorithm._CF_enumeration.addEnumeration(unicode_value=u'SHA-384')
ChecksumAlgorithm.SHA_512 = ChecksumAlgorithm._CF_enumeration.addEnumeration(unicode_value=u'SHA-512')
ChecksumAlgorithm.MD5 = ChecksumAlgorithm._CF_enumeration.addEnumeration(unicode_value=u'MD5')
ChecksumAlgorithm._InitializeFacetMap(ChecksumAlgorithm._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ChecksumAlgorithm', ChecksumAlgorithm)

# Atomic SimpleTypeDefinition
class QueryType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """A string value indicating the type of a query from a controlled list.
                          The types of queries will expand with subsequent release versions, but
                          the CN will only support certain query types for search during any particular
                          release.
        """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'QueryType')
    _Documentation = u'A string value indicating the type of a query from a controlled list.\n                          The types of queries will expand with subsequent release versions, but\n                          the CN will only support certain query types for search during any particular\n                          release.\n        '
QueryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=QueryType, enum_prefix=None)
QueryType.SOLR = QueryType._CF_enumeration.addEnumeration(unicode_value=u'SOLR')
QueryType.ECOGRID = QueryType._CF_enumeration.addEnumeration(unicode_value=u'ECOGRID')
QueryType._InitializeFacetMap(QueryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'QueryType', QueryType)

# Atomic SimpleTypeDefinition
class Permission (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """A string value indicating the set of actions that can be performed on a
  resource as specified in an access policy.  The set of permissions include
  the ability to read a resource, modify a resource (write), and to change
  the set of access control policies for a resource (changePermission).  In
  addition, there is a permission that controls ability to execute a service
  (execute). Permissions are cumulative, in that higher level permissions
  include all of the priveledges of lower levels (e.g., given write access, one
  also implicitly has read access)."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Permission')
    _Documentation = u'A string value indicating the set of actions that can be performed on a\n  resource as specified in an access policy.  The set of permissions include\n  the ability to read a resource, modify a resource (write), and to change\n  the set of access control policies for a resource (changePermission).  In\n  addition, there is a permission that controls ability to execute a service\n  (execute). Permissions are cumulative, in that higher level permissions\n  include all of the priveledges of lower levels (e.g., given write access, one\n  also implicitly has read access).'
Permission._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Permission, enum_prefix=None)
Permission.read = Permission._CF_enumeration.addEnumeration(unicode_value=u'read')
Permission.write = Permission._CF_enumeration.addEnumeration(unicode_value=u'write')
Permission.changePermission = Permission._CF_enumeration.addEnumeration(unicode_value=u'changePermission')
Permission.execute = Permission._CF_enumeration.addEnumeration(unicode_value=u'execute')
Permission._InitializeFacetMap(Permission._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'Permission', Permission)

# Atomic SimpleTypeDefinition
class ReplicationStatus (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReplicationStatus')
    _Documentation = None
ReplicationStatus._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ReplicationStatus, enum_prefix=None)
ReplicationStatus.queued = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'queued')
ReplicationStatus.requested = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'requested')
ReplicationStatus.completed = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'completed')
ReplicationStatus.invalidated = ReplicationStatus._CF_enumeration.addEnumeration(unicode_value=u'invalidated')
ReplicationStatus._InitializeFacetMap(ReplicationStatus._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ReplicationStatus', ReplicationStatus)

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
class CrontabEntry (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CrontabEntry')
    _Documentation = None
CrontabEntry._CF_pattern = pyxb.binding.facets.CF_pattern()
CrontabEntry._CF_pattern.addPattern(pattern=u'([\\*\\d]{1,2}[\\-,]?)+')
CrontabEntry._InitializeFacetMap(CrontabEntry._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'CrontabEntry', CrontabEntry)

# Atomic SimpleTypeDefinition
class IdentifierFormat (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """Initially an enumerated list of strings that specify different types of identifiers.
        """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IdentifierFormat')
    _Documentation = u'Initially an enumerated list of strings that specify different types of identifiers.\n        '
IdentifierFormat._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=IdentifierFormat, enum_prefix=None)
IdentifierFormat.OID = IdentifierFormat._CF_enumeration.addEnumeration(unicode_value=u'OID')
IdentifierFormat.LSID = IdentifierFormat._CF_enumeration.addEnumeration(unicode_value=u'LSID')
IdentifierFormat.UUID = IdentifierFormat._CF_enumeration.addEnumeration(unicode_value=u'UUID')
IdentifierFormat.LSRN = IdentifierFormat._CF_enumeration.addEnumeration(unicode_value=u'LSRN')
IdentifierFormat.DOI = IdentifierFormat._CF_enumeration.addEnumeration(unicode_value=u'DOI')
IdentifierFormat.URI = IdentifierFormat._CF_enumeration.addEnumeration(unicode_value=u'URI')
IdentifierFormat.STRING = IdentifierFormat._CF_enumeration.addEnumeration(unicode_value=u'STRING')
IdentifierFormat._InitializeFacetMap(IdentifierFormat._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'IdentifierFormat', IdentifierFormat)

# Atomic SimpleTypeDefinition
class ObjectFormatIdentifier (NonEmptyString):

    """ An ObjectFormatIdentifier is a string identifying
          the object format. It must be unique in the containing ObjectFormatList.
          """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectFormatIdentifier')
    _Documentation = u' An ObjectFormatIdentifier is a string identifying\n          the object format. It must be unique in the containing ObjectFormatList.\n          '
ObjectFormatIdentifier._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ObjectFormatIdentifier', ObjectFormatIdentifier)

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

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceName')
    _Documentation = None
ServiceName._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ServiceName', ServiceName)

# Atomic SimpleTypeDefinition
class ComponentName (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ComponentName')
    _Documentation = None
ComponentName._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ComponentName, enum_prefix=None)
ComponentName.Apache = ComponentName._CF_enumeration.addEnumeration(unicode_value=u'Apache')
ComponentName.CoordinatingNode = ComponentName._CF_enumeration.addEnumeration(unicode_value=u'CoordinatingNode')
ComponentName.Django = ComponentName._CF_enumeration.addEnumeration(unicode_value=u'Django')
ComponentName.LinuxUbuntu = ComponentName._CF_enumeration.addEnumeration(unicode_value=u'LinuxUbuntu')
ComponentName.LinuxDebian = ComponentName._CF_enumeration.addEnumeration(unicode_value=u'LinuxDebian')
ComponentName.MemberNode = ComponentName._CF_enumeration.addEnumeration(unicode_value=u'MemberNode')
ComponentName.Mercury = ComponentName._CF_enumeration.addEnumeration(unicode_value=u'Mercury')
ComponentName.Metacat = ComponentName._CF_enumeration.addEnumeration(unicode_value=u'Metacat')
ComponentName._InitializeFacetMap(ComponentName._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ComponentName', ComponentName)

# Atomic SimpleTypeDefinition
class ComponentVersion (NonEmptyString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ComponentVersion')
    _Documentation = None
ComponentVersion._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ComponentVersion', ComponentVersion)

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


# Complex type Node with content type ELEMENT_ONLY
class Node (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Node')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element synchronization uses Python identifier synchronization
    __synchronization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'synchronization'), 'synchronization', '__httpns_dataone_orgservicetypesv1_Node_synchronization', False)

    
    synchronization = property(__synchronization.value, __synchronization.set, None, None)

    
    # Element health uses Python identifier health
    __health = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'health'), 'health', '__httpns_dataone_orgservicetypesv1_Node_health', False)

    
    health = property(__health.value, __health.set, None, u'The name of the node is being used in Mercury currently to assign a\n                        path, so format should be consistent with dataone directory naming conventions\n                    ')

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesv1_Node_name', False)

    
    name = property(__name.value, __name.set, None, u'A human readable name of the Node. \n                        The name of the node is being used in Mercury currently to assign a path,\n                        so format should be consistent with dataone directory naming conventions\n                    ')

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_Node_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'A unique identifier for the node. This may initially be the same as the\n                        baseURL, however this value should not change for future implementations of the same\n                        node, whereas the baseURL may change in the future. \n                    ')

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__httpns_dataone_orgservicetypesv1_Node_description', False)

    
    description = property(__description.value, __description.set, None, u'Description of content maintained by this node and any other free style\n                        notes. May be we should allow CDATA element with the purpose of using for display\n                    ')

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'baseURL'), 'baseURL', '__httpns_dataone_orgservicetypesv1_Node_baseURL', False)

    
    baseURL = property(__baseURL.value, __baseURL.set, None, None)

    
    # Element services uses Python identifier services
    __services = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'services'), 'services', '__httpns_dataone_orgservicetypesv1_Node_services', False)

    
    services = property(__services.value, __services.set, None, None)

    
    # Attribute synchronize uses Python identifier synchronize
    __synchronize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'synchronize'), 'synchronize', '__httpns_dataone_orgservicetypesv1_Node_synchronize', pyxb.binding.datatypes.boolean, required=True)
    
    synchronize = property(__synchronize.value, __synchronize.set, None, None)

    
    # Attribute replicate uses Python identifier replicate
    __replicate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'replicate'), 'replicate', '__httpns_dataone_orgservicetypesv1_Node_replicate', pyxb.binding.datatypes.boolean, required=True)
    
    replicate = property(__replicate.value, __replicate.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'type'), 'type', '__httpns_dataone_orgservicetypesv1_Node_type', NodeType, required=True)
    
    type = property(__type.value, __type.set, None, None)


    _ElementMap = {
        __synchronization.name() : __synchronization,
        __health.name() : __health,
        __name.name() : __name,
        __identifier.name() : __identifier,
        __description.name() : __description,
        __baseURL.name() : __baseURL,
        __services.name() : __services
    }
    _AttributeMap = {
        __synchronize.name() : __synchronize,
        __replicate.name() : __replicate,
        __type.name() : __type
    }
Namespace.addCategoryObject('typeBinding', u'Node', Node)


# Complex type SubjectList with content type ELEMENT_ONLY
class SubjectList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SubjectList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element group uses Python identifier group
    __group = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'group'), 'group', '__httpns_dataone_orgservicetypesv1_SubjectList_group', True)

    
    group = property(__group.value, __group.set, None, None)

    
    # Element person uses Python identifier person
    __person = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'person'), 'person', '__httpns_dataone_orgservicetypesv1_SubjectList_person', True)

    
    person = property(__person.value, __person.set, None, None)


    _ElementMap = {
        __group.name() : __group,
        __person.name() : __person
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SubjectList', SubjectList)


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

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesv1_Service_name', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute available uses Python identifier available
    __available = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'available'), 'available', '__httpns_dataone_orgservicetypesv1_Service_available', pyxb.binding.datatypes.boolean)
    
    available = property(__available.value, __available.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpns_dataone_orgservicetypesv1_Service_version', ServiceVersion, required=True)
    
    version = property(__version.value, __version.set, None, None)


    _ElementMap = {
        __restriction.name() : __restriction,
        __name.name() : __name
    }
    _AttributeMap = {
        __available.name() : __available,
        __version.name() : __version
    }
Namespace.addCategoryObject('typeBinding', u'Service', Service)


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


# Complex type ReplicationPolicy with content type ELEMENT_ONLY
class ReplicationPolicy (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReplicationPolicy')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element blockedMemberNode uses Python identifier blockedMemberNode
    __blockedMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'blockedMemberNode'), 'blockedMemberNode', '__httpns_dataone_orgservicetypesv1_ReplicationPolicy_blockedMemberNode', True)

    
    blockedMemberNode = property(__blockedMemberNode.value, __blockedMemberNode.set, None, u'The object MUST never be replicated to nodes \n                        listed as blockedMemberNodes. Where there is a conflict between \n                        a requiredMemberNode and a blockedMemberNode entry, the \n                        blockedMemberNode entry prevails.\n                    ')

    
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


# Complex type Identifier with content type SIMPLE
class Identifier (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = NonEmptyString
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Identifier')
    # Base type is NonEmptyString

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Identifier', Identifier)


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

    
    # Element ipAddress uses Python identifier ipAddress
    __ipAddress = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ipAddress'), 'ipAddress', '__httpns_dataone_orgservicetypesv1_LogEntry_ipAddress', False)

    
    ipAddress = property(__ipAddress.value, __ipAddress.set, None, None)

    
    # Element event uses Python identifier event
    __event = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'event'), 'event', '__httpns_dataone_orgservicetypesv1_LogEntry_event', False)

    
    event = property(__event.value, __event.set, None, None)

    
    # Element userAgent uses Python identifier userAgent
    __userAgent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'userAgent'), 'userAgent', '__httpns_dataone_orgservicetypesv1_LogEntry_userAgent', False)

    
    userAgent = property(__userAgent.value, __userAgent.set, None, None)

    
    # Element dateLogged uses Python identifier dateLogged
    __dateLogged = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateLogged'), 'dateLogged', '__httpns_dataone_orgservicetypesv1_LogEntry_dateLogged', False)

    
    dateLogged = property(__dateLogged.value, __dateLogged.set, None, None)

    
    # Element memberNode uses Python identifier memberNode
    __memberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'memberNode'), 'memberNode', '__httpns_dataone_orgservicetypesv1_LogEntry_memberNode', False)

    
    memberNode = property(__memberNode.value, __memberNode.set, None, None)

    
    # Element entryId uses Python identifier entryId
    __entryId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'entryId'), 'entryId', '__httpns_dataone_orgservicetypesv1_LogEntry_entryId', False)

    
    entryId = property(__entryId.value, __entryId.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_LogEntry_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)


    _ElementMap = {
        __subject.name() : __subject,
        __ipAddress.name() : __ipAddress,
        __event.name() : __event,
        __userAgent.name() : __userAgent,
        __dateLogged.name() : __dateLogged,
        __memberNode.name() : __memberNode,
        __entryId.name() : __entryId,
        __identifier.name() : __identifier
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LogEntry', LogEntry)


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


# Complex type ObjectFormat with content type ELEMENT_ONLY
class ObjectFormat (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectFormat')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element scienceMetadata uses Python identifier scienceMetadata
    __scienceMetadata = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'scienceMetadata'), 'scienceMetadata', '__httpns_dataone_orgservicetypesv1_ObjectFormat_scienceMetadata', False)

    
    scienceMetadata = property(__scienceMetadata.value, __scienceMetadata.set, None, u'\n              A boolean field indicating whether or not this format is science\n              metadata describing a science data object.  If the format is a\n              self-describing data format that includes science metadata, then \n              the field should also be set to true.\n            ')

    
    # Element fmtid uses Python identifier fmtid
    __fmtid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'fmtid'), 'fmtid', '__httpns_dataone_orgservicetypesv1_ObjectFormat_fmtid', False)

    
    fmtid = property(__fmtid.value, __fmtid.set, None, u'\n                  The unique identifier of the object format in the DataONE\n                  Object Format Vocabulary.  The identifier should comply with\n                  DataONE Identifier rules, i.e. no whitespace, UTF-8 or \n                  US-ASCII printable characters.\n              ')

    
    # Element formatName uses Python identifier formatName
    __formatName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'formatName'), 'formatName', '__httpns_dataone_orgservicetypesv1_ObjectFormat_formatName', False)

    
    formatName = property(__formatName.value, __formatName.set, None, u'\n              For objects that are typed using a Document Type Definition, \n              this lists the well-known and accepted named version of the DTD.\n            ')


    _ElementMap = {
        __scienceMetadata.name() : __scienceMetadata,
        __fmtid.name() : __fmtid,
        __formatName.name() : __formatName
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectFormat', ObjectFormat)


# Complex type ComponentList with content type ELEMENT_ONLY
class ComponentList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ComponentList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element component uses Python identifier component
    __component = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'component'), 'component', '__httpns_dataone_orgservicetypesv1_ComponentList_component', False)

    
    component = property(__component.value, __component.set, None, None)


    _ElementMap = {
        __component.name() : __component
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ComponentList', ComponentList)


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


# Complex type Ping with content type EMPTY
class Ping (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Ping')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute lastSuccess uses Python identifier lastSuccess
    __lastSuccess = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'lastSuccess'), 'lastSuccess', '__httpns_dataone_orgservicetypesv1_Ping_lastSuccess', pyxb.binding.datatypes.dateTime)
    
    lastSuccess = property(__lastSuccess.value, __lastSuccess.set, None, None)

    
    # Attribute success uses Python identifier success
    __success = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'success'), 'success', '__httpns_dataone_orgservicetypesv1_Ping_success', pyxb.binding.datatypes.boolean)
    
    success = property(__success.value, __success.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __lastSuccess.name() : __lastSuccess,
        __success.name() : __success
    }
Namespace.addCategoryObject('typeBinding', u'Ping', Ping)


# Complex type Person with content type ELEMENT_ONLY
class Person (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Person')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'email'), 'email', '__httpns_dataone_orgservicetypesv1_Person_email', True)

    
    email = property(__email.value, __email.set, None, None)

    
    # Element isMemberOf uses Python identifier isMemberOf
    __isMemberOf = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'isMemberOf'), 'isMemberOf', '__httpns_dataone_orgservicetypesv1_Person_isMemberOf', True)

    
    isMemberOf = property(__isMemberOf.value, __isMemberOf.set, None, None)

    
    # Element equivalentIdentity uses Python identifier equivalentIdentity
    __equivalentIdentity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'equivalentIdentity'), 'equivalentIdentity', '__httpns_dataone_orgservicetypesv1_Person_equivalentIdentity', True)

    
    equivalentIdentity = property(__equivalentIdentity.value, __equivalentIdentity.set, None, None)

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Person_subject', False)

    
    subject = property(__subject.value, __subject.set, None, None)

    
    # Element givenName uses Python identifier givenName
    __givenName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'givenName'), 'givenName', '__httpns_dataone_orgservicetypesv1_Person_givenName', True)

    
    givenName = property(__givenName.value, __givenName.set, None, None)

    
    # Element familyName uses Python identifier familyName
    __familyName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'familyName'), 'familyName', '__httpns_dataone_orgservicetypesv1_Person_familyName', False)

    
    familyName = property(__familyName.value, __familyName.set, None, None)


    _ElementMap = {
        __email.name() : __email,
        __isMemberOf.name() : __isMemberOf,
        __equivalentIdentity.name() : __equivalentIdentity,
        __subject.name() : __subject,
        __givenName.name() : __givenName,
        __familyName.name() : __familyName
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Person', Person)


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


# Complex type NodeHealth with content type ELEMENT_ONLY
class NodeHealth (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeHealth')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element status uses Python identifier status
    __status = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'status'), 'status', '__httpns_dataone_orgservicetypesv1_NodeHealth_status', False)

    
    status = property(__status.value, __status.set, None, None)

    
    # Element ping uses Python identifier ping
    __ping = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ping'), 'ping', '__httpns_dataone_orgservicetypesv1_NodeHealth_ping', False)

    
    ping = property(__ping.value, __ping.set, None, None)

    
    # Attribute state uses Python identifier state
    __state = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'state'), 'state', '__httpns_dataone_orgservicetypesv1_NodeHealth_state', NodeState, required=True)
    
    state = property(__state.value, __state.set, None, None)


    _ElementMap = {
        __status.name() : __status,
        __ping.name() : __ping
    }
    _AttributeMap = {
        __state.name() : __state
    }
Namespace.addCategoryObject('typeBinding', u'NodeHealth', NodeHealth)


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

    
    # Attribute mon uses Python identifier mon
    __mon = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mon'), 'mon', '__httpns_dataone_orgservicetypesv1_Schedule_mon', CrontabEntry, required=True)
    
    mon = property(__mon.value, __mon.set, None, None)

    
    # Attribute sec uses Python identifier sec
    __sec = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'sec'), 'sec', '__httpns_dataone_orgservicetypesv1_Schedule_sec', CrontabEntry, required=True)
    
    sec = property(__sec.value, __sec.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __hour.name() : __hour,
        __wday.name() : __wday,
        __year.name() : __year,
        __mday.name() : __mday,
        __min.name() : __min,
        __mon.name() : __mon,
        __sec.name() : __sec
    }
Namespace.addCategoryObject('typeBinding', u'Schedule', Schedule)


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

    
    url = property(__url.value, __url.set, None, u'The full (absolute) URL that can be used to\n                        retrieve the object using the get() method of the rest interface.\n                    ')

    
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


# Complex type SystemMetadata with content type ELEMENT_ONLY
class SystemMetadata (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SystemMetadata')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element size uses Python identifier size
    __size = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'size'), 'size', '__httpns_dataone_orgservicetypesv1_SystemMetadata_size', False)

    
    size = property(__size.value, __size.set, None, None)

    
    # Element obsoletedBy uses Python identifier obsoletedBy
    __obsoletedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'obsoletedBy'), 'obsoletedBy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_obsoletedBy', False)

    
    obsoletedBy = property(__obsoletedBy.value, __obsoletedBy.set, None, None)

    
    # Element obsoletes uses Python identifier obsoletes
    __obsoletes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'obsoletes'), 'obsoletes', '__httpns_dataone_orgservicetypesv1_SystemMetadata_obsoletes', False)

    
    obsoletes = property(__obsoletes.value, __obsoletes.set, None, None)

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__httpns_dataone_orgservicetypesv1_SystemMetadata_checksum', False)

    
    checksum = property(__checksum.value, __checksum.set, None, None)

    
    # Element submitter uses Python identifier submitter
    __submitter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'submitter'), 'submitter', '__httpns_dataone_orgservicetypesv1_SystemMetadata_submitter', False)

    
    submitter = property(__submitter.value, __submitter.set, None, None)

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpns_dataone_orgservicetypesv1_SystemMetadata_dateSysMetadataModified', False)

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, None)

    
    # Element rightsHolder uses Python identifier rightsHolder
    __rightsHolder = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'rightsHolder'), 'rightsHolder', '__httpns_dataone_orgservicetypesv1_SystemMetadata_rightsHolder', False)

    
    rightsHolder = property(__rightsHolder.value, __rightsHolder.set, None, None)

    
    # Element originMemberNode uses Python identifier originMemberNode
    __originMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'originMemberNode'), 'originMemberNode', '__httpns_dataone_orgservicetypesv1_SystemMetadata_originMemberNode', False)

    
    originMemberNode = property(__originMemberNode.value, __originMemberNode.set, None, None)

    
    # Element resourceMap uses Python identifier resourceMap
    __resourceMap = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'resourceMap'), 'resourceMap', '__httpns_dataone_orgservicetypesv1_SystemMetadata_resourceMap', True)

    
    resourceMap = property(__resourceMap.value, __resourceMap.set, None, None)

    
    # Element authoritativeMemberNode uses Python identifier authoritativeMemberNode
    __authoritativeMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode'), 'authoritativeMemberNode', '__httpns_dataone_orgservicetypesv1_SystemMetadata_authoritativeMemberNode', False)

    
    authoritativeMemberNode = property(__authoritativeMemberNode.value, __authoritativeMemberNode.set, None, None)

    
    # Element dateUploaded uses Python identifier dateUploaded
    __dateUploaded = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateUploaded'), 'dateUploaded', '__httpns_dataone_orgservicetypesv1_SystemMetadata_dateUploaded', False)

    
    dateUploaded = property(__dateUploaded.value, __dateUploaded.set, None, None)

    
    # Element replica uses Python identifier replica
    __replica = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replica'), 'replica', '__httpns_dataone_orgservicetypesv1_SystemMetadata_replica', True)

    
    replica = property(__replica.value, __replica.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpns_dataone_orgservicetypesv1_SystemMetadata_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element accessPolicy uses Python identifier accessPolicy
    __accessPolicy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'accessPolicy'), 'accessPolicy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_accessPolicy', False)

    
    accessPolicy = property(__accessPolicy.value, __accessPolicy.set, None, None)

    
    # Element objectFormat uses Python identifier objectFormat
    __objectFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectFormat'), 'objectFormat', '__httpns_dataone_orgservicetypesv1_SystemMetadata_objectFormat', False)

    
    objectFormat = property(__objectFormat.value, __objectFormat.set, None, None)

    
    # Element replicationPolicy uses Python identifier replicationPolicy
    __replicationPolicy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicationPolicy'), 'replicationPolicy', '__httpns_dataone_orgservicetypesv1_SystemMetadata_replicationPolicy', False)

    
    replicationPolicy = property(__replicationPolicy.value, __replicationPolicy.set, None, None)


    _ElementMap = {
        __size.name() : __size,
        __obsoletedBy.name() : __obsoletedBy,
        __obsoletes.name() : __obsoletes,
        __checksum.name() : __checksum,
        __submitter.name() : __submitter,
        __dateSysMetadataModified.name() : __dateSysMetadataModified,
        __rightsHolder.name() : __rightsHolder,
        __originMemberNode.name() : __originMemberNode,
        __resourceMap.name() : __resourceMap,
        __authoritativeMemberNode.name() : __authoritativeMemberNode,
        __dateUploaded.name() : __dateUploaded,
        __replica.name() : __replica,
        __identifier.name() : __identifier,
        __accessPolicy.name() : __accessPolicy,
        __objectFormat.name() : __objectFormat,
        __replicationPolicy.name() : __replicationPolicy
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SystemMetadata', SystemMetadata)


# Complex type Status with content type EMPTY
class Status (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Status')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute dateChecked uses Python identifier dateChecked
    __dateChecked = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dateChecked'), 'dateChecked', '__httpns_dataone_orgservicetypesv1_Status_dateChecked', pyxb.binding.datatypes.dateTime, required=True)
    
    dateChecked = property(__dateChecked.value, __dateChecked.set, None, None)

    
    # Attribute success uses Python identifier success
    __success = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'success'), 'success', '__httpns_dataone_orgservicetypesv1_Status_success', pyxb.binding.datatypes.boolean)
    
    success = property(__success.value, __success.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __dateChecked.name() : __dateChecked,
        __success.name() : __success
    }
Namespace.addCategoryObject('typeBinding', u'Status', Status)


# Complex type Group with content type ELEMENT_ONLY
class Group (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Group')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element hasMember uses Python identifier hasMember
    __hasMember = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'hasMember'), 'hasMember', '__httpns_dataone_orgservicetypesv1_Group_hasMember', True)

    
    hasMember = property(__hasMember.value, __hasMember.set, None, None)

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Group_subject', False)

    
    subject = property(__subject.value, __subject.set, None, None)

    
    # Element groupName uses Python identifier groupName
    __groupName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'groupName'), 'groupName', '__httpns_dataone_orgservicetypesv1_Group_groupName', False)

    
    groupName = property(__groupName.value, __groupName.set, None, None)


    _ElementMap = {
        __hasMember.name() : __hasMember,
        __subject.name() : __subject,
        __groupName.name() : __groupName
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Group', Group)


# Complex type Session with content type ELEMENT_ONLY
class Session (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Session')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element subjectList uses Python identifier subjectList
    __subjectList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subjectList'), 'subjectList', '__httpns_dataone_orgservicetypesv1_Session_subjectList', False)

    
    subjectList = property(__subjectList.value, __subjectList.set, None, None)

    
    # Element subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'subject'), 'subject', '__httpns_dataone_orgservicetypesv1_Session_subject', False)

    
    subject = property(__subject.value, __subject.set, None, None)


    _ElementMap = {
        __subjectList.name() : __subjectList,
        __subject.name() : __subject
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Session', Session)


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

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpns_dataone_orgservicetypesv1_ObjectInfo_dateSysMetadataModified', False)

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, None)

    
    # Element objectFormat uses Python identifier objectFormat
    __objectFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectFormat'), 'objectFormat', '__httpns_dataone_orgservicetypesv1_ObjectInfo_objectFormat', False)

    
    objectFormat = property(__objectFormat.value, __objectFormat.set, None, None)

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__httpns_dataone_orgservicetypesv1_ObjectInfo_checksum', False)

    
    checksum = property(__checksum.value, __checksum.set, None, None)


    _ElementMap = {
        __size.name() : __size,
        __identifier.name() : __identifier,
        __dateSysMetadataModified.name() : __dateSysMetadataModified,
        __objectFormat.name() : __objectFormat,
        __checksum.name() : __checksum
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectInfo', ObjectInfo)


# Complex type Component with content type EMPTY
class Component (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Component')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpns_dataone_orgservicetypesv1_Component_version', ComponentVersion, required=True)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesv1_Component_name', ComponentName, required=True)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __version.name() : __version,
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'Component', Component)


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


objectFormatList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectFormatList'), ObjectFormatList)
Namespace.addCategoryObject('elementBinding', objectFormatList.name().localName(), objectFormatList)

node = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'node'), Node)
Namespace.addCategoryObject('elementBinding', node.name().localName(), node)

subjectList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subjectList'), SubjectList)
Namespace.addCategoryObject('elementBinding', subjectList.name().localName(), subjectList)

componentList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'componentList'), ComponentList)
Namespace.addCategoryObject('elementBinding', componentList.name().localName(), componentList)

nodeList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'nodeList'), NodeList)
Namespace.addCategoryObject('elementBinding', nodeList.name().localName(), nodeList)

subject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subject'), Subject)
Namespace.addCategoryObject('elementBinding', subject.name().localName(), subject)

objectFormat = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectFormat'), ObjectFormat)
Namespace.addCategoryObject('elementBinding', objectFormat.name().localName(), objectFormat)

checksum = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'checksum'), Checksum)
Namespace.addCategoryObject('elementBinding', checksum.name().localName(), checksum)

objectLocationList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectLocationList'), ObjectLocationList)
Namespace.addCategoryObject('elementBinding', objectLocationList.name().localName(), objectLocationList)

person = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'person'), Person)
Namespace.addCategoryObject('elementBinding', person.name().localName(), person)

log = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'log'), Log)
Namespace.addCategoryObject('elementBinding', log.name().localName(), log)

nodeReference = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'nodeReference'), NodeReference)
Namespace.addCategoryObject('elementBinding', nodeReference.name().localName(), nodeReference)

objectList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectList'), ObjectList)
Namespace.addCategoryObject('elementBinding', objectList.name().localName(), objectList)

monitorList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'monitorList'), MonitorList)
Namespace.addCategoryObject('elementBinding', monitorList.name().localName(), monitorList)

systemMetadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'systemMetadata'), SystemMetadata)
Namespace.addCategoryObject('elementBinding', systemMetadata.name().localName(), systemMetadata)

accessPolicy = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'accessPolicy'), AccessPolicy)
Namespace.addCategoryObject('elementBinding', accessPolicy.name().localName(), accessPolicy)

identifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'identifier'), Identifier)
Namespace.addCategoryObject('elementBinding', identifier.name().localName(), identifier)



ObjectFormatList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectFormat'), ObjectFormat, scope=ObjectFormatList))
ObjectFormatList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectFormatList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectFormat')), min_occurs=1L, max_occurs=None)
    )
ObjectFormatList._ContentModel = pyxb.binding.content.ParticleModel(ObjectFormatList._GroupModel, min_occurs=1, max_occurs=1)



Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'synchronization'), Synchronization, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'health'), NodeHealth, scope=Node, documentation=u'The name of the node is being used in Mercury currently to assign a\n                        path, so format should be consistent with dataone directory naming conventions\n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), NonEmptyString, scope=Node, documentation=u'A human readable name of the Node. \n                        The name of the node is being used in Mercury currently to assign a path,\n                        so format should be consistent with dataone directory naming conventions\n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), NodeReference, scope=Node, documentation=u'A unique identifier for the node. This may initially be the same as the\n                        baseURL, however this value should not change for future implementations of the same\n                        node, whereas the baseURL may change in the future. \n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'description'), NonEmptyString, scope=Node, documentation=u'Description of content maintained by this node and any other free style\n                        notes. May be we should allow CDATA element with the purpose of using for display\n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'services'), Services, scope=Node))
Node._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'name')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'description')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'baseURL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'services')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'synchronization')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Node._UseForTag(pyxb.namespace.ExpandedName(None, u'health')), min_occurs=0L, max_occurs=1L)
    )
Node._ContentModel = pyxb.binding.content.ParticleModel(Node._GroupModel, min_occurs=1, max_occurs=1)



SubjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'group'), Group, scope=SubjectList))

SubjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'person'), Person, scope=SubjectList))
SubjectList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SubjectList._UseForTag(pyxb.namespace.ExpandedName(None, u'person')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SubjectList._UseForTag(pyxb.namespace.ExpandedName(None, u'group')), min_occurs=0L, max_occurs=None)
    )
SubjectList._ContentModel = pyxb.binding.content.ParticleModel(SubjectList._GroupModel, min_occurs=1, max_occurs=1)



ServiceMethodRestriction._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'allowed'), SubjectList, scope=ServiceMethodRestriction))
ServiceMethodRestriction._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ServiceMethodRestriction._UseForTag(pyxb.namespace.ExpandedName(None, u'allowed')), min_occurs=1L, max_occurs=1L)
    )
ServiceMethodRestriction._ContentModel = pyxb.binding.content.ParticleModel(ServiceMethodRestriction._GroupModel, min_occurs=1, max_occurs=1)



Service._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'restriction'), ServiceMethodRestriction, scope=Service))

Service._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), ServiceName, scope=Service))
Service._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Service._UseForTag(pyxb.namespace.ExpandedName(None, u'name')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Service._UseForTag(pyxb.namespace.ExpandedName(None, u'restriction')), min_occurs=0L, max_occurs=None)
    )
Service._ContentModel = pyxb.binding.content.ParticleModel(Service._GroupModel, min_occurs=1, max_occurs=1)



ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'blockedMemberNode'), NodeReference, scope=ReplicationPolicy, documentation=u'The object MUST never be replicated to nodes \n                        listed as blockedMemberNodes. Where there is a conflict between \n                        a requiredMemberNode and a blockedMemberNode entry, the \n                        blockedMemberNode entry prevails.\n                    '))

ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'preferredMemberNode'), NodeReference, scope=ReplicationPolicy, documentation=u'Nodes listed here have preference over other nodes for \n                    replication targets.\n                '))
ReplicationPolicy._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'preferredMemberNode')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'blockedMemberNode')), min_occurs=0L, max_occurs=None)
    )
ReplicationPolicy._ContentModel = pyxb.binding.content.ParticleModel(ReplicationPolicy._GroupModel, min_occurs=1, max_occurs=1)



LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ipAddress'), pyxb.binding.datatypes.string, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'event'), Event, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'userAgent'), pyxb.binding.datatypes.string, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateLogged'), pyxb.binding.datatypes.dateTime, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'memberNode'), NodeReference, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'entryId'), Identifier, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=LogEntry))
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



ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'scienceMetadata'), pyxb.binding.datatypes.boolean, scope=ObjectFormat, documentation=u'\n              A boolean field indicating whether or not this format is science\n              metadata describing a science data object.  If the format is a\n              self-describing data format that includes science metadata, then \n              the field should also be set to true.\n            '))

ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'fmtid'), ObjectFormatIdentifier, scope=ObjectFormat, documentation=u'\n                  The unique identifier of the object format in the DataONE\n                  Object Format Vocabulary.  The identifier should comply with\n                  DataONE Identifier rules, i.e. no whitespace, UTF-8 or \n                  US-ASCII printable characters.\n              '))

ObjectFormat._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'formatName'), pyxb.binding.datatypes.string, scope=ObjectFormat, documentation=u'\n              For objects that are typed using a Document Type Definition, \n              this lists the well-known and accepted named version of the DTD.\n            '))
ObjectFormat._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, u'fmtid')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, u'formatName')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectFormat._UseForTag(pyxb.namespace.ExpandedName(None, u'scienceMetadata')), min_occurs=1L, max_occurs=1L)
    )
ObjectFormat._ContentModel = pyxb.binding.content.ParticleModel(ObjectFormat._GroupModel, min_occurs=1, max_occurs=1)



ComponentList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'component'), Component, scope=ComponentList))
ComponentList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ComponentList._UseForTag(pyxb.namespace.ExpandedName(None, u'component')), min_occurs=1, max_occurs=1)
    )
ComponentList._ContentModel = pyxb.binding.content.ParticleModel(ComponentList._GroupModel, min_occurs=1, max_occurs=1)



NodeList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'node'), Node, scope=NodeList))
NodeList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NodeList._UseForTag(pyxb.namespace.ExpandedName(None, u'node')), min_occurs=1L, max_occurs=None)
    )
NodeList._ContentModel = pyxb.binding.content.ParticleModel(NodeList._GroupModel, min_occurs=1, max_occurs=1)



Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'email'), NonEmptyString, scope=Person))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'isMemberOf'), Subject, scope=Person))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'equivalentIdentity'), Subject, scope=Person))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Person))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'givenName'), NonEmptyString, scope=Person))

Person._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'familyName'), NonEmptyString, scope=Person))
Person._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'givenName')), min_occurs=1L, max_occurs=None),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'familyName')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'email')), min_occurs=1L, max_occurs=None),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'isMemberOf')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(Person._UseForTag(pyxb.namespace.ExpandedName(None, u'equivalentIdentity')), min_occurs=0L, max_occurs=None)
    )
Person._ContentModel = pyxb.binding.content.ParticleModel(Person._GroupModel, min_occurs=1, max_occurs=1)



Services._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'service'), Service, scope=Services))
Services._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Services._UseForTag(pyxb.namespace.ExpandedName(None, u'service')), min_occurs=1L, max_occurs=None)
    )
Services._ContentModel = pyxb.binding.content.ParticleModel(Services._GroupModel, min_occurs=1, max_occurs=1)



NodeHealth._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'status'), Status, scope=NodeHealth))

NodeHealth._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ping'), Ping, scope=NodeHealth))
NodeHealth._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NodeHealth._UseForTag(pyxb.namespace.ExpandedName(None, u'ping')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(NodeHealth._UseForTag(pyxb.namespace.ExpandedName(None, u'status')), min_occurs=1, max_occurs=1)
    )
NodeHealth._ContentModel = pyxb.binding.content.ParticleModel(NodeHealth._GroupModel, min_occurs=1, max_occurs=1)



ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectLocation'), ObjectLocation, scope=ObjectLocationList, documentation=u'List of nodes from which the object can be\n                        retrieved'))

ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=ObjectLocationList, documentation=u'The identifier of the object being resolved.\n                    '))
ObjectLocationList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectLocation')), min_occurs=0L, max_occurs=None)
    )
ObjectLocationList._ContentModel = pyxb.binding.content.ParticleModel(ObjectLocationList._GroupModel, min_occurs=1, max_occurs=1)



AccessPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'allow'), AccessRule, scope=AccessPolicy))
AccessPolicy._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AccessPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'allow')), min_occurs=1L, max_occurs=None)
    )
AccessPolicy._ContentModel = pyxb.binding.content.ParticleModel(AccessPolicy._GroupModel, min_occurs=1, max_occurs=1)



AccessRule._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'permission'), Permission, scope=AccessRule))

AccessRule._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=AccessRule))
AccessRule._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AccessRule._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AccessRule._UseForTag(pyxb.namespace.ExpandedName(None, u'permission')), min_occurs=1L, max_occurs=None)
    )
AccessRule._ContentModel = pyxb.binding.content.ParticleModel(AccessRule._GroupModel, min_occurs=1, max_occurs=1)



ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'preference'), pyxb.binding.datatypes.int, scope=ObjectLocation, documentation=u'A weighting parameter that provides a hint to the caller \n                        for the relative preference for nodes from which the content should be retrieved.\n                    '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), NodeReference, scope=ObjectLocation, documentation=u'Identifier of the node (the same identifier used\n                        in the node registry for identifying the node.\n                    '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'url'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation=u'The full (absolute) URL that can be used to\n                        retrieve the object using the get() method of the rest interface.\n                    '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation=u'The current base URL for services implemented on the target node.\n                    '))
ObjectLocation._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'nodeIdentifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'baseURL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'url')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'preference')), min_occurs=0L, max_occurs=1L)
    )
ObjectLocation._ContentModel = pyxb.binding.content.ParticleModel(ObjectLocation._GroupModel, min_occurs=1, max_occurs=1)



Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation=u'The last time all the data from a node was pulled from a member node\n                    '))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'schedule'), Schedule, scope=Synchronization))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastHarvested'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation=u'The last time the mn sychronization daemon ran and found new data to synchronize\n                    '))
Synchronization._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'schedule')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastHarvested')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest')), min_occurs=1L, max_occurs=1L)
    )
Synchronization._ContentModel = pyxb.binding.content.ParticleModel(Synchronization._GroupModel, min_occurs=1, max_occurs=1)



MonitorInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'count'), pyxb.binding.datatypes.int, scope=MonitorInfo))

MonitorInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'date'), pyxb.binding.datatypes.date, scope=MonitorInfo))
MonitorInfo._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MonitorInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'date')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(MonitorInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'count')), min_occurs=1L, max_occurs=1L)
    )
MonitorInfo._ContentModel = pyxb.binding.content.ParticleModel(MonitorInfo._GroupModel, min_occurs=1, max_occurs=1)



Log._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'logEntry'), LogEntry, scope=Log))
Log._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Log._UseForTag(pyxb.namespace.ExpandedName(None, u'logEntry')), min_occurs=0L, max_occurs=None)
    )
Log._ContentModel = pyxb.binding.content.ParticleModel(Log._GroupModel, min_occurs=1, max_occurs=1)



ObjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectInfo'), ObjectInfo, scope=ObjectList))
ObjectList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectInfo')), min_occurs=0L, max_occurs=None)
    )
ObjectList._ContentModel = pyxb.binding.content.ParticleModel(ObjectList._GroupModel, min_occurs=1, max_occurs=1)



MonitorList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'monitorInfo'), MonitorInfo, scope=MonitorList))
MonitorList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MonitorList._UseForTag(pyxb.namespace.ExpandedName(None, u'monitorInfo')), min_occurs=0L, max_occurs=None)
    )
MonitorList._ContentModel = pyxb.binding.content.ParticleModel(MonitorList._GroupModel, min_occurs=1, max_occurs=1)



SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'size'), pyxb.binding.datatypes.long, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'obsoletedBy'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'obsoletes'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'checksum'), Checksum, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'submitter'), Subject, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'rightsHolder'), Subject, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'originMemberNode'), NodeReference, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'resourceMap'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode'), NodeReference, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateUploaded'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replica'), Replica, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'accessPolicy'), AccessPolicy, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectFormat'), ObjectFormat, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicationPolicy'), ReplicationPolicy, scope=SystemMetadata))
SystemMetadata._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'objectFormat')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'size')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'checksum')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'submitter')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'rightsHolder')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'accessPolicy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'replicationPolicy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'obsoletes')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'obsoletedBy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'resourceMap')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'dateUploaded')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'originMemberNode')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'replica')), min_occurs=0L, max_occurs=None)
    )
SystemMetadata._ContentModel = pyxb.binding.content.ParticleModel(SystemMetadata._GroupModel, min_occurs=1, max_occurs=1)



Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'hasMember'), Subject, scope=Group))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Group))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'groupName'), NonEmptyString, scope=Group))
Group._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Group._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Group._UseForTag(pyxb.namespace.ExpandedName(None, u'groupName')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Group._UseForTag(pyxb.namespace.ExpandedName(None, u'hasMember')), min_occurs=0L, max_occurs=None)
    )
Group._ContentModel = pyxb.binding.content.ParticleModel(Group._GroupModel, min_occurs=1, max_occurs=1)



Session._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subjectList'), SubjectList, scope=Session))

Session._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'subject'), Subject, scope=Session))
Session._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Session._UseForTag(pyxb.namespace.ExpandedName(None, u'subject')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Session._UseForTag(pyxb.namespace.ExpandedName(None, u'subjectList')), min_occurs=0L, max_occurs=1L)
    )
Session._ContentModel = pyxb.binding.content.ParticleModel(Session._GroupModel, min_occurs=1, max_occurs=1)



ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'size'), pyxb.binding.datatypes.long, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectFormat'), ObjectFormat, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'checksum'), Checksum, scope=ObjectInfo))
ObjectInfo._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'objectFormat')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'checksum')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'size')), min_occurs=1, max_occurs=1)
    )
ObjectInfo._ContentModel = pyxb.binding.content.ParticleModel(ObjectInfo._GroupModel, min_occurs=1, max_occurs=1)



Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicaVerified'), pyxb.binding.datatypes.dateTime, scope=Replica))

Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicaMemberNode'), NodeReference, scope=Replica))

Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicationStatus'), ReplicationStatus, scope=Replica))
Replica._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicaMemberNode')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicationStatus')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicaVerified')), min_occurs=1, max_occurs=1)
    )
Replica._ContentModel = pyxb.binding.content.ParticleModel(Replica._GroupModel, min_occurs=1, max_occurs=1)
