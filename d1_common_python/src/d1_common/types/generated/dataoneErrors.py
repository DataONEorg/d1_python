# ./d1_common/types/generated/dataoneErrors.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2012-12-19 22:02:21.708418 by PyXB version 1.2.1
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:6fc2617c-4a62-11e2-a023-000c294230b4')

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
    """Defines a structure for serializing DataONE
        Exceptions."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 49, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__AbsentNamespace0_CTD_ANON_description', False, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 51, 8), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element traceInformation uses Python identifier traceInformation
    __traceInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'traceInformation'), 'traceInformation', '__AbsentNamespace0_CTD_ANON_traceInformation', False, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 53, 8), )

    
    traceInformation = property(__traceInformation.value, __traceInformation.set, None, None)

    
    # Attribute detailCode uses Python identifier detailCode
    __detailCode = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'detailCode'), 'detailCode', '__AbsentNamespace0_CTD_ANON_detailCode', pyxb.binding.datatypes.int, required=True)
    __detailCode._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 56, 6)
    __detailCode._UseLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 56, 6)
    
    detailCode = property(__detailCode.value, __detailCode.set, None, None)

    
    # Attribute errorCode uses Python identifier errorCode
    __errorCode = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'errorCode'), 'errorCode', '__AbsentNamespace0_CTD_ANON_errorCode', pyxb.binding.datatypes.int, required=True)
    __errorCode._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 57, 6)
    __errorCode._UseLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 57, 6)
    
    errorCode = property(__errorCode.value, __errorCode.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__AbsentNamespace0_CTD_ANON_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 58, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 58, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute pid uses Python identifier pid
    __pid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'pid'), 'pid', '__AbsentNamespace0_CTD_ANON_pid', pyxb.binding.datatypes.string)
    __pid._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 59, 6)
    __pid._UseLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 59, 6)
    
    pid = property(__pid.value, __pid.set, None, None)


    _ElementMap = {
        __description.name() : __description,
        __traceInformation.name() : __traceInformation
    }
    _AttributeMap = {
        __detailCode.name() : __detailCode,
        __errorCode.name() : __errorCode,
        __name.name() : __name,
        __pid.name() : __pid
    }



error = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'error'), CTD_ANON, documentation=u'Defines a structure for serializing DataONE\n        Exceptions.', location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 44, 2))
Namespace.addCategoryObject('elementBinding', error.name().localName(), error)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'description'), pyxb.binding.datatypes.string, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 51, 8)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'traceInformation'), pyxb.binding.datatypes.string, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 53, 8)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1L, metadata=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 53, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'description')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 51, 8))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'traceInformation')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 53, 8))
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
CTD_ANON._Automaton = _BuildAutomaton()

