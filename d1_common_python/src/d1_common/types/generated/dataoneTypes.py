# ./d1_common/types/generated/dataoneTypes.py
# PyXB bindings for NamespaceModule
# NSM:d1ef279f3b9e8053cdac3124559191020a3fa490
# Generated 2011-02-11 16:42:18.245990 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:8fbe4d00-3638-11e0-9fdd-000c29f765e9')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/0.5.1', create_if_missing=True)
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
class NonEmptyString (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonEmptyString')
    _Documentation = None
NonEmptyString._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1L))
NonEmptyString._CF_pattern = pyxb.binding.facets.CF_pattern()
NonEmptyString._CF_pattern.addPattern(pattern=u'[\\s]*[\\S][\\s\\S]*')
NonEmptyString._InitializeFacetMap(NonEmptyString._CF_minLength,
   NonEmptyString._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'NonEmptyString', NonEmptyString)

# Atomic SimpleTypeDefinition
class ComponentVersion (NonEmptyString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ComponentVersion')
    _Documentation = None
ComponentVersion._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ComponentVersion', ComponentVersion)

# Atomic SimpleTypeDefinition
class NodeReference (NonEmptyString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeReference')
    _Documentation = None
NodeReference._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'NodeReference', NodeReference)

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

# Atomic SimpleTypeDefinition
class ObjectFormat (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectFormat')
    _Documentation = None
ObjectFormat._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ObjectFormat, enum_prefix=None)
ObjectFormat.emlecoinformatics_orgeml_2_0_0 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'eml://ecoinformatics.org/eml-2.0.0')
ObjectFormat.emlecoinformatics_orgeml_2_0_1 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'eml://ecoinformatics.org/eml-2.0.1')
ObjectFormat.emlecoinformatics_orgeml_2_1_0 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'eml://ecoinformatics.org/eml-2.1.0')
ObjectFormat.emlecoinformatics_orgeml_2_1_1 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'eml://ecoinformatics.org/eml-2.1.1')
ObjectFormat.FGDC_STD_001_1_1999 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'FGDC-STD-001.1-1999')
ObjectFormat.FGDC_STD_001_1998 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'FGDC-STD-001-1998')
ObjectFormat.INCITS_453_2009 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'INCITS 453-2009')
ObjectFormat.httpwww_unidata_ucar_edunamespacesnetcdfncml_2_2 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2')
ObjectFormat.CF_1_0 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'CF-1.0')
ObjectFormat.CF_1_1 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'CF-1.1')
ObjectFormat.CF_1_2 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'CF-1.2')
ObjectFormat.CF_1_3 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'CF-1.3')
ObjectFormat.CF_1_4 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'CF-1.4')
ObjectFormat.httpwww_cuahsi_orgwaterML1_0 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'http://www.cuahsi.org/waterML/1.0/')
ObjectFormat.httpwww_cuahsi_orgwaterML1_1 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'http://www.cuahsi.org/waterML/1.1/')
ObjectFormat.httpwww_loc_govMETS = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'http://www.loc.gov/METS/')
ObjectFormat.netCDF_3 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'netCDF-3')
ObjectFormat.netCDF_4 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'netCDF-4')
ObjectFormat.textplain = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'text/plain')
ObjectFormat.textcsv = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'text/csv')
ObjectFormat.imagebmp = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'image/bmp')
ObjectFormat.imagegif = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'image/gif')
ObjectFormat.imagejp2 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'image/jp2')
ObjectFormat.imagejpeg = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'image/jpeg')
ObjectFormat.imagepng = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'image/png')
ObjectFormat.imagesvgxml = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'image/svg+xml')
ObjectFormat.imagetiff = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'image/tiff')
ObjectFormat.httprs_tdwg_orgdwcxsdsimpledarwincore = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'http://rs.tdwg.org/dwc/xsd/simpledarwincore/')
ObjectFormat.httpdigir_netschemaconceptualdarwin20031_0darwin2_xsd = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'http://digir.net/schema/conceptual/darwin/2003/1.0/darwin2.xsd')
ObjectFormat.applicationoctet_stream = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'application/octet-stream')
ObjectFormat._InitializeFacetMap(ObjectFormat._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ObjectFormat', ObjectFormat)

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
class CrontabEntry (pyxb.binding.datatypes.token):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CrontabEntry')
    _Documentation = None
CrontabEntry._CF_pattern = pyxb.binding.facets.CF_pattern()
CrontabEntry._CF_pattern.addPattern(pattern=u'([\\*\\d]{1,2}[\\-,]?)+')
CrontabEntry._InitializeFacetMap(CrontabEntry._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'CrontabEntry', CrontabEntry)

# Atomic SimpleTypeDefinition
class ServiceName (NonEmptyString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceName')
    _Documentation = None
ServiceName._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ServiceName', ServiceName)

# Atomic SimpleTypeDefinition
class IdentifierFormat (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IdentifierFormat')
    _Documentation = None
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
class Principal (NonEmptyString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Principal')
    _Documentation = None
Principal._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'Principal', Principal)

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
class ServiceVersion (NonEmptyString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceVersion')
    _Documentation = None
ServiceVersion._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ServiceVersion', ServiceVersion)

# Atomic SimpleTypeDefinition
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.allow = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'allow')
STD_ANON.deny = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'deny')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.read = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'read')
STD_ANON_.write = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'write')
STD_ANON_.changePermission = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'changePermission')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

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

