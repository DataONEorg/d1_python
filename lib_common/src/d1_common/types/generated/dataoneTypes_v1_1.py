# ./d1_common/types/generated/dataoneTypes_v1_1.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:360f646bcacd4796da7a71be6ffd7cac7a35ff8a
# Generated 2017-10-17 10:39:46.546406 by PyXB version 1.2.6 using Python 2.7.12.final.0
# Namespace http://ns.dataone.org/service/types/v1.1


import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:c90f2764-b359-11e7-b444-080027018ba0')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
from . import dataoneTypes_v1 as _ImportedBinding_dataoneTypes_v1

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://ns.dataone.org/service/types/v1.1', create_if_missing=True)
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
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
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


# Complex type {http://ns.dataone.org/service/types/v1.1}QueryEngineDescription with content type ELEMENT_ONLY
class QueryEngineDescription (pyxb.binding.basis.complexTypeDefinition):
    """Describes a query engine that can be used to search content on the node. 
      Query engines may be general purpose or specialized for particular communities or domains."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'QueryEngineDescription')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 72, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element queryEngineVersion uses Python identifier queryEngineVersion
    __queryEngineVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'queryEngineVersion'), 'queryEngineVersion', '__httpns_dataone_orgservicetypesv1_1_QueryEngineDescription_queryEngineVersion', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 78, 6), )

    
    queryEngineVersion = property(__queryEngineVersion.value, __queryEngineVersion.set, None, 'The version of the underlying query engine. Used by clients to determine possible\n          compatibility concerns or features available.')

    
    # Element querySchemaVersion uses Python identifier querySchemaVersion
    __querySchemaVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'querySchemaVersion'), 'querySchemaVersion', '__httpns_dataone_orgservicetypesv1_1_QueryEngineDescription_querySchemaVersion', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 84, 6), )

    
    querySchemaVersion = property(__querySchemaVersion.value, __querySchemaVersion.set, None, 'Version of the schema in use by the query engine, e.g. "1.0.1"')

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpns_dataone_orgservicetypesv1_1_QueryEngineDescription_name', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 89, 6), )

    
    name = property(__name.value, __name.set, None, 'The full, human readable name of the query engine. For example: \n            "Apache SOLR"')

    
    # Element additionalInfo uses Python identifier additionalInfo
    __additionalInfo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'additionalInfo'), 'additionalInfo', '__httpns_dataone_orgservicetypesv1_1_QueryEngineDescription_additionalInfo', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 95, 6), )

    
    additionalInfo = property(__additionalInfo.value, __additionalInfo.set, None, 'An optional human readable description of the query engine. This can be \n            used to describe any special capabilities or intended uses for the query engine. For example, \n            a query engine may be tuned to suit a particular audience or domain as opposed to providing \n            a general purpose discovery mechanism.This field may also contain links to additional information about the query engine, \n          such as documentation for the search syntax provided by the query engine implemntors.')

    
    # Element queryField uses Python identifier queryField
    __queryField = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'queryField'), 'queryField', '__httpns_dataone_orgservicetypesv1_1_QueryEngineDescription_queryField', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 105, 6), )

    
    queryField = property(__queryField.value, __queryField.set, None, 'A list of query fields supported by the query engine.')

    _ElementMap.update({
        __queryEngineVersion.name() : __queryEngineVersion,
        __querySchemaVersion.name() : __querySchemaVersion,
        __name.name() : __name,
        __additionalInfo.name() : __additionalInfo,
        __queryField.name() : __queryField
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.QueryEngineDescription = QueryEngineDescription
Namespace.addCategoryObject('typeBinding', 'QueryEngineDescription', QueryEngineDescription)


# Complex type {http://ns.dataone.org/service/types/v1.1}QueryEngineList with content type ELEMENT_ONLY
class QueryEngineList (pyxb.binding.basis.complexTypeDefinition):
    """A list of query engine names that indicate the possible values for 
        CNRead.getQueryEngineDescription and CNRead.query REST API endpoints."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'QueryEngineList')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 114, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element queryEngine uses Python identifier queryEngine
    __queryEngine = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'queryEngine'), 'queryEngine', '__httpns_dataone_orgservicetypesv1_1_QueryEngineList_queryEngine', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 120, 6), )

    
    queryEngine = property(__queryEngine.value, __queryEngine.set, None, 'The name of a queryEngine. This value will be used as a path element in \n            REST API calls and so should not contain characters that will need to be escaped.')

    _ElementMap.update({
        __queryEngine.name() : __queryEngine
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.QueryEngineList = QueryEngineList
Namespace.addCategoryObject('typeBinding', 'QueryEngineList', QueryEngineList)


# Complex type {http://ns.dataone.org/service/types/v1.1}QueryField with content type ELEMENT_ONLY
class QueryField (pyxb.binding.basis.complexTypeDefinition):
    """"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'QueryField')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 131, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpns_dataone_orgservicetypesv1_1_QueryField_name', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 136, 6), )

    
    name = property(__name.value, __name.set, None, 'The name of the field as used programmatically when \n            constructing queries or other rferences to the field.')

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'description'), 'description', '__httpns_dataone_orgservicetypesv1_1_QueryField_description', True, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 142, 6), )

    
    description = property(__description.value, __description.set, None, 'An optional, repeatable, brief description of the field that can be\n          used to help guide developers or end users in appropriate use of the field. May for \n          example, contain a links to additional documentation.')

    
    # Element type uses Python identifier type
    __type = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpns_dataone_orgservicetypesv1_1_QueryField_type', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 149, 6), )

    
    type = property(__type.value, __type.set, None, 'The type of the field, expressed in the language peculiar to the \n          query engine being described.')

    
    # Element searchable uses Python identifier searchable
    __searchable = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'searchable'), 'searchable', '__httpns_dataone_orgservicetypesv1_1_QueryField_searchable', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 155, 6), )

    
    searchable = property(__searchable.value, __searchable.set, None, 'Indicates if the field may be used in constructing queries (as opposed \n            to only appearing in results)')

    
    # Element returnable uses Python identifier returnable
    __returnable = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'returnable'), 'returnable', '__httpns_dataone_orgservicetypesv1_1_QueryField_returnable', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 161, 6), )

    
    returnable = property(__returnable.value, __returnable.set, None, 'Indicates if the field values may be returned in search results.')

    
    # Element sortable uses Python identifier sortable
    __sortable = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'sortable'), 'sortable', '__httpns_dataone_orgservicetypesv1_1_QueryField_sortable', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 166, 6), )

    
    sortable = property(__sortable.value, __sortable.set, None, 'Indicates if the field can be used for sorting results.')

    
    # Element multivalued uses Python identifier multivalued
    __multivalued = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'multivalued'), 'multivalued', '__httpns_dataone_orgservicetypesv1_1_QueryField_multivalued', False, pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 171, 6), )

    
    multivalued = property(__multivalued.value, __multivalued.set, None, 'Indicates if the field may contain multiple values. Some query engines\n          such as SOLR support this capability.')

    _ElementMap.update({
        __name.name() : __name,
        __description.name() : __description,
        __type.name() : __type,
        __searchable.name() : __searchable,
        __returnable.name() : __returnable,
        __sortable.name() : __sortable,
        __multivalued.name() : __multivalued
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.QueryField = QueryField
Namespace.addCategoryObject('typeBinding', 'QueryField', QueryField)


queryEngineList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'queryEngineList'), QueryEngineList, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 194, 2))
Namespace.addCategoryObject('elementBinding', queryEngineList.name().localName(), queryEngineList)

queryEngineDescription = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'queryEngineDescription'), QueryEngineDescription, location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 195, 2))
Namespace.addCategoryObject('elementBinding', queryEngineDescription.name().localName(), queryEngineDescription)



QueryEngineDescription._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'queryEngineVersion'), pyxb.binding.datatypes.string, scope=QueryEngineDescription, documentation='The version of the underlying query engine. Used by clients to determine possible\n          compatibility concerns or features available.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 78, 6)))

QueryEngineDescription._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'querySchemaVersion'), pyxb.binding.datatypes.string, scope=QueryEngineDescription, documentation='Version of the schema in use by the query engine, e.g. "1.0.1"', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 84, 6)))

QueryEngineDescription._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'name'), pyxb.binding.datatypes.string, scope=QueryEngineDescription, documentation='The full, human readable name of the query engine. For example: \n            "Apache SOLR"', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 89, 6)))

QueryEngineDescription._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'additionalInfo'), _ImportedBinding_dataoneTypes_v1.NonEmptyString, scope=QueryEngineDescription, documentation='An optional human readable description of the query engine. This can be \n            used to describe any special capabilities or intended uses for the query engine. For example, \n            a query engine may be tuned to suit a particular audience or domain as opposed to providing \n            a general purpose discovery mechanism.This field may also contain links to additional information about the query engine, \n          such as documentation for the search syntax provided by the query engine implemntors.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 95, 6)))

QueryEngineDescription._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'queryField'), QueryField, scope=QueryEngineDescription, documentation='A list of query fields supported by the query engine.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 105, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 84, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 95, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 105, 6))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(QueryEngineDescription._UseForTag(pyxb.namespace.ExpandedName(None, 'queryEngineVersion')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 78, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(QueryEngineDescription._UseForTag(pyxb.namespace.ExpandedName(None, 'querySchemaVersion')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 84, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(QueryEngineDescription._UseForTag(pyxb.namespace.ExpandedName(None, 'name')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 89, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(QueryEngineDescription._UseForTag(pyxb.namespace.ExpandedName(None, 'additionalInfo')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 95, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(QueryEngineDescription._UseForTag(pyxb.namespace.ExpandedName(None, 'queryField')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 105, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
QueryEngineDescription._Automaton = _BuildAutomaton()




QueryEngineList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'queryEngine'), _ImportedBinding_dataoneTypes_v1.NonEmptyString, scope=QueryEngineList, documentation='The name of a queryEngine. This value will be used as a path element in \n            REST API calls and so should not contain characters that will need to be escaped.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 120, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 120, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(QueryEngineList._UseForTag(pyxb.namespace.ExpandedName(None, 'queryEngine')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 120, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
QueryEngineList._Automaton = _BuildAutomaton_()




QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'name'), _ImportedBinding_dataoneTypes_v1.NonEmptyString, scope=QueryField, documentation='The name of the field as used programmatically when \n            constructing queries or other rferences to the field.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 136, 6)))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'description'), pyxb.binding.datatypes.string, scope=QueryField, documentation='An optional, repeatable, brief description of the field that can be\n          used to help guide developers or end users in appropriate use of the field. May for \n          example, contain a links to additional documentation.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 142, 6)))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'type'), _ImportedBinding_dataoneTypes_v1.NonEmptyString, scope=QueryField, documentation='The type of the field, expressed in the language peculiar to the \n          query engine being described.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 149, 6)))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'searchable'), pyxb.binding.datatypes.boolean, scope=QueryField, documentation='Indicates if the field may be used in constructing queries (as opposed \n            to only appearing in results)', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 155, 6)))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'returnable'), pyxb.binding.datatypes.boolean, scope=QueryField, documentation='Indicates if the field values may be returned in search results.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 161, 6)))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'sortable'), pyxb.binding.datatypes.boolean, scope=QueryField, documentation='Indicates if the field can be used for sorting results.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 166, 6)))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'multivalued'), pyxb.binding.datatypes.boolean, scope=QueryField, documentation='Indicates if the field may contain multiple values. Some query engines\n          such as SOLR support this capability.', location=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 171, 6)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 142, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 171, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, 'name')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 136, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, 'description')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 142, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, 'type')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 149, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, 'searchable')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 155, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, 'returnable')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 161, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, 'sortable')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 166, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, 'multivalued')), pyxb.utils.utility.Location('/home/dahl/dev/d1_python/lib_common/src/d1_common/types/schemas/dataoneTypes_v1.1.xsd', 171, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
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
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
QueryField._Automaton = _BuildAutomaton_2()

