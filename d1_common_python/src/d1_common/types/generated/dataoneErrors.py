# ./d1_common/types/generated/dataoneErrors.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2014-08-01 17:18:09.766318 by PyXB version 1.2.3
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:19f68be2-19d2-11e4-ad23-000c292ff10e')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.3'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
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
    xmld = xml_text
    if isinstance(xmld, unicode):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: NonEmptyString
class NonEmptyString (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonEmptyString')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 45, 2)
    _Documentation = None
NonEmptyString._CF_pattern = pyxb.binding.facets.CF_pattern()
NonEmptyString._CF_pattern.addPattern(pattern=u'[\\s]*[\\S][\\s\\S]*')
NonEmptyString._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1L))
NonEmptyString._InitializeFacetMap(NonEmptyString._CF_pattern,
   NonEmptyString._CF_minLength)
Namespace.addCategoryObject('typeBinding', u'NonEmptyString', NonEmptyString)

# Complex type DataONEException with content type ELEMENT_ONLY
class DataONEException (pyxb.binding.basis.complexTypeDefinition):
    """Defines a structure for serializing DataONE
        Exceptions."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataONEException')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 53, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__AbsentNamespace0_DataONEException_description', False, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 59, 6), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element traceInformation uses Python identifier traceInformation
    __traceInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'traceInformation'), 'traceInformation', '__AbsentNamespace0_DataONEException_traceInformation', False, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 60, 6), )

    
    traceInformation = property(__traceInformation.value, __traceInformation.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__AbsentNamespace0_DataONEException_name', NonEmptyString, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 62, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 62, 4)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute errorCode uses Python identifier errorCode
    __errorCode = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'errorCode'), 'errorCode', '__AbsentNamespace0_DataONEException_errorCode', pyxb.binding.datatypes.integer, required=True)
    __errorCode._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 63, 4)
    __errorCode._UseLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 63, 4)
    
    errorCode = property(__errorCode.value, __errorCode.set, None, None)

    
    # Attribute detailCode uses Python identifier detailCode
    __detailCode = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'detailCode'), 'detailCode', '__AbsentNamespace0_DataONEException_detailCode', NonEmptyString, required=True)
    __detailCode._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 64, 4)
    __detailCode._UseLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 64, 4)
    
    detailCode = property(__detailCode.value, __detailCode.set, None, None)

    
    # Attribute identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__AbsentNamespace0_DataONEException_identifier', NonEmptyString)
    __identifier._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 65, 4)
    __identifier._UseLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 65, 4)
    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Attribute nodeId uses Python identifier nodeId
    __nodeId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'nodeId'), 'nodeId', '__AbsentNamespace0_DataONEException_nodeId', NonEmptyString)
    __nodeId._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 66, 4)
    __nodeId._UseLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 66, 4)
    
    nodeId = property(__nodeId.value, __nodeId.set, None, None)

    _ElementMap.update({
        __description.name() : __description,
        __traceInformation.name() : __traceInformation
    })
    _AttributeMap.update({
        __name.name() : __name,
        __errorCode.name() : __errorCode,
        __detailCode.name() : __detailCode,
        __identifier.name() : __identifier,
        __nodeId.name() : __nodeId
    })
Namespace.addCategoryObject('typeBinding', u'DataONEException', DataONEException)


error = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'error'), DataONEException, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 69, 2))
Namespace.addCategoryObject('elementBinding', error.name().localName(), error)



DataONEException._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'description'), pyxb.binding.datatypes.string, scope=DataONEException, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 59, 6)))

DataONEException._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'traceInformation'), pyxb.binding.datatypes.anyType, scope=DataONEException, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 60, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1L, metadata=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 59, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1L, metadata=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 60, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DataONEException._UseForTag(pyxb.namespace.ExpandedName(None, u'description')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 59, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(DataONEException._UseForTag(pyxb.namespace.ExpandedName(None, u'traceInformation')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_common_python/src/d1_schemas/dataoneErrors.xsd', 60, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
DataONEException._Automaton = _BuildAutomaton()