# Complex type Ping with content type EMPTY
class Ping (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Ping')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute lastSuccess uses Python identifier lastSuccess
    __lastSuccess = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'lastSuccess'), 'lastSuccess', '__httpdataone_orgservicetypes0_5_1_Ping_lastSuccess', pyxb.binding.datatypes.dateTime)
    
    lastSuccess = property(__lastSuccess.value, __lastSuccess.set, None, None)

    
    # Attribute success uses Python identifier success
    __success = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'success'), 'success', '__httpdataone_orgservicetypes0_5_1_Ping_success', pyxb.binding.datatypes.boolean)
    
    success = property(__success.value, __success.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __lastSuccess.name() : __lastSuccess,
        __success.name() : __success
    }
Namespace.addCategoryObject('typeBinding', u'Ping', Ping)


# Complex type Component with content type EMPTY
class Component (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Component')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpdataone_orgservicetypes0_5_1_Component_version', ComponentVersion, required=True)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpdataone_orgservicetypes0_5_1_Component_name', ComponentName, required=True)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __version.name() : __version,
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'Component', Component)


# Complex type Status with content type EMPTY
class Status (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Status')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute dateChecked uses Python identifier dateChecked
    __dateChecked = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dateChecked'), 'dateChecked', '__httpdataone_orgservicetypes0_5_1_Status_dateChecked', pyxb.binding.datatypes.dateTime, required=True)
    
    dateChecked = property(__dateChecked.value, __dateChecked.set, None, None)

    
    # Attribute success uses Python identifier success
    __success = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'success'), 'success', '__httpdataone_orgservicetypes0_5_1_Status_success', pyxb.binding.datatypes.boolean)
    
    success = property(__success.value, __success.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __dateChecked.name() : __dateChecked,
        __success.name() : __success
    }
Namespace.addCategoryObject('typeBinding', u'Status', Status)


# Complex type Synchronization with content type ELEMENT_ONLY
class Synchronization (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Synchronization')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element lastCompleteHarvest uses Python identifier lastCompleteHarvest
    __lastCompleteHarvest = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), 'lastCompleteHarvest', '__httpdataone_orgservicetypes0_5_1_Synchronization_lastCompleteHarvest', False)

    
    lastCompleteHarvest = property(__lastCompleteHarvest.value, __lastCompleteHarvest.set, None, u'The last time all the data from a node was pulled from a member node\n                    ')

    
    # Element schedule uses Python identifier schedule
    __schedule = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'schedule'), 'schedule', '__httpdataone_orgservicetypes0_5_1_Synchronization_schedule', False)

    
    schedule = property(__schedule.value, __schedule.set, None, None)

    
    # Element lastHarvested uses Python identifier lastHarvested
    __lastHarvested = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'lastHarvested'), 'lastHarvested', '__httpdataone_orgservicetypes0_5_1_Synchronization_lastHarvested', False)

    
    lastHarvested = property(__lastHarvested.value, __lastHarvested.set, None, u'The last time the mn sychronization daemon ran and found new data to synchronize\n                    ')


    _ElementMap = {
        __lastCompleteHarvest.name() : __lastCompleteHarvest,
        __schedule.name() : __schedule,
        __lastHarvested.name() : __lastHarvested
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Synchronization', Synchronization)


# Complex type NodeList with content type ELEMENT_ONLY
class NodeList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element node uses Python identifier node
    __node = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'node'), 'node', '__httpdataone_orgservicetypes0_5_1_NodeList_node', True)

    
    node = property(__node.value, __node.set, None, None)


    _ElementMap = {
        __node.name() : __node
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'NodeList', NodeList)


# Complex type Slice with content type EMPTY
class Slice (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Slice')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute count uses Python identifier count
    __count = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'count'), 'count', '__httpdataone_orgservicetypes0_5_1_Slice_count', pyxb.binding.datatypes.int, required=True)
    
    count = property(__count.value, __count.set, None, None)

    
    # Attribute start uses Python identifier start
    __start = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'start'), 'start', '__httpdataone_orgservicetypes0_5_1_Slice_start', pyxb.binding.datatypes.int, required=True)
    
    start = property(__start.value, __start.set, None, None)

    
    # Attribute total uses Python identifier total
    __total = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'total'), 'total', '__httpdataone_orgservicetypes0_5_1_Slice_total', pyxb.binding.datatypes.int, required=True)
    
    total = property(__total.value, __total.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __count.name() : __count,
        __start.name() : __start,
        __total.name() : __total
    }
Namespace.addCategoryObject('typeBinding', u'Slice', Slice)


# Complex type ObjectList with content type ELEMENT_ONLY
class ObjectList (Slice):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectList')
    # Base type is Slice
    
    # Element objectInfo uses Python identifier objectInfo
    __objectInfo = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectInfo'), 'objectInfo', '__httpdataone_orgservicetypes0_5_1_ObjectList_objectInfo', True)

    
    objectInfo = property(__objectInfo.value, __objectInfo.set, None, None)

    
    # Attribute count inherited from {http://dataone.org/service/types/0.5.1}Slice
    
    # Attribute start inherited from {http://dataone.org/service/types/0.5.1}Slice
    
    # Attribute total inherited from {http://dataone.org/service/types/0.5.1}Slice

    _ElementMap = Slice._ElementMap.copy()
    _ElementMap.update({
        __objectInfo.name() : __objectInfo
    })
    _AttributeMap = Slice._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ObjectList', ObjectList)


