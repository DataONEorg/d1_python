# ./generated/workspace_types.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2013-05-17 09:55:28.582636 by PyXB version 1.2.1
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:32134568-bf0a-11e2-8a24-000c294230b4')

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


# Complex type Folder with content type ELEMENT_ONLY
class Folder (pyxb.binding.basis.complexTypeDefinition):
    """Complex type Folder with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Folder')
    _XSDLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 7, 2)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element folder uses Python identifier folder
    __folder = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'folder'), 'folder', '__AbsentNamespace0_Folder_folder', True, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 9, 6), )

    
    folder = property(__folder.value, __folder.set, None, None)

    
    # Element identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__AbsentNamespace0_Folder_identifier', True, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 10, 6), )

    
    identifier = property(__identifier.value, __identifier.set, None, None)

    
    # Element query uses Python identifier query
    __query = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'query'), 'query', '__AbsentNamespace0_Folder_query', True, pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 11, 6), )

    
    query = property(__query.value, __query.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__AbsentNamespace0_Folder_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 13, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 13, 4)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __folder.name() : __folder,
        __identifier.name() : __identifier,
        __query.name() : __query
    }
    _AttributeMap = {
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'Folder', Folder)


folder = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'folder'), Folder, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 5, 2))
Namespace.addCategoryObject('elementBinding', folder.name().localName(), folder)



Folder._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'folder'), Folder, scope=Folder, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 9, 6)))

Folder._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'identifier'), pyxb.binding.datatypes.string, scope=Folder, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 10, 6)))

Folder._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'query'), pyxb.binding.datatypes.string, scope=Folder, location=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 11, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 9, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 10, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 11, 6))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Folder._UseForTag(pyxb.namespace.ExpandedName(None, u'folder')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 9, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Folder._UseForTag(pyxb.namespace.ExpandedName(None, u'identifier')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 10, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(Folder._UseForTag(pyxb.namespace.ExpandedName(None, u'query')), pyxb.utils.utility.Location('/home/dahl/d1/d1_python/d1_workspace_client/src/d1_workspace/types/workspace_types.xsd', 11, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Folder._Automaton = _BuildAutomaton()

