# ./pyxb/bundles/common/raw/xsd_hfp.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:c53ce1768a4a63294762e2dee968b656ae0d44d0
# Generated 2012-12-17 13:09:17.132772 by PyXB version 1.2.1
# Namespace http://www.w3.org/2001/XMLSchema-hasFacetAndProperty

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:40e19b70-487d-11e2-85d6-c8600024e903')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI('http://www.w3.org/2001/XMLSchema-hasFacetAndProperty', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.
    
    @kw default_namespace The L{pyxb.Namespace} instance to use as the
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
        return CreateFromDOM(dom.documentElement)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
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
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """
       
       
      """

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 60, 4)
    _Documentation = u'\n       \n       \n      '
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.length = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'length', tag=u'length')
STD_ANON.minLength = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'minLength', tag=u'minLength')
STD_ANON.maxLength = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'maxLength', tag=u'maxLength')
STD_ANON.pattern = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'pattern', tag=u'pattern')
STD_ANON.enumeration = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'enumeration', tag=u'enumeration')
STD_ANON.maxInclusive = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'maxInclusive', tag=u'maxInclusive')
STD_ANON.maxExclusive = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'maxExclusive', tag=u'maxExclusive')
STD_ANON.minInclusive = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'minInclusive', tag=u'minInclusive')
STD_ANON.minExclusive = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'minExclusive', tag=u'minExclusive')
STD_ANON.totalDigits = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'totalDigits', tag=u'totalDigits')
STD_ANON.fractionDigits = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'fractionDigits', tag=u'fractionDigits')
STD_ANON.whiteSpace = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'whiteSpace', tag=u'whiteSpace')
STD_ANON.maxScale = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'maxScale', tag=u'maxScale')
STD_ANON.minScale = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'minScale', tag=u'minScale')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """
       
       
      """

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 117, 4)
    _Documentation = u'\n       \n       \n      '
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.ordered = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'ordered', tag=u'ordered')
STD_ANON_.bounded = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'bounded', tag=u'bounded')
STD_ANON_.cardinality = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'cardinality', tag=u'cardinality')
STD_ANON_.numeric = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'numeric', tag=u'numeric')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Complex type [anonymous] with content type EMPTY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """
   
   
   
   """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 58, 2)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_w3_org2001XMLSchema_hasFacetAndProperty_CTD_ANON_name', STD_ANON, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 59, 3)
    __name._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 59, 3)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __name.name() : __name
    }



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """
    
    
    
   """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 115, 2)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_w3_org2001XMLSchema_hasFacetAndProperty_CTD_ANON__name', STD_ANON_, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 116, 3)
    __name._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 116, 3)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'value'), 'value_', '__httpwww_w3_org2001XMLSchema_hasFacetAndProperty_CTD_ANON__value', pyxb.binding.datatypes.normalizedString, required=True)
    __value._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 139, 3)
    __value._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 139, 3)
    
    value_ = property(__value.value, __value.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __name.name() : __name,
        __value.name() : __value
    }



hasFacet = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'hasFacet'), CTD_ANON, documentation=u'\n   \n   \n   \n   ', location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 35, 1))
Namespace.addCategoryObject('elementBinding', hasFacet.name().localName(), hasFacet)

hasProperty = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'hasProperty'), CTD_ANON_, documentation=u'\n    \n    \n    \n   ', location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/common/schemas/xsd_hfp.xsd', 97, 1))
Namespace.addCategoryObject('elementBinding', hasProperty.name().localName(), hasProperty)
