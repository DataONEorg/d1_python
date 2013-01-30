# ./generated/gmn_types.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2013-01-09 09:12:32.879210 by PyXB version 1.2.1
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:5fbf508a-5a77-11e2-b865-000c294230b4')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.CreateAbsentNamespace()
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


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 8, 8)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element taskId uses Python identifier taskId
    __taskId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'taskId'), 'taskId', '__AbsentNamespace0_CTD_ANON_taskId', False, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 10, 16), )

    
    taskId = property(__taskId.value, __taskId.set, None, None)

    
    # Element status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'status'), 'status', '__AbsentNamespace0_CTD_ANON_status', False, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 11, 16), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element pid uses Python identifier pid
    __pid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'pid'), 'pid', '__AbsentNamespace0_CTD_ANON_pid', False, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 12, 16), )

    
    pid = property(__pid.value, __pid.set, None, None)

    
    # Element sourceNode uses Python identifier sourceNode
    __sourceNode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'sourceNode'), 'sourceNode', '__AbsentNamespace0_CTD_ANON_sourceNode', False, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 13, 16), )

    
    sourceNode = property(__sourceNode.value, __sourceNode.set, None, None)

    
    # Element timestamp uses Python identifier timestamp
    __timestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'timestamp'), 'timestamp', '__AbsentNamespace0_CTD_ANON_timestamp', False, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 14, 16), )

    
    timestamp = property(__timestamp.value, __timestamp.set, None, None)


    _ElementMap = {
        __taskId.name() : __taskId,
        __status.name() : __status,
        __pid.name() : __pid,
        __sourceNode.name() : __sourceNode,
        __timestamp.name() : __timestamp
    }
    _AttributeMap = {
        
    }



replicationRequest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'replicationRequest'), CTD_ANON, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 7, 4))
Namespace.addCategoryObject('elementBinding', replicationRequest.name().localName(), replicationRequest)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'taskId'), pyxb.binding.datatypes.unsignedLong, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 10, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'status'), pyxb.binding.datatypes.string, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 11, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'pid'), pyxb.binding.datatypes.string, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 12, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'sourceNode'), pyxb.binding.datatypes.string, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 13, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'timestamp'), pyxb.binding.datatypes.dateTime, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 14, 16)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'taskId')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 10, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'status')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 11, 16))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'pid')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 12, 16))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'sourceNode')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 13, 16))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'timestamp')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_mn_generic/src/service/types/gmn_types.xsd', 14, 16))
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
CTD_ANON._Automaton = _BuildAutomaton()

