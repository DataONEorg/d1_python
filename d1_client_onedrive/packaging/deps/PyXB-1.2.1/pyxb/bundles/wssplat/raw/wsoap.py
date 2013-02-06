# ./pyxb/bundles/wssplat/raw/wsoap.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:3a38467dbfe17f8bf02ac4151ad87deda2d076d0
# Generated 2012-12-17 13:09:29.263393 by PyXB version 1.2.1
# Namespace http://www.w3.org/ns/wsdl/soap

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:481911c0-487d-11e2-8724-c8600024e903')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.wssplat.wsdl20

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.w3.org/ns/wsdl/soap', create_if_missing=True)
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


# Atomic simple type: {http://www.w3.org/ns/wsdl/soap}TokenAny
class TokenAny (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TokenAny')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 55, 1)
    _Documentation = None
TokenAny._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=TokenAny, enum_prefix=None)
TokenAny.any = TokenAny._CF_enumeration.addEnumeration(unicode_value=u'#any', tag=u'any')
TokenAny._InitializeFacetMap(TokenAny._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'TokenAny', TokenAny)

# List simple type: [anonymous]
# superclasses pyxb.binding.datatypes.anySimpleType
class STD_ANON (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.QName."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 70, 2)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.QName
STD_ANON._InitializeFacetMap()

# Union simple type: [anonymous]
# superclasses pyxb.binding.datatypes.anySimpleType
class STD_ANON_ (pyxb.binding.basis.STD_union):

    """Simple type that is a union of pyxb.binding.datatypes.QName, TokenAny."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 62, 3)
    _Documentation = None

    _MemberTypes = ( pyxb.binding.datatypes.QName, TokenAny, )
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_)
STD_ANON_._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_.any = u'#any'                           # originally TokenAny.any
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration,
   STD_ANON_._CF_pattern)

# Union simple type: [anonymous]
# superclasses pyxb.binding.datatypes.anySimpleType
class STD_ANON_2 (pyxb.binding.basis.STD_union):

    """Simple type that is a union of TokenAny, STD_ANON."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 68, 3)
    _Documentation = None

    _MemberTypes = ( TokenAny, STD_ANON, )
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_2)
STD_ANON_2._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_2.any = u'#any'                          # originally TokenAny.any
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration,
   STD_ANON_2._CF_pattern)

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.bundles.wssplat.wsdl20.ExtensibleDocumentedType):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 33, 2)
    # Base type is pyxb.bundles.wssplat.wsdl20.ExtensibleDocumentedType
    
    # Element documentation ({http://www.w3.org/ns/wsdl}documentation) inherited from {http://www.w3.org/ns/wsdl}DocumentedType
    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ref'), 'ref', '__httpwww_w3_orgnswsdlsoap_CTD_ANON_ref', pyxb.binding.datatypes.anyURI, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 36, 5)
    __ref._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 36, 5)
    
    ref = property(__ref.value, __ref.set, None, None)

    
    # Attribute required uses Python identifier required
    __required = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'required'), 'required', '__httpwww_w3_orgnswsdlsoap_CTD_ANON_required', pyxb.binding.datatypes.boolean)
    __required._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 37, 5)
    __required._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 37, 5)
    
    required = property(__required.value, __required.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, u'http://www.w3.org/ns/wsdl'))

    _ElementMap = pyxb.bundles.wssplat.wsdl20.ExtensibleDocumentedType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = pyxb.bundles.wssplat.wsdl20.ExtensibleDocumentedType._AttributeMap.copy()
    _AttributeMap.update({
        __ref.name() : __ref,
        __required.name() : __required
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.bundles.wssplat.wsdl20.ExtensibleDocumentedType):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 44, 2)
    # Base type is pyxb.bundles.wssplat.wsdl20.ExtensibleDocumentedType
    
    # Element documentation ({http://www.w3.org/ns/wsdl}documentation) inherited from {http://www.w3.org/ns/wsdl}DocumentedType
    
    # Attribute element uses Python identifier element
    __element = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'element'), 'element', '__httpwww_w3_orgnswsdlsoap_CTD_ANON__element', pyxb.binding.datatypes.QName, required=True)
    __element._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 47, 5)
    __element._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 47, 5)
    
    element = property(__element.value, __element.set, None, None)

    
    # Attribute mustUnderstand uses Python identifier mustUnderstand
    __mustUnderstand = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mustUnderstand'), 'mustUnderstand', '__httpwww_w3_orgnswsdlsoap_CTD_ANON__mustUnderstand', pyxb.binding.datatypes.boolean)
    __mustUnderstand._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 48, 5)
    __mustUnderstand._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 48, 5)
    
    mustUnderstand = property(__mustUnderstand.value, __mustUnderstand.set, None, None)

    
    # Attribute required uses Python identifier required
    __required = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'required'), 'required', '__httpwww_w3_orgnswsdlsoap_CTD_ANON__required', pyxb.binding.datatypes.boolean)
    __required._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 49, 5)
    __required._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 49, 5)
    
    required = property(__required.value, __required.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, u'http://www.w3.org/ns/wsdl'))

    _ElementMap = pyxb.bundles.wssplat.wsdl20.ExtensibleDocumentedType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = pyxb.bundles.wssplat.wsdl20.ExtensibleDocumentedType._AttributeMap.copy()
    _AttributeMap.update({
        __element.name() : __element,
        __mustUnderstand.name() : __mustUnderstand,
        __required.name() : __required
    })



module = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'module'), CTD_ANON, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 32, 1))
Namespace.addCategoryObject('elementBinding', module.name().localName(), module)

header = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'header'), CTD_ANON_, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsoap.xsd', 43, 1))
Namespace.addCategoryObject('elementBinding', header.name().localName(), header)



def _BuildAutomaton ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsdl20.xsd', 37, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/ns/wsdl'), u'documentation')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsdl20.xsd', 37, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsdl20.xsd', 37, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/ns/wsdl'), u'documentation')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsdl20.xsd', 37, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()