# Complex type SystemMetadata with content type ELEMENT_ONLY
class SystemMetadata (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SystemMetadata')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element obsoletes uses Python identifier obsoletes
    __obsoletes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'obsoletes'), 'obsoletes', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_obsoletes', True)

    
    obsoletes = property(__obsoletes.value, __obsoletes.set, None, None)

    
    # Element obsoletedBy uses Python identifier obsoletedBy
    __obsoletedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'obsoletedBy'), 'obsoletedBy', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_obsoletedBy', True)

    
    obsoletedBy = property(__obsoletedBy.value, __obsoletedBy.set, None, None)

    
    # Element describes uses Python identifier describes
    __describes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'describes'), 'describes', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_describes', True)

    
    describes = property(__describes.value, __describes.set, None, None)

    
    # Element dateUploaded uses Python identifier dateUploaded
    __dateUploaded = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateUploaded'), 'dateUploaded', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_dateUploaded', False)

    
    dateUploaded = property(__dateUploaded.value, __dateUploaded.set, None, None)

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_checksum', False)

    
    checksum = property(__checksum.value, __checksum.set, None, None)

    
    # Element derivedFrom uses Python identifier derivedFrom
    __derivedFrom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'derivedFrom'), 'derivedFrom', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_derivedFrom', True)

    
    derivedFrom = property(__derivedFrom.value, __derivedFrom.set, None, None)

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_dateSysMetadataModified', False)

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element originMemberNode uses Python identifier originMemberNode
    __originMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'originMemberNode'), 'originMemberNode', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_originMemberNode', False)

    
    originMemberNode = property(__originMemberNode.value, __originMemberNode.set, None, None)

    
    # Element replicationPolicy uses Python identifier replicationPolicy
    __replicationPolicy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicationPolicy'), 'replicationPolicy', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_replicationPolicy', False)

    
    replicationPolicy = property(__replicationPolicy.value, __replicationPolicy.set, None, None)

    
    # Element authoritativeMemberNode uses Python identifier authoritativeMemberNode
    __authoritativeMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode'), 'authoritativeMemberNode', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_authoritativeMemberNode', False)

    
    authoritativeMemberNode = property(__authoritativeMemberNode.value, __authoritativeMemberNode.set, None, None)

    
    # Element size uses Python identifier size
    __size = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'size'), 'size', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_size', False)

    
    size = property(__size.value, __size.set, None, None)

    
    # Element replica uses Python identifier replica
    __replica = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replica'), 'replica', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_replica', True)

    
    replica = property(__replica.value, __replica.set, None, None)

    
    # Element objectFormat uses Python identifier objectFormat
    __objectFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectFormat'), 'objectFormat', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_objectFormat', False)

    
    objectFormat = property(__objectFormat.value, __objectFormat.set, None, None)

    
    # Element describedBy uses Python identifier describedBy
    __describedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'describedBy'), 'describedBy', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_describedBy', True)

    
    describedBy = property(__describedBy.value, __describedBy.set, None, None)

    
    # Element accessRule uses Python identifier accessRule
    __accessRule = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'accessRule'), 'accessRule', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_accessRule', True)

    
    accessRule = property(__accessRule.value, __accessRule.set, None, None)

    
    # Element rightsHolder uses Python identifier rightsHolder
    __rightsHolder = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'rightsHolder'), 'rightsHolder', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_rightsHolder', False)

    
    rightsHolder = property(__rightsHolder.value, __rightsHolder.set, None, None)

    
    # Element embargoExpires uses Python identifier embargoExpires
    __embargoExpires = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'embargoExpires'), 'embargoExpires', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_embargoExpires', False)

    
    embargoExpires = property(__embargoExpires.value, __embargoExpires.set, None, None)

    
    # Element submitter uses Python identifier submitter
    __submitter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'submitter'), 'submitter', '__httpdataone_orgservicetypes0_5_1_SystemMetadata_submitter', False)

    
    submitter = property(__submitter.value, __submitter.set, None, None)


    _ElementMap = {
        __obsoletes.name() : __obsoletes,
        __obsoletedBy.name() : __obsoletedBy,
        __describes.name() : __describes,
        __dateUploaded.name() : __dateUploaded,
        __checksum.name() : __checksum,
        __derivedFrom.name() : __derivedFrom,
        __dateSysMetadataModified.name() : __dateSysMetadataModified,
        __identifier.name() : __identifier,
        __originMemberNode.name() : __originMemberNode,
        __replicationPolicy.name() : __replicationPolicy,
        __authoritativeMemberNode.name() : __authoritativeMemberNode,
        __size.name() : __size,
        __replica.name() : __replica,
        __objectFormat.name() : __objectFormat,
        __describedBy.name() : __describedBy,
        __accessRule.name() : __accessRule,
        __rightsHolder.name() : __rightsHolder,
        __embargoExpires.name() : __embargoExpires,
        __submitter.name() : __submitter
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SystemMetadata', SystemMetadata)


# Complex type Checksum with content type SIMPLE
class Checksum (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Checksum')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute algorithm uses Python identifier algorithm
    __algorithm = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'algorithm'), 'algorithm', '__httpdataone_orgservicetypes0_5_1_Checksum_algorithm', ChecksumAlgorithm, required=True)
    
    algorithm = property(__algorithm.value, __algorithm.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __algorithm.name() : __algorithm
    }
Namespace.addCategoryObject('typeBinding', u'Checksum', Checksum)


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


