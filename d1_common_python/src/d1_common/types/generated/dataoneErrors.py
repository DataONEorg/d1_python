# ./d1_common/types/generated/dataoneErrors.py
# PyXB bindings for NamespaceModule
# NSM:e1c8105703d7da231af0d9fa96019858275c42c4
# Generated 2011-09-11 08:22:05.396480 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:6cad4362-dc81-11e0-9619-000c294230b4')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'http://ns.dataone.org/service/types/exceptions', create_if_missing=True)
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


# Complex type ErrorBase with content type ELEMENT_ONLY
class ErrorBase (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ErrorBase')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element traceInformation uses Python identifier traceInformation
    __traceInformation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'traceInformation'), 'traceInformation', '__httpns_dataone_orgservicetypesexceptions_ErrorBase_traceInformation', False)

    
    traceInformation = property(__traceInformation.value, __traceInformation.set, None, None)

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__httpns_dataone_orgservicetypesexceptions_ErrorBase_description', False)

    
    description = property(__description.value, __description.set, None, None)

    
    # Attribute errorCode uses Python identifier errorCode
    __errorCode = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'errorCode'), 'errorCode', '__httpns_dataone_orgservicetypesexceptions_ErrorBase_errorCode', pyxb.binding.datatypes.int, required=True)
    
    errorCode = property(__errorCode.value, __errorCode.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesexceptions_ErrorBase_name', pyxb.binding.datatypes.string, required=True)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __traceInformation.name() : __traceInformation,
        __description.name() : __description
    }
    _AttributeMap = {
        __errorCode.name() : __errorCode,
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'ErrorBase', ErrorBase)


# Complex type ErrorPID with content type ELEMENT_ONLY
class ErrorPID (ErrorBase):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ErrorPID')
    # Base type is ErrorBase
    
    # Element traceInformation (traceInformation) inherited from {http://ns.dataone.org/service/types/exceptions}ErrorBase
    
    # Element description (description) inherited from {http://ns.dataone.org/service/types/exceptions}ErrorBase
    
    # Attribute errorCode inherited from {http://ns.dataone.org/service/types/exceptions}ErrorBase
    
    # Attribute PID uses Python identifier PID
    __PID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'PID'), 'PID', '__httpns_dataone_orgservicetypesexceptions_ErrorPID_PID', pyxb.binding.datatypes.int, required=True)
    
    PID = property(__PID.value, __PID.set, None, None)

    
    # Attribute name inherited from {http://ns.dataone.org/service/types/exceptions}ErrorBase

    _ElementMap = ErrorBase._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ErrorBase._AttributeMap.copy()
    _AttributeMap.update({
        __PID.name() : __PID
    })
Namespace.addCategoryObject('typeBinding', u'ErrorPID', ErrorPID)


ServiceFailure = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ServiceFailure'), ErrorBase)
Namespace.addCategoryObject('elementBinding', ServiceFailure.name().localName(), ServiceFailure)

UnsupportedMetadataType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'UnsupportedMetadataType'), ErrorBase)
Namespace.addCategoryObject('elementBinding', UnsupportedMetadataType.name().localName(), UnsupportedMetadataType)

UnsupportedType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'UnsupportedType'), ErrorBase)
Namespace.addCategoryObject('elementBinding', UnsupportedType.name().localName(), UnsupportedType)

NotFound = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NotFound'), ErrorPID)
Namespace.addCategoryObject('elementBinding', NotFound.name().localName(), NotFound)

NotImplemented = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NotImplemented'), ErrorBase)
Namespace.addCategoryObject('elementBinding', NotImplemented.name().localName(), NotImplemented)

AuthenticationTimeout = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthenticationTimeout'), ErrorBase)
Namespace.addCategoryObject('elementBinding', AuthenticationTimeout.name().localName(), AuthenticationTimeout)

InsufficientResources = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InsufficientResources'), ErrorBase)
Namespace.addCategoryObject('elementBinding', InsufficientResources.name().localName(), InsufficientResources)

IdentifierNotUnique = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IdentifierNotUnique'), ErrorPID)
Namespace.addCategoryObject('elementBinding', IdentifierNotUnique.name().localName(), IdentifierNotUnique)

InvalidCredentials = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InvalidCredentials'), ErrorBase)
Namespace.addCategoryObject('elementBinding', InvalidCredentials.name().localName(), InvalidCredentials)

InvalidRequest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InvalidRequest'), ErrorBase)
Namespace.addCategoryObject('elementBinding', InvalidRequest.name().localName(), InvalidRequest)

InvalidSystemMetadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InvalidSystemMetadata'), ErrorBase)
Namespace.addCategoryObject('elementBinding', InvalidSystemMetadata.name().localName(), InvalidSystemMetadata)

InvalidToken = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InvalidToken'), ErrorBase)
Namespace.addCategoryObject('elementBinding', InvalidToken.name().localName(), InvalidToken)

NotAuthorized = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NotAuthorized'), ErrorBase)
Namespace.addCategoryObject('elementBinding', NotAuthorized.name().localName(), NotAuthorized)



ErrorBase._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'traceInformation'), pyxb.binding.datatypes.string, scope=ErrorBase))

ErrorBase._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'description'), pyxb.binding.datatypes.string, scope=ErrorBase))
ErrorBase._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ErrorBase._UseForTag(pyxb.namespace.ExpandedName(None, u'description')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ErrorBase._UseForTag(pyxb.namespace.ExpandedName(None, u'traceInformation')), min_occurs=0L, max_occurs=1L)
    )
ErrorBase._ContentModel = pyxb.binding.content.ParticleModel(ErrorBase._GroupModel, min_occurs=1, max_occurs=1)


ErrorPID._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ErrorPID._UseForTag(pyxb.namespace.ExpandedName(None, u'description')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ErrorPID._UseForTag(pyxb.namespace.ExpandedName(None, u'traceInformation')), min_occurs=0L, max_occurs=1L)
    )
ErrorPID._ContentModel = pyxb.binding.content.ParticleModel(ErrorPID._GroupModel, min_occurs=1, max_occurs=1)
