# ./pyxb/systemmetadata.py
# PyXB bindings for NamespaceModule
# NSM:ad83a62b16c5ba4e749e404d671cad04fd140a97
# Generated 2010-09-15 10:01:42.813827 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:88156dd4-c0e2-11df-9288-000c29f765e9')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import _common

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/SystemMetadata/0.1', create_if_missing=True)
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
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.read = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'read')
STD_ANON.write = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'write')
STD_ANON.changePermission = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'changePermission')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.allow = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'allow')
STD_ANON_.deny = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'deny')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_2 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_2, enum_prefix=None)
STD_ANON_2.true = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'true')
STD_ANON_2.false = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'false')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_3 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_3._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_3, enum_prefix=None)
STD_ANON_3.queued = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'queued')
STD_ANON_3.requested = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'requested')
STD_ANON_3.completed = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'completed')
STD_ANON_3.invalidated = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'invalidated')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_enumeration)

# Complex type AccessRule with content type EMPTY
class AccessRule (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AccessRule')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute service uses Python identifier service
    __service = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpdataone_orgservicetypesSystemMetadata0_1_AccessRule_service', STD_ANON)
    
    service = property(__service.value, __service.set, None, None)

    
    # Attribute rule uses Python identifier rule
    __rule = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'rule'), 'rule', '__httpdataone_orgservicetypesSystemMetadata0_1_AccessRule_rule', STD_ANON_)
    
    rule = property(__rule.value, __rule.set, None, None)

    
    # Attribute principal uses Python identifier principal
    __principal = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'principal'), 'principal', '__httpdataone_orgservicetypesSystemMetadata0_1_AccessRule_principal', _common.Principal)
    
    principal = property(__principal.value, __principal.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __service.name() : __service,
        __rule.name() : __rule,
        __principal.name() : __principal
    }
Namespace.addCategoryObject('typeBinding', u'AccessRule', AccessRule)


# Complex type ReplicationPolicy with content type ELEMENT_ONLY
class ReplicationPolicy (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReplicationPolicy')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element blockedMemberNode uses Python identifier blockedMemberNode
    __blockedMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'blockedMemberNode'), 'blockedMemberNode', '__httpdataone_orgservicetypesSystemMetadata0_1_ReplicationPolicy_blockedMemberNode', True)

    
    blockedMemberNode = property(__blockedMemberNode.value, __blockedMemberNode.set, None, None)

    
    # Element preferredMemberNode uses Python identifier preferredMemberNode
    __preferredMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'preferredMemberNode'), 'preferredMemberNode', '__httpdataone_orgservicetypesSystemMetadata0_1_ReplicationPolicy_preferredMemberNode', True)

    
    preferredMemberNode = property(__preferredMemberNode.value, __preferredMemberNode.set, None, None)

    
    # Attribute replicationAllowed uses Python identifier replicationAllowed
    __replicationAllowed = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'replicationAllowed'), 'replicationAllowed', '__httpdataone_orgservicetypesSystemMetadata0_1_ReplicationPolicy_replicationAllowed', STD_ANON_2)
    
    replicationAllowed = property(__replicationAllowed.value, __replicationAllowed.set, None, None)

    
    # Attribute numberReplicas uses Python identifier numberReplicas
    __numberReplicas = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'numberReplicas'), 'numberReplicas', '__httpdataone_orgservicetypesSystemMetadata0_1_ReplicationPolicy_numberReplicas', pyxb.binding.datatypes.int)
    
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