# Complex type Schedule with content type EMPTY
class Schedule (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Schedule')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute mon uses Python identifier mon
    __mon = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mon'), 'mon', '__httpdataone_orgservicetypes0_5_1_Schedule_mon', CrontabEntry, required=True)
    
    mon = property(__mon.value, __mon.set, None, None)

    
    # Attribute hour uses Python identifier hour
    __hour = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'hour'), 'hour', '__httpdataone_orgservicetypes0_5_1_Schedule_hour', CrontabEntry, required=True)
    
    hour = property(__hour.value, __hour.set, None, None)

    
    # Attribute sec uses Python identifier sec
    __sec = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'sec'), 'sec', '__httpdataone_orgservicetypes0_5_1_Schedule_sec', CrontabEntry, required=True)
    
    sec = property(__sec.value, __sec.set, None, None)

    
    # Attribute wday uses Python identifier wday
    __wday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'wday'), 'wday', '__httpdataone_orgservicetypes0_5_1_Schedule_wday', CrontabEntry, required=True)
    
    wday = property(__wday.value, __wday.set, None, None)

    
    # Attribute year uses Python identifier year
    __year = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'year'), 'year', '__httpdataone_orgservicetypes0_5_1_Schedule_year', CrontabEntry, required=True)
    
    year = property(__year.value, __year.set, None, None)

    
    # Attribute mday uses Python identifier mday
    __mday = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mday'), 'mday', '__httpdataone_orgservicetypes0_5_1_Schedule_mday', CrontabEntry, required=True)
    
    mday = property(__mday.value, __mday.set, None, None)

    
    # Attribute min uses Python identifier min
    __min = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'min'), 'min', '__httpdataone_orgservicetypes0_5_1_Schedule_min', CrontabEntry, required=True)
    
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


# Complex type ServiceMethod with content type EMPTY
class ServiceMethod (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceMethod')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute implemented uses Python identifier implemented
    __implemented = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'implemented'), 'implemented', '__httpdataone_orgservicetypes0_5_1_ServiceMethod_implemented', pyxb.binding.datatypes.boolean, required=True)
    
    implemented = property(__implemented.value, __implemented.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpdataone_orgservicetypes0_5_1_ServiceMethod_name', pyxb.binding.datatypes.NMTOKEN)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute rest uses Python identifier rest
    __rest = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'rest'), 'rest', '__httpdataone_orgservicetypes0_5_1_ServiceMethod_rest', pyxb.binding.datatypes.token, required=True)
    
    rest = property(__rest.value, __rest.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __implemented.name() : __implemented,
        __name.name() : __name,
        __rest.name() : __rest
    }
Namespace.addCategoryObject('typeBinding', u'ServiceMethod', ServiceMethod)


# Complex type ObjectLocationList with content type ELEMENT_ONLY
class ObjectLocationList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectLocationList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element objectLocation uses Python identifier objectLocation
    __objectLocation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectLocation'), 'objectLocation', '__httpdataone_orgservicetypes0_5_1_ObjectLocationList_objectLocation', True)

    
    objectLocation = property(__objectLocation.value, __objectLocation.set, None, u'List of nodes from which the object can be\n                        retrieved')

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypes0_5_1_ObjectLocationList_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'The identifier of the object being resolved.\n                    ')


    _ElementMap = {
        __objectLocation.name() : __objectLocation,
        __identifier.name() : __identifier
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectLocationList', ObjectLocationList)


# Complex type MonitorInfo with content type ELEMENT_ONLY
class MonitorInfo (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MonitorInfo')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element count uses Python identifier count
    __count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'count'), 'count', '__httpdataone_orgservicetypes0_5_1_MonitorInfo_count', False)

    
    count = property(__count.value, __count.set, None, None)

    
    # Element date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'date'), 'date', '__httpdataone_orgservicetypes0_5_1_MonitorInfo_date', False)

    
    date = property(__date.value, __date.set, None, None)


    _ElementMap = {
        __count.name() : __count,
        __date.name() : __date
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MonitorInfo', MonitorInfo)


# Complex type Node with content type ELEMENT_ONLY
class Node (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Node')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'baseURL'), 'baseURL', '__httpdataone_orgservicetypes0_5_1_Node_baseURL', False)

    
    baseURL = property(__baseURL.value, __baseURL.set, None, None)

    
    # Element synchronization uses Python identifier synchronization
    __synchronization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'synchronization'), 'synchronization', '__httpdataone_orgservicetypes0_5_1_Node_synchronization', False)

    
    synchronization = property(__synchronization.value, __synchronization.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypes0_5_1_Node_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, u'A unique identifier for the node. This may initially be the same as the\n                        baseURL, however this value should not change for future implementations of the same\n                        node, whereas the baseURL may change in the future. \n                    ')

    
    # Element services uses Python identifier services
    __services = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'services'), 'services', '__httpdataone_orgservicetypes0_5_1_Node_services', False)

    
    services = property(__services.value, __services.set, None, None)

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpdataone_orgservicetypes0_5_1_Node_name', False)

    
    name = property(__name.value, __name.set, None, u'A human readable name of the Node. \n                        The name of the node is being used in Mercury currently to assign a path,\n                        so format should be consistent with dataone directory naming conventions\n                    ')

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__httpdataone_orgservicetypes0_5_1_Node_description', False)

    
    description = property(__description.value, __description.set, None, u'Description of content maintained by this node and any other free style\n                        notes. May be we should allow CDATA element with the purpose of using for display\n                    ')

    
    # Element health uses Python identifier health
    __health = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'health'), 'health', '__httpdataone_orgservicetypes0_5_1_Node_health', False)

    
    health = property(__health.value, __health.set, None, u'The name of the node is being used in Mercury currently to assign a\n                        path, so format should be consistent with dataone directory naming conventions\n                    ')

    
    # Attribute environment uses Python identifier environment
    __environment = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'environment'), 'environment', '__httpdataone_orgservicetypes0_5_1_Node_environment', Environment)
    
    environment = property(__environment.value, __environment.set, None, None)

    
    # Attribute synchronize uses Python identifier synchronize
    __synchronize = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'synchronize'), 'synchronize', '__httpdataone_orgservicetypes0_5_1_Node_synchronize', pyxb.binding.datatypes.boolean, required=True)
    
    synchronize = property(__synchronize.value, __synchronize.set, None, None)

    
    # Attribute replicate uses Python identifier replicate
    __replicate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'replicate'), 'replicate', '__httpdataone_orgservicetypes0_5_1_Node_replicate', pyxb.binding.datatypes.boolean, required=True)
    
    replicate = property(__replicate.value, __replicate.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'type'), 'type', '__httpdataone_orgservicetypes0_5_1_Node_type', NodeType, required=True)
    
    type = property(__type.value, __type.set, None, None)


    _ElementMap = {
        __baseURL.name() : __baseURL,
        __synchronization.name() : __synchronization,
        __identifier.name() : __identifier,
        __services.name() : __services,
        __name.name() : __name,
        __description.name() : __description,
        __health.name() : __health
    }
    _AttributeMap = {
        __environment.name() : __environment,
        __synchronize.name() : __synchronize,
        __replicate.name() : __replicate,
        __type.name() : __type
    }
