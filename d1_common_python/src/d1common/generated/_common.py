# d1generated/_common.py
# PyXB bindings for NamespaceModule
# NSM:cc95dcea7ffc87390c2ad21660a741b26761176b
# Generated 2010-06-28 16:44:35.585545 by PyXB version 1.1.1
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:f47b93de-82f5-11df-8800-00264a005868')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/common/0.1', create_if_missing=True)
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

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonEmptyString')
    _Documentation = None
NonEmptyString._CF_pattern = pyxb.binding.facets.CF_pattern()
NonEmptyString._CF_pattern.addPattern(pattern=u'[\\s]*[\\S][\\s\\S]*')
NonEmptyString._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1L))
NonEmptyString._InitializeFacetMap(NonEmptyString._CF_pattern,
   NonEmptyString._CF_minLength)
Namespace.addCategoryObject('typeBinding', u'NonEmptyString', NonEmptyString)

# Atomic SimpleTypeDefinition
class NodeReference (NonEmptyString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NodeReference')
    _Documentation = None
NodeReference._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'NodeReference', NodeReference)

# Atomic SimpleTypeDefinition
class Identifier (NonEmptyString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Identifier')
    _Documentation = None
Identifier._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'Identifier', Identifier)

# Atomic SimpleTypeDefinition
class Principal (NonEmptyString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Principal')
    _Documentation = None
Principal._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'Principal', Principal)

# Atomic SimpleTypeDefinition
class ObjectFormat (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObjectFormat')
    _Documentation = None
ObjectFormat._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ObjectFormat, enum_prefix=None)
ObjectFormat.emlecoinformatics_orgeml_2_0_0 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'eml://ecoinformatics.org/eml-2.0.0')
ObjectFormat.emlecoinformatics_orgeml_2_0_1 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'eml://ecoinformatics.org/eml-2.0.1')
ObjectFormat.emlecoinformatics_orgeml_2_1_0 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'eml://ecoinformatics.org/eml-2.1.0')
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
ObjectFormat.DSPACE_METS_SIP_Profile_1_0 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'DSPACE METS SIP Profile 1.0')
ObjectFormat.netCDF_3 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'netCDF-3')
ObjectFormat.netCDF_4 = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'netCDF-4')
ObjectFormat.textplain = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'text/plain')
ObjectFormat.textcsv = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'text/csv')
ObjectFormat.imagegif = ObjectFormat._CF_enumeration.addEnumeration(unicode_value=u'image/gif')
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

# Complex type Checksum with content type SIMPLE
class Checksum (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Checksum')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute algorithm uses Python identifier algorithm
    __algorithm = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'algorithm'), 'algorithm', '__httpdataone_orgservicetypescommon0_1_Checksum_algorithm', ChecksumAlgorithm, required=True)
    
    algorithm = property(__algorithm.value, __algorithm.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __algorithm.name() : __algorithm
    }
Namespace.addCategoryObject('typeBinding', u'Checksum', Checksum)