# Complex type SystemMetadata with content type ELEMENT_ONLY
class SystemMetadata (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SystemMetadata')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element accessRule uses Python identifier accessRule
    __accessRule = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'accessRule'), 'accessRule', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_accessRule', True)

    
    accessRule = property(__accessRule.value, __accessRule.set, None, None)

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_checksum', False)

    
    checksum = property(__checksum.value, __checksum.set, None, None)

    
    # Element submitter uses Python identifier submitter
    __submitter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'submitter'), 'submitter', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_submitter', False)

    
    submitter = property(__submitter.value, __submitter.set, None, None)

    
    # Element derivedFrom uses Python identifier derivedFrom
    __derivedFrom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'derivedFrom'), 'derivedFrom', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_derivedFrom', True)

    
    derivedFrom = property(__derivedFrom.value, __derivedFrom.set, None, None)

    
    # Element embargoExpires uses Python identifier embargoExpires
    __embargoExpires = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'embargoExpires'), 'embargoExpires', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_embargoExpires', False)

    
    embargoExpires = property(__embargoExpires.value, __embargoExpires.set, None, None)

    
    # Element dateUploaded uses Python identifier dateUploaded
    __dateUploaded = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateUploaded'), 'dateUploaded', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_dateUploaded', False)

    
    dateUploaded = property(__dateUploaded.value, __dateUploaded.set, None, None)

    
    # Element rightsHolder uses Python identifier rightsHolder
    __rightsHolder = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'rightsHolder'), 'rightsHolder', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_rightsHolder', False)

    
    rightsHolder = property(__rightsHolder.value, __rightsHolder.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element replicationPolicy uses Python identifier replicationPolicy
    __replicationPolicy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicationPolicy'), 'replicationPolicy', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_replicationPolicy', False)

    
    replicationPolicy = property(__replicationPolicy.value, __replicationPolicy.set, None, None)

    
    # Element authoritativeMemberNode uses Python identifier authoritativeMemberNode
    __authoritativeMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode'), 'authoritativeMemberNode', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_authoritativeMemberNode', False)

    
    authoritativeMemberNode = property(__authoritativeMemberNode.value, __authoritativeMemberNode.set, None, None)

    
    # Element size uses Python identifier size
    __size = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'size'), 'size', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_size', False)

    
    size = property(__size.value, __size.set, None, None)

    
    # Element obsoletedBy uses Python identifier obsoletedBy
    __obsoletedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'obsoletedBy'), 'obsoletedBy', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_obsoletedBy', True)

    
    obsoletedBy = property(__obsoletedBy.value, __obsoletedBy.set, None, None)

    
    # Element obsoletes uses Python identifier obsoletes
    __obsoletes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'obsoletes'), 'obsoletes', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_obsoletes', True)

    
    obsoletes = property(__obsoletes.value, __obsoletes.set, None, None)

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_dateSysMetadataModified', False)

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, None)

    
    # Element replica uses Python identifier replica
    __replica = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replica'), 'replica', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_replica', True)

    
    replica = property(__replica.value, __replica.set, None, None)

    
    # Element describes uses Python identifier describes
    __describes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'describes'), 'describes', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_describes', True)

    
    describes = property(__describes.value, __describes.set, None, None)

    
    # Element originMemberNode uses Python identifier originMemberNode
    __originMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'originMemberNode'), 'originMemberNode', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_originMemberNode', False)

    
    originMemberNode = property(__originMemberNode.value, __originMemberNode.set, None, None)

    
    # Element objectFormat uses Python identifier objectFormat
    __objectFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectFormat'), 'objectFormat', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_objectFormat', False)

    
    objectFormat = property(__objectFormat.value, __objectFormat.set, None, None)

    
    # Element describedBy uses Python identifier describedBy
    __describedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'describedBy'), 'describedBy', '__httpdataone_orgservicetypesSystemMetadata0_1_SystemMetadata_describedBy', True)

    
    describedBy = property(__describedBy.value, __describedBy.set, None, None)


    _ElementMap = {
        __accessRule.name() : __accessRule,
        __checksum.name() : __checksum,
        __submitter.name() : __submitter,
        __derivedFrom.name() : __derivedFrom,
        __embargoExpires.name() : __embargoExpires,
        __dateUploaded.name() : __dateUploaded,
        __rightsHolder.name() : __rightsHolder,
        __identifier.name() : __identifier,
        __replicationPolicy.name() : __replicationPolicy,
        __authoritativeMemberNode.name() : __authoritativeMemberNode,
        __size.name() : __size,
        __obsoletedBy.name() : __obsoletedBy,
        __obsoletes.name() : __obsoletes,
        __dateSysMetadataModified.name() : __dateSysMetadataModified,
        __replica.name() : __replica,
        __describes.name() : __describes,
        __originMemberNode.name() : __originMemberNode,
        __objectFormat.name() : __objectFormat,
        __describedBy.name() : __describedBy
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SystemMetadata', SystemMetadata)


# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element replicaVerified uses Python identifier replicaVerified
    __replicaVerified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicaVerified'), 'replicaVerified', '__httpdataone_orgservicetypesSystemMetadata0_1_CTD_ANON_replicaVerified', False)

    
    replicaVerified = property(__replicaVerified.value, __replicaVerified.set, None, None)

    
    # Element replicaMemberNode uses Python identifier replicaMemberNode
    __replicaMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicaMemberNode'), 'replicaMemberNode', '__httpdataone_orgservicetypesSystemMetadata0_1_CTD_ANON_replicaMemberNode', False)

    
    replicaMemberNode = property(__replicaMemberNode.value, __replicaMemberNode.set, None, None)

    
    # Element replicationStatus uses Python identifier replicationStatus
    __replicationStatus = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicationStatus'), 'replicationStatus', '__httpdataone_orgservicetypesSystemMetadata0_1_CTD_ANON_replicationStatus', False)

    
    replicationStatus = property(__replicationStatus.value, __replicationStatus.set, None, None)


    _ElementMap = {
        __replicaVerified.name() : __replicaVerified,
        __replicaMemberNode.name() : __replicaMemberNode,
        __replicationStatus.name() : __replicationStatus
    }
    _AttributeMap = {
        
    }



systemMetadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'systemMetadata'), SystemMetadata)
Namespace.addCategoryObject('elementBinding', systemMetadata.name().localName(), systemMetadata)



ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'blockedMemberNode'), _common.NodeReference, scope=ReplicationPolicy))

ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'preferredMemberNode'), _common.NodeReference, scope=ReplicationPolicy))
ReplicationPolicy._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'preferredMemberNode')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'blockedMemberNode')), min_occurs=0L, max_occurs=None)
    )