Namespace.addCategoryObject('typeBinding', u'Node', Node)


# Complex type Service with content type ELEMENT_ONLY
class Service (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Service')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element method uses Python identifier method
    __method = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'method'), 'method', '__httpdataone_orgservicetypes0_5_1_Service_method', True)

    
    method = property(__method.value, __method.set, None, None)

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpdataone_orgservicetypes0_5_1_Service_name', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute available uses Python identifier available
    __available = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'available'), 'available', '__httpdataone_orgservicetypes0_5_1_Service_available', pyxb.binding.datatypes.boolean)
    
    available = property(__available.value, __available.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpdataone_orgservicetypes0_5_1_Service_version', ServiceVersion, required=True)
    
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


# Complex type AccessRule with content type EMPTY
class AccessRule (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AccessRule')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute service uses Python identifier service
    __service = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpdataone_orgservicetypes0_5_1_AccessRule_service', STD_ANON_)
    
    service = property(__service.value, __service.set, None, None)

    
    # Attribute rule uses Python identifier rule
    __rule = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'rule'), 'rule', '__httpdataone_orgservicetypes0_5_1_AccessRule_rule', STD_ANON)
    
    rule = property(__rule.value, __rule.set, None, None)

    
    # Attribute principal uses Python identifier principal
    __principal = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'principal'), 'principal', '__httpdataone_orgservicetypes0_5_1_AccessRule_principal', Principal)
    
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
    __blockedMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'blockedMemberNode'), 'blockedMemberNode', '__httpdataone_orgservicetypes0_5_1_ReplicationPolicy_blockedMemberNode', True)

    
    blockedMemberNode = property(__blockedMemberNode.value, __blockedMemberNode.set, None, None)

    
    # Element preferredMemberNode uses Python identifier preferredMemberNode
    __preferredMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'preferredMemberNode'), 'preferredMemberNode', '__httpdataone_orgservicetypes0_5_1_ReplicationPolicy_preferredMemberNode', True)

    
    preferredMemberNode = property(__preferredMemberNode.value, __preferredMemberNode.set, None, None)

    
    # Attribute replicationAllowed uses Python identifier replicationAllowed
    __replicationAllowed = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'replicationAllowed'), 'replicationAllowed', '__httpdataone_orgservicetypes0_5_1_ReplicationPolicy_replicationAllowed', pyxb.binding.datatypes.boolean)
    
    replicationAllowed = property(__replicationAllowed.value, __replicationAllowed.set, None, None)

    
    # Attribute numberReplicas uses Python identifier numberReplicas
    __numberReplicas = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'numberReplicas'), 'numberReplicas', '__httpdataone_orgservicetypes0_5_1_ReplicationPolicy_numberReplicas', pyxb.binding.datatypes.int)
    
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


# Complex type ObjectLocation with content type ELEMENT_ONLY
class ObjectLocation (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectLocation')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element preference uses Python identifier preference
    __preference = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'preference'), 'preference', '__httpdataone_orgservicetypes0_5_1_ObjectLocation_preference', False)

    
    preference = property(__preference.value, __preference.set, None, u'A weighting parameter that provides a hint to the caller \n                        for the relative preference for nodes from which the content should be retrieved.\n                    ')

    
    # Element nodeIdentifier uses Python identifier nodeIdentifier
    __nodeIdentifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), 'nodeIdentifier', '__httpdataone_orgservicetypes0_5_1_ObjectLocation_nodeIdentifier', False)

    
    nodeIdentifier = property(__nodeIdentifier.value, __nodeIdentifier.set, None, u'Identifier of the node (the same identifier used\n                        in the node registry for identifying the node.\n                    ')

    
    # Element url uses Python identifier url
    __url = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'url'), 'url', '__httpdataone_orgservicetypes0_5_1_ObjectLocation_url', False)

    
    url = property(__url.value, __url.set, None, u'The full (absolute) URL that can be used to\n                        retrieve the object using the get() method of the rest interface.\n                    ')

    
    # Element baseURL uses Python identifier baseURL
    __baseURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'baseURL'), 'baseURL', '__httpdataone_orgservicetypes0_5_1_ObjectLocation_baseURL', False)

    
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


# Complex type Services with content type ELEMENT_ONLY
class Services (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Services')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element service uses Python identifier service
    __service = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpdataone_orgservicetypes0_5_1_Services_service', True)

    
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
    __status = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'status'), 'status', '__httpdataone_orgservicetypes0_5_1_NodeHealth_status', False)

    
    status = property(__status.value, __status.set, None, None)

    
    # Element ping uses Python identifier ping
    __ping = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ping'), 'ping', '__httpdataone_orgservicetypes0_5_1_NodeHealth_ping', False)

    
    ping = property(__ping.value, __ping.set, None, None)

    
    # Attribute state uses Python identifier state
    __state = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'state'), 'state', '__httpdataone_orgservicetypes0_5_1_NodeHealth_state', NodeState, required=True)
    
    state = property(__state.value, __state.set, None, None)


    _ElementMap = {
        __status.name() : __status,
        __ping.name() : __ping
    }
    _AttributeMap = {
        __state.name() : __state
    }
