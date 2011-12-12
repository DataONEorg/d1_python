# ./d1_common/types/generated/dataoneErrors.py
# PyXB bindings for NamespaceModule
# NSM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2011-12-12 09:24:02.431768 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:b3fb4fda-24dd-11e1-9e12-000c294230b4')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.CreateAbsentNamespace()
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


# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element traceInformation uses Python identifier traceInformation
    __traceInformation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'traceInformation'), 'traceInformation', '__AbsentNamespace0_CTD_ANON_traceInformation', False)

    
    traceInformation = property(__traceInformation.value, __traceInformation.set, None, None)

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__AbsentNamespace0_CTD_ANON_description', False)

    
    description = property(__description.value, __description.set, None, None)

    
    # Attribute errorCode uses Python identifier errorCode
    __errorCode = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'errorCode'), 'errorCode', '__AbsentNamespace0_CTD_ANON_errorCode', pyxb.binding.datatypes.int, required=True)
    
    errorCode = property(__errorCode.value, __errorCode.set, None, None)

    
    # Attribute detailCode uses Python identifier detailCode
    __detailCode = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'detailCode'), 'detailCode', '__AbsentNamespace0_CTD_ANON_detailCode', pyxb.binding.datatypes.int, required=True)
    
    detailCode = property(__detailCode.value, __detailCode.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__AbsentNamespace0_CTD_ANON_name', pyxb.binding.datatypes.string, required=True)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute pid uses Python identifier pid
    __pid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'pid'), 'pid', '__AbsentNamespace0_CTD_ANON_pid', pyxb.binding.datatypes.string)
    
    pid = property(__pid.value, __pid.set, None, None)


    _ElementMap = {
        __traceInformation.name() : __traceInformation,
        __description.name() : __description
    }
    _AttributeMap = {
        __errorCode.name() : __errorCode,
        __detailCode.name() : __detailCode,
        __name.name() : __name,
        __pid.name() : __pid
    }



error = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'error'), CTD_ANON)
Namespace.addCategoryObject('elementBinding', error.name().localName(), error)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'traceInformation'), pyxb.binding.datatypes.string, scope=CTD_ANON))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'description'), pyxb.binding.datatypes.string, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'description')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'traceInformation')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)