ReplicationPolicy._ContentModel = pyxb.binding.content.ParticleModel(ReplicationPolicy._GroupModel, min_occurs=1, max_occurs=1)



SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'accessRule'), AccessRule, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'checksum'), _common.Checksum, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'submitter'), _common.Principal, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'derivedFrom'), _common.Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'embargoExpires'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateUploaded'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'rightsHolder'), _common.Principal, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), _common.Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicationPolicy'), ReplicationPolicy, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode'), _common.NodeReference, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'size'), pyxb.binding.datatypes.long, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'obsoletedBy'), _common.Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'obsoletes'), _common.Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replica'), CTD_ANON, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'describes'), _common.Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'originMemberNode'), _common.NodeReference, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectFormat'), _common.ObjectFormat, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'describedBy'), _common.Identifier, scope=SystemMetadata))
SystemMetadata._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'objectFormat')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'size')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'submitter')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'rightsHolder')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'obsoletes')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'obsoletedBy')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'derivedFrom')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'describes')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'describedBy')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'checksum')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'embargoExpires')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'accessRule')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'replicationPolicy')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'dateUploaded')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'originMemberNode')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemMetadata._UseForTag(pyxb.namespace.ExpandedName(None, u'replica')), min_occurs=0L, max_occurs=None)
    )
SystemMetadata._ContentModel = pyxb.binding.content.ParticleModel(SystemMetadata._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicaVerified'), pyxb.binding.datatypes.dateTime, scope=CTD_ANON))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicaMemberNode'), _common.NodeReference, scope=CTD_ANON))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicationStatus'), STD_ANON_3, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'replicaMemberNode')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'replicationStatus')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'replicaVerified')), min_occurs=1, max_occurs=1)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)