Namespace.addCategoryObject('typeBinding', u'NodeHealth', NodeHealth)


# Complex type MonitorList with content type ELEMENT_ONLY
class MonitorList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MonitorList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element monitorInfo uses Python identifier monitorInfo
    __monitorInfo = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'monitorInfo'), 'monitorInfo', '__httpdataone_orgservicetypes0_5_1_MonitorList_monitorInfo', True)

    
    monitorInfo = property(__monitorInfo.value, __monitorInfo.set, None, None)


    _ElementMap = {
        __monitorInfo.name() : __monitorInfo
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MonitorList', MonitorList)


# Complex type LogEntry with content type ELEMENT_ONLY
class LogEntry (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LogEntry')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element entryId uses Python identifier entryId
    __entryId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'entryId'), 'entryId', '__httpdataone_orgservicetypes0_5_1_LogEntry_entryId', False)

    
    entryId = property(__entryId.value, __entryId.set, None, None)

    
    # Element ipAddress uses Python identifier ipAddress
    __ipAddress = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ipAddress'), 'ipAddress', '__httpdataone_orgservicetypes0_5_1_LogEntry_ipAddress', False)

    
    ipAddress = property(__ipAddress.value, __ipAddress.set, None, None)

    
    # Element userAgent uses Python identifier userAgent
    __userAgent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'userAgent'), 'userAgent', '__httpdataone_orgservicetypes0_5_1_LogEntry_userAgent', False)

    
    userAgent = property(__userAgent.value, __userAgent.set, None, None)

    
    # Element principal uses Python identifier principal
    __principal = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'principal'), 'principal', '__httpdataone_orgservicetypes0_5_1_LogEntry_principal', False)

    
    principal = property(__principal.value, __principal.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypes0_5_1_LogEntry_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element event uses Python identifier event
    __event = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'event'), 'event', '__httpdataone_orgservicetypes0_5_1_LogEntry_event', False)

    
    event = property(__event.value, __event.set, None, None)

    
    # Element dateLogged uses Python identifier dateLogged
    __dateLogged = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateLogged'), 'dateLogged', '__httpdataone_orgservicetypes0_5_1_LogEntry_dateLogged', False)

    
    dateLogged = property(__dateLogged.value, __dateLogged.set, None, None)

    
    # Element memberNode uses Python identifier memberNode
    __memberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'memberNode'), 'memberNode', '__httpdataone_orgservicetypes0_5_1_LogEntry_memberNode', False)

    
    memberNode = property(__memberNode.value, __memberNode.set, None, None)


    _ElementMap = {
        __entryId.name() : __entryId,
        __ipAddress.name() : __ipAddress,
        __userAgent.name() : __userAgent,
        __principal.name() : __principal,
        __identifier.name() : __identifier,
        __event.name() : __event,
        __dateLogged.name() : __dateLogged,
        __memberNode.name() : __memberNode
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LogEntry', LogEntry)


# Complex type Replica with content type ELEMENT_ONLY
class Replica (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Replica')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element replicaVerified uses Python identifier replicaVerified
    __replicaVerified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicaVerified'), 'replicaVerified', '__httpdataone_orgservicetypes0_5_1_Replica_replicaVerified', False)

    
    replicaVerified = property(__replicaVerified.value, __replicaVerified.set, None, None)

    
    # Element replicaMemberNode uses Python identifier replicaMemberNode
    __replicaMemberNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicaMemberNode'), 'replicaMemberNode', '__httpdataone_orgservicetypes0_5_1_Replica_replicaMemberNode', False)

    
    replicaMemberNode = property(__replicaMemberNode.value, __replicaMemberNode.set, None, None)

    
    # Element replicationStatus uses Python identifier replicationStatus
    __replicationStatus = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'replicationStatus'), 'replicationStatus', '__httpdataone_orgservicetypes0_5_1_Replica_replicationStatus', False)

    
    replicationStatus = property(__replicationStatus.value, __replicationStatus.set, None, None)


    _ElementMap = {
        __replicaVerified.name() : __replicaVerified,
        __replicaMemberNode.name() : __replicaMemberNode,
        __replicationStatus.name() : __replicationStatus
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'Replica', Replica)


