# ./pyxb/bundles/wssplat/raw/wsrf_bf.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:1f695b8b0461ea6da4ae596208b164781fcb562b
# Generated 2012-12-17 13:09:30.532954 by PyXB version 1.2.1
# Namespace http://docs.oasis-open.org/wsrf/bf-2

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:48ddaca6-487d-11e2-a769-c8600024e903')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.wssplat.wsa
import pyxb.binding.xml_

Namespace = pyxb.namespace.NamespaceForURI(u'http://docs.oasis-open.org/wsrf/bf-2', create_if_missing=True)
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


# Complex type {http://docs.oasis-open.org/wsrf/bf-2}BaseFaultType with content type ELEMENT_ONLY
class BaseFaultType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://docs.oasis-open.org/wsrf/bf-2}BaseFaultType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BaseFaultType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 44, 2)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://docs.oasis-open.org/wsrf/bf-2}Timestamp uses Python identifier Timestamp
    __Timestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Timestamp'), 'Timestamp', '__httpdocs_oasis_open_orgwsrfbf_2_BaseFaultType_httpdocs_oasis_open_orgwsrfbf_2Timestamp', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 48, 6), )

    
    Timestamp = property(__Timestamp.value, __Timestamp.set, None, None)

    
    # Element {http://docs.oasis-open.org/wsrf/bf-2}Originator uses Python identifier Originator
    __Originator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Originator'), 'Originator', '__httpdocs_oasis_open_orgwsrfbf_2_BaseFaultType_httpdocs_oasis_open_orgwsrfbf_2Originator', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 50, 6), )

    
    Originator = property(__Originator.value, __Originator.set, None, None)

    
    # Element {http://docs.oasis-open.org/wsrf/bf-2}ErrorCode uses Python identifier ErrorCode
    __ErrorCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'ErrorCode'), 'ErrorCode', '__httpdocs_oasis_open_orgwsrfbf_2_BaseFaultType_httpdocs_oasis_open_orgwsrfbf_2ErrorCode', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 52, 6), )

    
    ErrorCode = property(__ErrorCode.value, __ErrorCode.set, None, None)

    
    # Element {http://docs.oasis-open.org/wsrf/bf-2}Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Description'), 'Description', '__httpdocs_oasis_open_orgwsrfbf_2_BaseFaultType_httpdocs_oasis_open_orgwsrfbf_2Description', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 64, 6), )

    
    Description = property(__Description.value, __Description.set, None, None)

    
    # Element {http://docs.oasis-open.org/wsrf/bf-2}FaultCause uses Python identifier FaultCause
    __FaultCause = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'FaultCause'), 'FaultCause', '__httpdocs_oasis_open_orgwsrfbf_2_BaseFaultType_httpdocs_oasis_open_orgwsrfbf_2FaultCause', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 74, 6), )

    
    FaultCause = property(__FaultCause.value, __FaultCause.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, u'http://docs.oasis-open.org/wsrf/bf-2'))
    _HasWildcardElement = True

    _ElementMap = {
        __Timestamp.name() : __Timestamp,
        __Originator.name() : __Originator,
        __ErrorCode.name() : __ErrorCode,
        __Description.name() : __Description,
        __FaultCause.name() : __FaultCause
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'BaseFaultType', BaseFaultType)


# Complex type [anonymous] with content type MIXED
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 54, 8)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute dialect uses Python identifier dialect
    __dialect = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dialect'), 'dialect', '__httpdocs_oasis_open_orgwsrfbf_2_CTD_ANON_dialect', pyxb.binding.datatypes.anyURI, required=True)
    __dialect._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 57, 14)
    __dialect._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 57, 14)
    
    dialect = property(__dialect.value, __dialect.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _HasWildcardElement = True

    _ElementMap = {
        
    }
    _AttributeMap = {
        __dialect.name() : __dialect
    }



# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 66, 8)
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute {http://www.w3.org/XML/1998/namespace}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.XML, 'lang'), 'lang', '__httpdocs_oasis_open_orgwsrfbf_2_CTD_ANON__httpwww_w3_orgXML1998namespacelang', pyxb.binding.xml_.STD_ANON_lang)
    __lang._DeclarationLocation = None
    __lang._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 69, 14)
    
    lang = property(__lang.value, __lang.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __lang.name() : __lang
    }



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 75, 8)
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }



BaseFault = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BaseFault'), BaseFaultType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 42, 2))
Namespace.addCategoryObject('elementBinding', BaseFault.name().localName(), BaseFault)



BaseFaultType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Timestamp'), pyxb.binding.datatypes.dateTime, scope=BaseFaultType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 48, 6)))

BaseFaultType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Originator'), pyxb.bundles.wssplat.wsa.EndpointReferenceType, scope=BaseFaultType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 50, 6)))

BaseFaultType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ErrorCode'), CTD_ANON, scope=BaseFaultType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 52, 6)))

BaseFaultType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Description'), CTD_ANON_, scope=BaseFaultType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 64, 6)))

BaseFaultType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FaultCause'), CTD_ANON_2, scope=BaseFaultType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 74, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 46, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1L, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 50, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1L, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 52, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 64, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0L, max=1L, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 74, 6))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, u'http://docs.oasis-open.org/wsrf/bf-2')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 46, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BaseFaultType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Timestamp')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 48, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(BaseFaultType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Originator')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 50, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(BaseFaultType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ErrorCode')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 52, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(BaseFaultType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Description')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 64, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(BaseFaultType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FaultCause')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 74, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BaseFaultType._Automaton = _BuildAutomaton()




def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1L, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 54, 8))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1L, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 54, 8))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_()




def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, u'http://docs.oasis-open.org/wsrf/bf-2')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/wsrf_bf.xsd', 77, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_2()