# Complex type ComponentList with content type ELEMENT_ONLY
class ComponentList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ComponentList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element component uses Python identifier component
    __component = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'component'), 'component', '__httpdataone_orgservicetypes0_5_1_ComponentList_component', False)

    
    component = property(__component.value, __component.set, None, None)


    _ElementMap = {
        __component.name() : __component
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ComponentList', ComponentList)


# Complex type ObjectInfo with content type ELEMENT_ONLY
class ObjectInfo (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectInfo')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element size uses Python identifier size
    __size = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'size'), 'size', '__httpdataone_orgservicetypes0_5_1_ObjectInfo_size', False)

    
    size = property(__size.value, __size.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpdataone_orgservicetypes0_5_1_ObjectInfo_identifier', False)

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__httpdataone_orgservicetypes0_5_1_ObjectInfo_checksum', False)

    
    checksum = property(__checksum.value, __checksum.set, None, None)

    
    # Element dateSysMetadataModified uses Python identifier dateSysMetadataModified
    __dateSysMetadataModified = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), 'dateSysMetadataModified', '__httpdataone_orgservicetypes0_5_1_ObjectInfo_dateSysMetadataModified', False)

    
    dateSysMetadataModified = property(__dateSysMetadataModified.value, __dateSysMetadataModified.set, None, None)

    
    # Element objectFormat uses Python identifier objectFormat
    __objectFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'objectFormat'), 'objectFormat', '__httpdataone_orgservicetypes0_5_1_ObjectInfo_objectFormat', False)

    
    objectFormat = property(__objectFormat.value, __objectFormat.set, None, None)


    _ElementMap = {
        __size.name() : __size,
        __identifier.name() : __identifier,
        __checksum.name() : __checksum,
        __dateSysMetadataModified.name() : __dateSysMetadataModified,
        __objectFormat.name() : __objectFormat
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ObjectInfo', ObjectInfo)


# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (Slice):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is Slice
    
    # Element logEntry uses Python identifier logEntry
    __logEntry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'logEntry'), 'logEntry', '__httpdataone_orgservicetypes0_5_1_CTD_ANON_logEntry', True)

    
    logEntry = property(__logEntry.value, __logEntry.set, None, None)

    
    # Attribute count inherited from {http://dataone.org/service/types/0.5.1}Slice
    
    # Attribute start inherited from {http://dataone.org/service/types/0.5.1}Slice
    
    # Attribute total inherited from {http://dataone.org/service/types/0.5.1}Slice

    _ElementMap = Slice._ElementMap.copy()
    _ElementMap.update({
        __logEntry.name() : __logEntry
    })
    _AttributeMap = Slice._AttributeMap.copy()
    _AttributeMap.update({
        
    })



nodeList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'nodeList'), NodeList)
Namespace.addCategoryObject('elementBinding', nodeList.name().localName(), nodeList)

objectList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectList'), ObjectList)
Namespace.addCategoryObject('elementBinding', objectList.name().localName(), objectList)

systemMetadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'systemMetadata'), SystemMetadata)
Namespace.addCategoryObject('elementBinding', systemMetadata.name().localName(), systemMetadata)

objectLocationList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objectLocationList'), ObjectLocationList)
Namespace.addCategoryObject('elementBinding', objectLocationList.name().localName(), objectLocationList)

monitorList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'monitorList'), MonitorList)
Namespace.addCategoryObject('elementBinding', monitorList.name().localName(), monitorList)

checksum = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'checksum'), Checksum)
Namespace.addCategoryObject('elementBinding', checksum.name().localName(), checksum)

componentList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'componentList'), ComponentList)
Namespace.addCategoryObject('elementBinding', componentList.name().localName(), componentList)

identifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'identifier'), Identifier)
Namespace.addCategoryObject('elementBinding', identifier.name().localName(), identifier)

log = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'log'), CTD_ANON)
Namespace.addCategoryObject('elementBinding', log.name().localName(), log)



Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation=u'The last time all the data from a node was pulled from a member node\n                    '))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'schedule'), Schedule, scope=Synchronization))

Synchronization._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'lastHarvested'), pyxb.binding.datatypes.dateTime, scope=Synchronization, documentation=u'The last time the mn sychronization daemon ran and found new data to synchronize\n                    '))
Synchronization._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'schedule')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastHarvested')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Synchronization._UseForTag(pyxb.namespace.ExpandedName(None, u'lastCompleteHarvest')), min_occurs=1, max_occurs=1)
    )
Synchronization._ContentModel = pyxb.binding.content.ParticleModel(Synchronization._GroupModel, min_occurs=1, max_occurs=1)



NodeList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'node'), Node, scope=NodeList))
NodeList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NodeList._UseForTag(pyxb.namespace.ExpandedName(None, u'node')), min_occurs=1L, max_occurs=None)
    )
NodeList._ContentModel = pyxb.binding.content.ParticleModel(NodeList._GroupModel, min_occurs=1, max_occurs=1)



ObjectList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectInfo'), ObjectInfo, scope=ObjectList))
ObjectList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectInfo')), min_occurs=0L, max_occurs=None)
    )
ObjectList._ContentModel = pyxb.binding.content.ParticleModel(ObjectList._GroupModel, min_occurs=1, max_occurs=1)



SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'obsoletes'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'obsoletedBy'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'describes'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateUploaded'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'checksum'), Checksum, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'derivedFrom'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'originMemberNode'), NodeReference, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicationPolicy'), ReplicationPolicy, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'authoritativeMemberNode'), NodeReference, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'size'), pyxb.binding.datatypes.long, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replica'), Replica, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectFormat'), ObjectFormat, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'describedBy'), Identifier, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'accessRule'), AccessRule, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'rightsHolder'), Principal, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'embargoExpires'), pyxb.binding.datatypes.dateTime, scope=SystemMetadata))

SystemMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'submitter'), Principal, scope=SystemMetadata))
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



ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectLocation'), ObjectLocation, scope=ObjectLocationList, documentation=u'List of nodes from which the object can be\n                        retrieved'))

ObjectLocationList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=ObjectLocationList, documentation=u'The identifier of the object being resolved.\n                    '))
ObjectLocationList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocationList._UseForTag(pyxb.namespace.ExpandedName(None, u'objectLocation')), min_occurs=0L, max_occurs=None)
    )
ObjectLocationList._ContentModel = pyxb.binding.content.ParticleModel(ObjectLocationList._GroupModel, min_occurs=1, max_occurs=1)



MonitorInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'count'), pyxb.binding.datatypes.int, scope=MonitorInfo))

MonitorInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'date'), pyxb.binding.datatypes.date, scope=MonitorInfo))
MonitorInfo._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MonitorInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'date')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(MonitorInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'count')), min_occurs=1L, max_occurs=1L)
    )
MonitorInfo._ContentModel = pyxb.binding.content.ParticleModel(MonitorInfo._GroupModel, min_occurs=1, max_occurs=1)



Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'synchronization'), Synchronization, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), NodeReference, scope=Node, documentation=u'A unique identifier for the node. This may initially be the same as the\n                        baseURL, however this value should not change for future implementations of the same\n                        node, whereas the baseURL may change in the future. \n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'services'), Services, scope=Node))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), NonEmptyString, scope=Node, documentation=u'A human readable name of the Node. \n                        The name of the node is being used in Mercury currently to assign a path,\n                        so format should be consistent with dataone directory naming conventions\n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'description'), NonEmptyString, scope=Node, documentation=u'Description of content maintained by this node and any other free style\n                        notes. May be we should allow CDATA element with the purpose of using for display\n                    '))

Node._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'health'), NodeHealth, scope=Node, documentation=u'The name of the node is being used in Mercury currently to assign a\n                        path, so format should be consistent with dataone directory naming conventions\n                    '))
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



Service._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'method'), ServiceMethod, scope=Service))

Service._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), ServiceName, scope=Service))
Service._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Service._UseForTag(pyxb.namespace.ExpandedName(None, u'name')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(Service._UseForTag(pyxb.namespace.ExpandedName(None, u'method')), min_occurs=0L, max_occurs=None)
    )
Service._ContentModel = pyxb.binding.content.ParticleModel(Service._GroupModel, min_occurs=1, max_occurs=1)



ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'blockedMemberNode'), NodeReference, scope=ReplicationPolicy))

ReplicationPolicy._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'preferredMemberNode'), NodeReference, scope=ReplicationPolicy))
ReplicationPolicy._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'preferredMemberNode')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ReplicationPolicy._UseForTag(pyxb.namespace.ExpandedName(None, u'blockedMemberNode')), min_occurs=0L, max_occurs=None)
    )
ReplicationPolicy._ContentModel = pyxb.binding.content.ParticleModel(ReplicationPolicy._GroupModel, min_occurs=1, max_occurs=1)



ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'preference'), pyxb.binding.datatypes.integer, scope=ObjectLocation, documentation=u'A weighting parameter that provides a hint to the caller \n                        for the relative preference for nodes from which the content should be retrieved.\n                    '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'nodeIdentifier'), Identifier, scope=ObjectLocation, documentation=u'Identifier of the node (the same identifier used\n                        in the node registry for identifying the node.\n                    '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'url'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation=u'The full (absolute) URL that can be used to\n                        retrieve the object using the get() method of the rest interface.\n                    '))

ObjectLocation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'baseURL'), pyxb.binding.datatypes.anyURI, scope=ObjectLocation, documentation=u'The current base URL for services implemented on the target node.\n                    '))
ObjectLocation._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'nodeIdentifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'baseURL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'url')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectLocation._UseForTag(pyxb.namespace.ExpandedName(None, u'preference')), min_occurs=0L, max_occurs=1L)
    )
ObjectLocation._ContentModel = pyxb.binding.content.ParticleModel(ObjectLocation._GroupModel, min_occurs=1, max_occurs=1)



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



MonitorList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'monitorInfo'), MonitorInfo, scope=MonitorList))
MonitorList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MonitorList._UseForTag(pyxb.namespace.ExpandedName(None, u'monitorInfo')), min_occurs=0L, max_occurs=None)
    )
MonitorList._ContentModel = pyxb.binding.content.ParticleModel(MonitorList._GroupModel, min_occurs=1, max_occurs=1)



LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'entryId'), Identifier, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ipAddress'), pyxb.binding.datatypes.string, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'userAgent'), pyxb.binding.datatypes.string, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'principal'), Principal, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'event'), Event, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateLogged'), pyxb.binding.datatypes.dateTime, scope=LogEntry))

LogEntry._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'memberNode'), NodeReference, scope=LogEntry))
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



Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicaVerified'), pyxb.binding.datatypes.dateTime, scope=Replica))

Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicaMemberNode'), NodeReference, scope=Replica))

Replica._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'replicationStatus'), ReplicationStatus, scope=Replica))
Replica._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicaMemberNode')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicationStatus')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(Replica._UseForTag(pyxb.namespace.ExpandedName(None, u'replicaVerified')), min_occurs=1, max_occurs=1)
    )
Replica._ContentModel = pyxb.binding.content.ParticleModel(Replica._GroupModel, min_occurs=1, max_occurs=1)



ComponentList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'component'), Component, scope=ComponentList))
ComponentList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ComponentList._UseForTag(pyxb.namespace.ExpandedName(None, u'component')), min_occurs=1, max_occurs=1)
    )
ComponentList._ContentModel = pyxb.binding.content.ParticleModel(ComponentList._GroupModel, min_occurs=1, max_occurs=1)



ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'size'), pyxb.binding.datatypes.long, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), Identifier, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'checksum'), Checksum, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified'), pyxb.binding.datatypes.dateTime, scope=ObjectInfo))

ObjectInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'objectFormat'), ObjectFormat, scope=ObjectInfo))
ObjectInfo._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'objectFormat')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'checksum')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'dateSysMetadataModified')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObjectInfo._UseForTag(pyxb.namespace.ExpandedName(None, u'size')), min_occurs=1, max_occurs=1)
    )
ObjectInfo._ContentModel = pyxb.binding.content.ParticleModel(ObjectInfo._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'logEntry'), LogEntry, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'logEntry')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)
