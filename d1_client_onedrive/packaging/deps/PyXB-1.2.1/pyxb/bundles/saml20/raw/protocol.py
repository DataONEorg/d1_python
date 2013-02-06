# ./pyxb/bundles/saml20/raw/protocol.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:36a732e723673f7ad63838d43d722888bbbdeb09
# Generated 2012-12-17 13:09:32.257614 by PyXB version 1.2.1
# Namespace urn:oasis:names:tc:SAML:2.0:protocol

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:49d89c10-487d-11e2-8c99-c8600024e903')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.wssplat.ds
import pyxb.bundles.saml20.assertion

Namespace = pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:protocol', create_if_missing=True)
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


# Atomic simple type: {urn:oasis:names:tc:SAML:2.0:protocol}AuthnContextComparisonType
class AuthnContextComparisonType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AuthnContextComparisonType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 122, 4)
    _Documentation = None
AuthnContextComparisonType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=AuthnContextComparisonType, enum_prefix=None)
AuthnContextComparisonType.exact = AuthnContextComparisonType._CF_enumeration.addEnumeration(unicode_value=u'exact', tag=u'exact')
AuthnContextComparisonType.minimum = AuthnContextComparisonType._CF_enumeration.addEnumeration(unicode_value=u'minimum', tag=u'minimum')
AuthnContextComparisonType.maximum = AuthnContextComparisonType._CF_enumeration.addEnumeration(unicode_value=u'maximum', tag=u'maximum')
AuthnContextComparisonType.better = AuthnContextComparisonType._CF_enumeration.addEnumeration(unicode_value=u'better', tag=u'better')
AuthnContextComparisonType._InitializeFacetMap(AuthnContextComparisonType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'AuthnContextComparisonType', AuthnContextComparisonType)

# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType with content type ELEMENT_ONLY
class RequestAbstractType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RequestAbstractType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 29, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature'), 'Signature', '__urnoasisnamestcSAML2_0protocol_RequestAbstractType_httpwww_w3_org200009xmldsigSignature', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/ds.xsd', 43, 0), )

    
    Signature = property(__Signature.value, __Signature.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Issuer uses Python identifier Issuer
    __Issuer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer'), 'Issuer', '__urnoasisnamestcSAML2_0protocol_RequestAbstractType_urnoasisnamestcSAML2_0assertionIssuer', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 54, 4), )

    
    Issuer = property(__Issuer.value, __Issuer.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}Extensions uses Python identifier Extensions
    __Extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Extensions'), 'Extensions', '__urnoasisnamestcSAML2_0protocol_RequestAbstractType_urnoasisnamestcSAML2_0protocolExtensions', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 41, 4), )

    
    Extensions = property(__Extensions.value, __Extensions.set, None, None)

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__urnoasisnamestcSAML2_0protocol_RequestAbstractType_ID', pyxb.binding.datatypes.ID, required=True)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 35, 8)
    __ID._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 35, 8)
    
    ID = property(__ID.value, __ID.set, None, None)

    
    # Attribute Version uses Python identifier Version
    __Version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Version'), 'Version', '__urnoasisnamestcSAML2_0protocol_RequestAbstractType_Version', pyxb.binding.datatypes.string, required=True)
    __Version._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 36, 8)
    __Version._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 36, 8)
    
    Version = property(__Version.value, __Version.set, None, None)

    
    # Attribute IssueInstant uses Python identifier IssueInstant
    __IssueInstant = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'IssueInstant'), 'IssueInstant', '__urnoasisnamestcSAML2_0protocol_RequestAbstractType_IssueInstant', pyxb.binding.datatypes.dateTime, required=True)
    __IssueInstant._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 37, 8)
    __IssueInstant._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 37, 8)
    
    IssueInstant = property(__IssueInstant.value, __IssueInstant.set, None, None)

    
    # Attribute Destination uses Python identifier Destination
    __Destination = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Destination'), 'Destination', '__urnoasisnamestcSAML2_0protocol_RequestAbstractType_Destination', pyxb.binding.datatypes.anyURI)
    __Destination._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 38, 8)
    __Destination._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 38, 8)
    
    Destination = property(__Destination.value, __Destination.set, None, None)

    
    # Attribute Consent uses Python identifier Consent
    __Consent = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Consent'), 'Consent', '__urnoasisnamestcSAML2_0protocol_RequestAbstractType_Consent', pyxb.binding.datatypes.anyURI)
    __Consent._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 39, 5)
    __Consent._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 39, 5)
    
    Consent = property(__Consent.value, __Consent.set, None, None)


    _ElementMap = {
        __Signature.name() : __Signature,
        __Issuer.name() : __Issuer,
        __Extensions.name() : __Extensions
    }
    _AttributeMap = {
        __ID.name() : __ID,
        __Version.name() : __Version,
        __IssueInstant.name() : __IssueInstant,
        __Destination.name() : __Destination,
        __Consent.name() : __Consent
    }
Namespace.addCategoryObject('typeBinding', u'RequestAbstractType', RequestAbstractType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ExtensionsType with content type ELEMENT_ONLY
class ExtensionsType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ExtensionsType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ExtensionsType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 42, 4)
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ExtensionsType', ExtensionsType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType with content type ELEMENT_ONLY
class StatusResponseType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StatusResponseType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 47, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature'), 'Signature', '__urnoasisnamestcSAML2_0protocol_StatusResponseType_httpwww_w3_org200009xmldsigSignature', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/ds.xsd', 43, 0), )

    
    Signature = property(__Signature.value, __Signature.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Issuer uses Python identifier Issuer
    __Issuer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer'), 'Issuer', '__urnoasisnamestcSAML2_0protocol_StatusResponseType_urnoasisnamestcSAML2_0assertionIssuer', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 54, 4), )

    
    Issuer = property(__Issuer.value, __Issuer.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}Extensions uses Python identifier Extensions
    __Extensions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Extensions'), 'Extensions', '__urnoasisnamestcSAML2_0protocol_StatusResponseType_urnoasisnamestcSAML2_0protocolExtensions', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 41, 4), )

    
    Extensions = property(__Extensions.value, __Extensions.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}Status uses Python identifier Status
    __Status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Status'), 'Status', '__urnoasisnamestcSAML2_0protocol_StatusResponseType_urnoasisnamestcSAML2_0protocolStatus', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 61, 4), )

    
    Status = property(__Status.value, __Status.set, None, None)

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__urnoasisnamestcSAML2_0protocol_StatusResponseType_ID', pyxb.binding.datatypes.ID, required=True)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 54, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 54, 5)
    
    ID = property(__ID.value, __ID.set, None, None)

    
    # Attribute InResponseTo uses Python identifier InResponseTo
    __InResponseTo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'InResponseTo'), 'InResponseTo', '__urnoasisnamestcSAML2_0protocol_StatusResponseType_InResponseTo', pyxb.binding.datatypes.NCName)
    __InResponseTo._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 55, 5)
    __InResponseTo._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 55, 5)
    
    InResponseTo = property(__InResponseTo.value, __InResponseTo.set, None, None)

    
    # Attribute Version uses Python identifier Version
    __Version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Version'), 'Version', '__urnoasisnamestcSAML2_0protocol_StatusResponseType_Version', pyxb.binding.datatypes.string, required=True)
    __Version._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 56, 5)
    __Version._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 56, 5)
    
    Version = property(__Version.value, __Version.set, None, None)

    
    # Attribute IssueInstant uses Python identifier IssueInstant
    __IssueInstant = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'IssueInstant'), 'IssueInstant', '__urnoasisnamestcSAML2_0protocol_StatusResponseType_IssueInstant', pyxb.binding.datatypes.dateTime, required=True)
    __IssueInstant._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 57, 5)
    __IssueInstant._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 57, 5)
    
    IssueInstant = property(__IssueInstant.value, __IssueInstant.set, None, None)

    
    # Attribute Destination uses Python identifier Destination
    __Destination = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Destination'), 'Destination', '__urnoasisnamestcSAML2_0protocol_StatusResponseType_Destination', pyxb.binding.datatypes.anyURI)
    __Destination._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 58, 5)
    __Destination._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 58, 5)
    
    Destination = property(__Destination.value, __Destination.set, None, None)

    
    # Attribute Consent uses Python identifier Consent
    __Consent = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Consent'), 'Consent', '__urnoasisnamestcSAML2_0protocol_StatusResponseType_Consent', pyxb.binding.datatypes.anyURI)
    __Consent._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 59, 5)
    __Consent._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 59, 5)
    
    Consent = property(__Consent.value, __Consent.set, None, None)


    _ElementMap = {
        __Signature.name() : __Signature,
        __Issuer.name() : __Issuer,
        __Extensions.name() : __Extensions,
        __Status.name() : __Status
    }
    _AttributeMap = {
        __ID.name() : __ID,
        __InResponseTo.name() : __InResponseTo,
        __Version.name() : __Version,
        __IssueInstant.name() : __IssueInstant,
        __Destination.name() : __Destination,
        __Consent.name() : __Consent
    }
Namespace.addCategoryObject('typeBinding', u'StatusResponseType', StatusResponseType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}StatusType with content type ELEMENT_ONLY
class StatusType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}StatusType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StatusType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 62, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}StatusCode uses Python identifier StatusCode
    __StatusCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'StatusCode'), 'StatusCode', '__urnoasisnamestcSAML2_0protocol_StatusType_urnoasisnamestcSAML2_0protocolStatusCode', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 69, 4), )

    
    StatusCode = property(__StatusCode.value, __StatusCode.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}StatusMessage uses Python identifier StatusMessage
    __StatusMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'StatusMessage'), 'StatusMessage', '__urnoasisnamestcSAML2_0protocol_StatusType_urnoasisnamestcSAML2_0protocolStatusMessage', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 76, 4), )

    
    StatusMessage = property(__StatusMessage.value, __StatusMessage.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}StatusDetail uses Python identifier StatusDetail
    __StatusDetail = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'StatusDetail'), 'StatusDetail', '__urnoasisnamestcSAML2_0protocol_StatusType_urnoasisnamestcSAML2_0protocolStatusDetail', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 77, 4), )

    
    StatusDetail = property(__StatusDetail.value, __StatusDetail.set, None, None)


    _ElementMap = {
        __StatusCode.name() : __StatusCode,
        __StatusMessage.name() : __StatusMessage,
        __StatusDetail.name() : __StatusDetail
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'StatusType', StatusType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}StatusCodeType with content type ELEMENT_ONLY
class StatusCodeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}StatusCodeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StatusCodeType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 70, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}StatusCode uses Python identifier StatusCode
    __StatusCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'StatusCode'), 'StatusCode', '__urnoasisnamestcSAML2_0protocol_StatusCodeType_urnoasisnamestcSAML2_0protocolStatusCode', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 69, 4), )

    
    StatusCode = property(__StatusCode.value, __StatusCode.set, None, None)

    
    # Attribute Value uses Python identifier Value
    __Value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Value'), 'Value', '__urnoasisnamestcSAML2_0protocol_StatusCodeType_Value', pyxb.binding.datatypes.anyURI, required=True)
    __Value._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 74, 8)
    __Value._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 74, 8)
    
    Value = property(__Value.value, __Value.set, None, None)


    _ElementMap = {
        __StatusCode.name() : __StatusCode
    }
    _AttributeMap = {
        __Value.name() : __Value
    }
Namespace.addCategoryObject('typeBinding', u'StatusCodeType', StatusCodeType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}StatusDetailType with content type ELEMENT_ONLY
class StatusDetailType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}StatusDetailType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StatusDetailType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 78, 4)
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'StatusDetailType', StatusDetailType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}NameIDPolicyType with content type EMPTY
class NameIDPolicyType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}NameIDPolicyType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NameIDPolicyType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 174, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute Format uses Python identifier Format
    __Format = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Format'), 'Format', '__urnoasisnamestcSAML2_0protocol_NameIDPolicyType_Format', pyxb.binding.datatypes.anyURI)
    __Format._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 175, 8)
    __Format._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 175, 8)
    
    Format = property(__Format.value, __Format.set, None, None)

    
    # Attribute SPNameQualifier uses Python identifier SPNameQualifier
    __SPNameQualifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SPNameQualifier'), 'SPNameQualifier', '__urnoasisnamestcSAML2_0protocol_NameIDPolicyType_SPNameQualifier', pyxb.binding.datatypes.string)
    __SPNameQualifier._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 176, 8)
    __SPNameQualifier._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 176, 8)
    
    SPNameQualifier = property(__SPNameQualifier.value, __SPNameQualifier.set, None, None)

    
    # Attribute AllowCreate uses Python identifier AllowCreate
    __AllowCreate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'AllowCreate'), 'AllowCreate', '__urnoasisnamestcSAML2_0protocol_NameIDPolicyType_AllowCreate', pyxb.binding.datatypes.boolean)
    __AllowCreate._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 177, 8)
    __AllowCreate._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 177, 8)
    
    AllowCreate = property(__AllowCreate.value, __AllowCreate.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __Format.name() : __Format,
        __SPNameQualifier.name() : __SPNameQualifier,
        __AllowCreate.name() : __AllowCreate
    }
Namespace.addCategoryObject('typeBinding', u'NameIDPolicyType', NameIDPolicyType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ScopingType with content type ELEMENT_ONLY
class ScopingType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ScopingType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ScopingType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 180, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}RequesterID uses Python identifier RequesterID
    __RequesterID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'RequesterID'), 'RequesterID', '__urnoasisnamestcSAML2_0protocol_ScopingType_urnoasisnamestcSAML2_0protocolRequesterID', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 187, 4), )

    
    RequesterID = property(__RequesterID.value, __RequesterID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}IDPList uses Python identifier IDPList
    __IDPList = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'IDPList'), 'IDPList', '__urnoasisnamestcSAML2_0protocol_ScopingType_urnoasisnamestcSAML2_0protocolIDPList', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 188, 4), )

    
    IDPList = property(__IDPList.value, __IDPList.set, None, None)

    
    # Attribute ProxyCount uses Python identifier ProxyCount
    __ProxyCount = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ProxyCount'), 'ProxyCount', '__urnoasisnamestcSAML2_0protocol_ScopingType_ProxyCount', pyxb.binding.datatypes.nonNegativeInteger)
    __ProxyCount._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 185, 8)
    __ProxyCount._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 185, 8)
    
    ProxyCount = property(__ProxyCount.value, __ProxyCount.set, None, None)


    _ElementMap = {
        __RequesterID.name() : __RequesterID,
        __IDPList.name() : __IDPList
    }
    _AttributeMap = {
        __ProxyCount.name() : __ProxyCount
    }
Namespace.addCategoryObject('typeBinding', u'ScopingType', ScopingType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}IDPListType with content type ELEMENT_ONLY
class IDPListType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}IDPListType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IDPListType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 189, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}IDPEntry uses Python identifier IDPEntry
    __IDPEntry = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'IDPEntry'), 'IDPEntry', '__urnoasisnamestcSAML2_0protocol_IDPListType_urnoasisnamestcSAML2_0protocolIDPEntry', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 195, 4), )

    
    IDPEntry = property(__IDPEntry.value, __IDPEntry.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}GetComplete uses Python identifier GetComplete
    __GetComplete = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'GetComplete'), 'GetComplete', '__urnoasisnamestcSAML2_0protocol_IDPListType_urnoasisnamestcSAML2_0protocolGetComplete', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 201, 4), )

    
    GetComplete = property(__GetComplete.value, __GetComplete.set, None, None)


    _ElementMap = {
        __IDPEntry.name() : __IDPEntry,
        __GetComplete.name() : __GetComplete
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'IDPListType', IDPListType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}IDPEntryType with content type EMPTY
class IDPEntryType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}IDPEntryType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IDPEntryType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 196, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ProviderID uses Python identifier ProviderID
    __ProviderID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ProviderID'), 'ProviderID', '__urnoasisnamestcSAML2_0protocol_IDPEntryType_ProviderID', pyxb.binding.datatypes.anyURI, required=True)
    __ProviderID._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 197, 8)
    __ProviderID._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 197, 8)
    
    ProviderID = property(__ProviderID.value, __ProviderID.set, None, None)

    
    # Attribute Name uses Python identifier Name
    __Name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Name'), 'Name', '__urnoasisnamestcSAML2_0protocol_IDPEntryType_Name', pyxb.binding.datatypes.string)
    __Name._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 198, 8)
    __Name._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 198, 8)
    
    Name = property(__Name.value, __Name.set, None, None)

    
    # Attribute Loc uses Python identifier Loc
    __Loc = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Loc'), 'Loc', '__urnoasisnamestcSAML2_0protocol_IDPEntryType_Loc', pyxb.binding.datatypes.anyURI)
    __Loc._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 199, 8)
    __Loc._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 199, 8)
    
    Loc = property(__Loc.value, __Loc.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __ProviderID.name() : __ProviderID,
        __Name.name() : __Name,
        __Loc.name() : __Loc
    }
Namespace.addCategoryObject('typeBinding', u'IDPEntryType', IDPEntryType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}TerminateType with content type EMPTY
class TerminateType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}TerminateType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TerminateType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 255, 4)
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TerminateType', TerminateType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}AssertionIDRequestType with content type ELEMENT_ONLY
class AssertionIDRequestType (RequestAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}AssertionIDRequestType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AssertionIDRequestType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 84, 4)
    # Base type is RequestAbstractType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AssertionIDRef uses Python identifier AssertionIDRef
    __AssertionIDRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'AssertionIDRef'), 'AssertionIDRef', '__urnoasisnamestcSAML2_0protocol_AssertionIDRequestType_urnoasisnamestcSAML2_0assertionAssertionIDRef', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 55, 4), )

    
    AssertionIDRef = property(__AssertionIDRef.value, __AssertionIDRef.set, None, None)

    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType

    _ElementMap = RequestAbstractType._ElementMap.copy()
    _ElementMap.update({
        __AssertionIDRef.name() : __AssertionIDRef
    })
    _AttributeMap = RequestAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AssertionIDRequestType', AssertionIDRequestType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}SubjectQueryAbstractType with content type ELEMENT_ONLY
class SubjectQueryAbstractType (RequestAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}SubjectQueryAbstractType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SubjectQueryAbstractType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 94, 4)
    # Base type is RequestAbstractType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Subject uses Python identifier Subject
    __Subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Subject'), 'Subject', '__urnoasisnamestcSAML2_0protocol_SubjectQueryAbstractType_urnoasisnamestcSAML2_0assertionSubject', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 76, 4), )

    
    Subject = property(__Subject.value, __Subject.set, None, None)

    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType

    _ElementMap = RequestAbstractType._ElementMap.copy()
    _ElementMap.update({
        __Subject.name() : __Subject
    })
    _AttributeMap = RequestAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'SubjectQueryAbstractType', SubjectQueryAbstractType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}RequestedAuthnContextType with content type ELEMENT_ONLY
class RequestedAuthnContextType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}RequestedAuthnContextType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RequestedAuthnContextType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 115, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AuthnContextClassRef uses Python identifier AuthnContextClassRef
    __AuthnContextClassRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'AuthnContextClassRef'), 'AuthnContextClassRef', '__urnoasisnamestcSAML2_0protocol_RequestedAuthnContextType_urnoasisnamestcSAML2_0assertionAuthnContextClassRef', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 219, 4), )

    
    AuthnContextClassRef = property(__AuthnContextClassRef.value, __AuthnContextClassRef.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AuthnContextDeclRef uses Python identifier AuthnContextDeclRef
    __AuthnContextDeclRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'AuthnContextDeclRef'), 'AuthnContextDeclRef', '__urnoasisnamestcSAML2_0protocol_RequestedAuthnContextType_urnoasisnamestcSAML2_0assertionAuthnContextDeclRef', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 220, 4), )

    
    AuthnContextDeclRef = property(__AuthnContextDeclRef.value, __AuthnContextDeclRef.set, None, None)

    
    # Attribute Comparison uses Python identifier Comparison
    __Comparison = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Comparison'), 'Comparison', '__urnoasisnamestcSAML2_0protocol_RequestedAuthnContextType_Comparison', AuthnContextComparisonType)
    __Comparison._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 120, 8)
    __Comparison._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 120, 8)
    
    Comparison = property(__Comparison.value, __Comparison.set, None, None)


    _ElementMap = {
        __AuthnContextClassRef.name() : __AuthnContextClassRef,
        __AuthnContextDeclRef.name() : __AuthnContextDeclRef
    }
    _AttributeMap = {
        __Comparison.name() : __Comparison
    }
Namespace.addCategoryObject('typeBinding', u'RequestedAuthnContextType', RequestedAuthnContextType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}AuthnRequestType with content type ELEMENT_ONLY
class AuthnRequestType (RequestAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}AuthnRequestType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AuthnRequestType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 153, 4)
    # Base type is RequestAbstractType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Subject uses Python identifier Subject
    __Subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Subject'), 'Subject', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_urnoasisnamestcSAML2_0assertionSubject', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 76, 4), )

    
    Subject = property(__Subject.value, __Subject.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Conditions uses Python identifier Conditions
    __Conditions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Conditions'), 'Conditions', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_urnoasisnamestcSAML2_0assertionConditions', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 127, 4), )

    
    Conditions = property(__Conditions.value, __Conditions.set, None, None)

    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}RequestedAuthnContext uses Python identifier RequestedAuthnContext
    __RequestedAuthnContext = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'RequestedAuthnContext'), 'RequestedAuthnContext', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_urnoasisnamestcSAML2_0protocolRequestedAuthnContext', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 114, 4), )

    
    RequestedAuthnContext = property(__RequestedAuthnContext.value, __RequestedAuthnContext.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}NameIDPolicy uses Python identifier NameIDPolicy
    __NameIDPolicy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'NameIDPolicy'), 'NameIDPolicy', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_urnoasisnamestcSAML2_0protocolNameIDPolicy', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 173, 4), )

    
    NameIDPolicy = property(__NameIDPolicy.value, __NameIDPolicy.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}Scoping uses Python identifier Scoping
    __Scoping = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Scoping'), 'Scoping', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_urnoasisnamestcSAML2_0protocolScoping', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 179, 4), )

    
    Scoping = property(__Scoping.value, __Scoping.set, None, None)

    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute ForceAuthn uses Python identifier ForceAuthn
    __ForceAuthn = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ForceAuthn'), 'ForceAuthn', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_ForceAuthn', pyxb.binding.datatypes.boolean)
    __ForceAuthn._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 163, 16)
    __ForceAuthn._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 163, 16)
    
    ForceAuthn = property(__ForceAuthn.value, __ForceAuthn.set, None, None)

    
    # Attribute IsPassive uses Python identifier IsPassive
    __IsPassive = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'IsPassive'), 'IsPassive', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_IsPassive', pyxb.binding.datatypes.boolean)
    __IsPassive._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 164, 16)
    __IsPassive._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 164, 16)
    
    IsPassive = property(__IsPassive.value, __IsPassive.set, None, None)

    
    # Attribute ProtocolBinding uses Python identifier ProtocolBinding
    __ProtocolBinding = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ProtocolBinding'), 'ProtocolBinding', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_ProtocolBinding', pyxb.binding.datatypes.anyURI)
    __ProtocolBinding._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 165, 16)
    __ProtocolBinding._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 165, 16)
    
    ProtocolBinding = property(__ProtocolBinding.value, __ProtocolBinding.set, None, None)

    
    # Attribute AssertionConsumerServiceIndex uses Python identifier AssertionConsumerServiceIndex
    __AssertionConsumerServiceIndex = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'AssertionConsumerServiceIndex'), 'AssertionConsumerServiceIndex', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_AssertionConsumerServiceIndex', pyxb.binding.datatypes.unsignedShort)
    __AssertionConsumerServiceIndex._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 166, 16)
    __AssertionConsumerServiceIndex._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 166, 16)
    
    AssertionConsumerServiceIndex = property(__AssertionConsumerServiceIndex.value, __AssertionConsumerServiceIndex.set, None, None)

    
    # Attribute AssertionConsumerServiceURL uses Python identifier AssertionConsumerServiceURL
    __AssertionConsumerServiceURL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'AssertionConsumerServiceURL'), 'AssertionConsumerServiceURL', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_AssertionConsumerServiceURL', pyxb.binding.datatypes.anyURI)
    __AssertionConsumerServiceURL._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 167, 16)
    __AssertionConsumerServiceURL._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 167, 16)
    
    AssertionConsumerServiceURL = property(__AssertionConsumerServiceURL.value, __AssertionConsumerServiceURL.set, None, None)

    
    # Attribute AttributeConsumingServiceIndex uses Python identifier AttributeConsumingServiceIndex
    __AttributeConsumingServiceIndex = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'AttributeConsumingServiceIndex'), 'AttributeConsumingServiceIndex', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_AttributeConsumingServiceIndex', pyxb.binding.datatypes.unsignedShort)
    __AttributeConsumingServiceIndex._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 168, 16)
    __AttributeConsumingServiceIndex._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 168, 16)
    
    AttributeConsumingServiceIndex = property(__AttributeConsumingServiceIndex.value, __AttributeConsumingServiceIndex.set, None, None)

    
    # Attribute ProviderName uses Python identifier ProviderName
    __ProviderName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ProviderName'), 'ProviderName', '__urnoasisnamestcSAML2_0protocol_AuthnRequestType_ProviderName', pyxb.binding.datatypes.string)
    __ProviderName._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 169, 16)
    __ProviderName._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 169, 16)
    
    ProviderName = property(__ProviderName.value, __ProviderName.set, None, None)


    _ElementMap = RequestAbstractType._ElementMap.copy()
    _ElementMap.update({
        __Subject.name() : __Subject,
        __Conditions.name() : __Conditions,
        __RequestedAuthnContext.name() : __RequestedAuthnContext,
        __NameIDPolicy.name() : __NameIDPolicy,
        __Scoping.name() : __Scoping
    })
    _AttributeMap = RequestAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        __ForceAuthn.name() : __ForceAuthn,
        __IsPassive.name() : __IsPassive,
        __ProtocolBinding.name() : __ProtocolBinding,
        __AssertionConsumerServiceIndex.name() : __AssertionConsumerServiceIndex,
        __AssertionConsumerServiceURL.name() : __AssertionConsumerServiceURL,
        __AttributeConsumingServiceIndex.name() : __AttributeConsumingServiceIndex,
        __ProviderName.name() : __ProviderName
    })
Namespace.addCategoryObject('typeBinding', u'AuthnRequestType', AuthnRequestType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ResponseType with content type ELEMENT_ONLY
class ResponseType (StatusResponseType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ResponseType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ResponseType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 203, 4)
    # Base type is StatusResponseType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Assertion uses Python identifier Assertion
    __Assertion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Assertion'), 'Assertion', '__urnoasisnamestcSAML2_0protocol_ResponseType_urnoasisnamestcSAML2_0assertionAssertion', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 57, 4), )

    
    Assertion = property(__Assertion.value, __Assertion.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedAssertion uses Python identifier EncryptedAssertion
    __EncryptedAssertion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedAssertion'), 'EncryptedAssertion', '__urnoasisnamestcSAML2_0protocol_ResponseType_urnoasisnamestcSAML2_0assertionEncryptedAssertion', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 178, 4), )

    
    EncryptedAssertion = property(__EncryptedAssertion.value, __EncryptedAssertion.set, None, None)

    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Element Status ({urn:oasis:names:tc:SAML:2.0:protocol}Status) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute InResponseTo inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType

    _ElementMap = StatusResponseType._ElementMap.copy()
    _ElementMap.update({
        __Assertion.name() : __Assertion,
        __EncryptedAssertion.name() : __EncryptedAssertion
    })
    _AttributeMap = StatusResponseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ResponseType', ResponseType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ArtifactResolveType with content type ELEMENT_ONLY
class ArtifactResolveType (RequestAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ArtifactResolveType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ArtifactResolveType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 214, 4)
    # Base type is RequestAbstractType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}Artifact uses Python identifier Artifact
    __Artifact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Artifact'), 'Artifact', '__urnoasisnamestcSAML2_0protocol_ArtifactResolveType_urnoasisnamestcSAML2_0protocolArtifact', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 223, 4), )

    
    Artifact = property(__Artifact.value, __Artifact.set, None, None)

    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType

    _ElementMap = RequestAbstractType._ElementMap.copy()
    _ElementMap.update({
        __Artifact.name() : __Artifact
    })
    _AttributeMap = RequestAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ArtifactResolveType', ArtifactResolveType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ArtifactResponseType with content type ELEMENT_ONLY
class ArtifactResponseType (StatusResponseType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ArtifactResponseType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ArtifactResponseType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 225, 4)
    # Base type is StatusResponseType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Element Status ({urn:oasis:names:tc:SAML:2.0:protocol}Status) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute InResponseTo inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    _HasWildcardElement = True

    _ElementMap = StatusResponseType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = StatusResponseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ArtifactResponseType', ArtifactResponseType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ManageNameIDRequestType with content type ELEMENT_ONLY
class ManageNameIDRequestType (RequestAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}ManageNameIDRequestType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ManageNameIDRequestType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 235, 4)
    # Base type is RequestAbstractType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}NameID uses Python identifier NameID
    __NameID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID'), 'NameID', '__urnoasisnamestcSAML2_0protocol_ManageNameIDRequestType_urnoasisnamestcSAML2_0assertionNameID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4), )

    
    NameID = property(__NameID.value, __NameID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedID uses Python identifier EncryptedID
    __EncryptedID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID'), 'EncryptedID', '__urnoasisnamestcSAML2_0protocol_ManageNameIDRequestType_urnoasisnamestcSAML2_0assertionEncryptedID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4), )

    
    EncryptedID = property(__EncryptedID.value, __EncryptedID.set, None, None)

    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}NewID uses Python identifier NewID
    __NewID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'NewID'), 'NewID', '__urnoasisnamestcSAML2_0protocol_ManageNameIDRequestType_urnoasisnamestcSAML2_0protocolNewID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 252, 4), )

    
    NewID = property(__NewID.value, __NewID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}NewEncryptedID uses Python identifier NewEncryptedID
    __NewEncryptedID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'NewEncryptedID'), 'NewEncryptedID', '__urnoasisnamestcSAML2_0protocol_ManageNameIDRequestType_urnoasisnamestcSAML2_0protocolNewEncryptedID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 253, 4), )

    
    NewEncryptedID = property(__NewEncryptedID.value, __NewEncryptedID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}Terminate uses Python identifier Terminate
    __Terminate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Terminate'), 'Terminate', '__urnoasisnamestcSAML2_0protocol_ManageNameIDRequestType_urnoasisnamestcSAML2_0protocolTerminate', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 254, 4), )

    
    Terminate = property(__Terminate.value, __Terminate.set, None, None)

    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType

    _ElementMap = RequestAbstractType._ElementMap.copy()
    _ElementMap.update({
        __NameID.name() : __NameID,
        __EncryptedID.name() : __EncryptedID,
        __NewID.name() : __NewID,
        __NewEncryptedID.name() : __NewEncryptedID,
        __Terminate.name() : __Terminate
    })
    _AttributeMap = RequestAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ManageNameIDRequestType', ManageNameIDRequestType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}LogoutRequestType with content type ELEMENT_ONLY
class LogoutRequestType (RequestAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}LogoutRequestType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LogoutRequestType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 258, 4)
    # Base type is RequestAbstractType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}BaseID uses Python identifier BaseID
    __BaseID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'BaseID'), 'BaseID', '__urnoasisnamestcSAML2_0protocol_LogoutRequestType_urnoasisnamestcSAML2_0assertionBaseID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 33, 4), )

    
    BaseID = property(__BaseID.value, __BaseID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}NameID uses Python identifier NameID
    __NameID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID'), 'NameID', '__urnoasisnamestcSAML2_0protocol_LogoutRequestType_urnoasisnamestcSAML2_0assertionNameID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4), )

    
    NameID = property(__NameID.value, __NameID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedID uses Python identifier EncryptedID
    __EncryptedID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID'), 'EncryptedID', '__urnoasisnamestcSAML2_0protocol_LogoutRequestType_urnoasisnamestcSAML2_0assertionEncryptedID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4), )

    
    EncryptedID = property(__EncryptedID.value, __EncryptedID.set, None, None)

    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}SessionIndex uses Python identifier SessionIndex
    __SessionIndex = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'SessionIndex'), 'SessionIndex', '__urnoasisnamestcSAML2_0protocol_LogoutRequestType_urnoasisnamestcSAML2_0protocolSessionIndex', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 274, 4), )

    
    SessionIndex = property(__SessionIndex.value, __SessionIndex.set, None, None)

    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Reason uses Python identifier Reason
    __Reason = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Reason'), 'Reason', '__urnoasisnamestcSAML2_0protocol_LogoutRequestType_Reason', pyxb.binding.datatypes.string)
    __Reason._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 269, 16)
    __Reason._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 269, 16)
    
    Reason = property(__Reason.value, __Reason.set, None, None)

    
    # Attribute NotOnOrAfter uses Python identifier NotOnOrAfter
    __NotOnOrAfter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NotOnOrAfter'), 'NotOnOrAfter', '__urnoasisnamestcSAML2_0protocol_LogoutRequestType_NotOnOrAfter', pyxb.binding.datatypes.dateTime)
    __NotOnOrAfter._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 270, 16)
    __NotOnOrAfter._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 270, 16)
    
    NotOnOrAfter = property(__NotOnOrAfter.value, __NotOnOrAfter.set, None, None)


    _ElementMap = RequestAbstractType._ElementMap.copy()
    _ElementMap.update({
        __BaseID.name() : __BaseID,
        __NameID.name() : __NameID,
        __EncryptedID.name() : __EncryptedID,
        __SessionIndex.name() : __SessionIndex
    })
    _AttributeMap = RequestAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        __Reason.name() : __Reason,
        __NotOnOrAfter.name() : __NotOnOrAfter
    })
Namespace.addCategoryObject('typeBinding', u'LogoutRequestType', LogoutRequestType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}NameIDMappingRequestType with content type ELEMENT_ONLY
class NameIDMappingRequestType (RequestAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}NameIDMappingRequestType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NameIDMappingRequestType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 277, 4)
    # Base type is RequestAbstractType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}BaseID uses Python identifier BaseID
    __BaseID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'BaseID'), 'BaseID', '__urnoasisnamestcSAML2_0protocol_NameIDMappingRequestType_urnoasisnamestcSAML2_0assertionBaseID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 33, 4), )

    
    BaseID = property(__BaseID.value, __BaseID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}NameID uses Python identifier NameID
    __NameID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID'), 'NameID', '__urnoasisnamestcSAML2_0protocol_NameIDMappingRequestType_urnoasisnamestcSAML2_0assertionNameID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4), )

    
    NameID = property(__NameID.value, __NameID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedID uses Python identifier EncryptedID
    __EncryptedID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID'), 'EncryptedID', '__urnoasisnamestcSAML2_0protocol_NameIDMappingRequestType_urnoasisnamestcSAML2_0assertionEncryptedID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4), )

    
    EncryptedID = property(__EncryptedID.value, __EncryptedID.set, None, None)

    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}NameIDPolicy uses Python identifier NameIDPolicy
    __NameIDPolicy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'NameIDPolicy'), 'NameIDPolicy', '__urnoasisnamestcSAML2_0protocol_NameIDMappingRequestType_urnoasisnamestcSAML2_0protocolNameIDPolicy', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 173, 4), )

    
    NameIDPolicy = property(__NameIDPolicy.value, __NameIDPolicy.set, None, None)

    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType

    _ElementMap = RequestAbstractType._ElementMap.copy()
    _ElementMap.update({
        __BaseID.name() : __BaseID,
        __NameID.name() : __NameID,
        __EncryptedID.name() : __EncryptedID,
        __NameIDPolicy.name() : __NameIDPolicy
    })
    _AttributeMap = RequestAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'NameIDMappingRequestType', NameIDMappingRequestType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}NameIDMappingResponseType with content type ELEMENT_ONLY
class NameIDMappingResponseType (StatusResponseType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}NameIDMappingResponseType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NameIDMappingResponseType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 292, 4)
    # Base type is StatusResponseType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}NameID uses Python identifier NameID
    __NameID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID'), 'NameID', '__urnoasisnamestcSAML2_0protocol_NameIDMappingResponseType_urnoasisnamestcSAML2_0assertionNameID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4), )

    
    NameID = property(__NameID.value, __NameID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedID uses Python identifier EncryptedID
    __EncryptedID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID'), 'EncryptedID', '__urnoasisnamestcSAML2_0protocol_NameIDMappingResponseType_urnoasisnamestcSAML2_0assertionEncryptedID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4), )

    
    EncryptedID = property(__EncryptedID.value, __EncryptedID.set, None, None)

    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Element Status ({urn:oasis:names:tc:SAML:2.0:protocol}Status) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute InResponseTo inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}StatusResponseType

    _ElementMap = StatusResponseType._ElementMap.copy()
    _ElementMap.update({
        __NameID.name() : __NameID,
        __EncryptedID.name() : __EncryptedID
    })
    _AttributeMap = StatusResponseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'NameIDMappingResponseType', NameIDMappingResponseType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}AuthnQueryType with content type ELEMENT_ONLY
class AuthnQueryType (SubjectQueryAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}AuthnQueryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AuthnQueryType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 104, 4)
    # Base type is SubjectQueryAbstractType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Subject ({urn:oasis:names:tc:SAML:2.0:assertion}Subject) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}SubjectQueryAbstractType
    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:protocol}RequestedAuthnContext uses Python identifier RequestedAuthnContext
    __RequestedAuthnContext = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'RequestedAuthnContext'), 'RequestedAuthnContext', '__urnoasisnamestcSAML2_0protocol_AuthnQueryType_urnoasisnamestcSAML2_0protocolRequestedAuthnContext', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 114, 4), )

    
    RequestedAuthnContext = property(__RequestedAuthnContext.value, __RequestedAuthnContext.set, None, None)

    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute SessionIndex uses Python identifier SessionIndex
    __SessionIndex = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SessionIndex'), 'SessionIndex', '__urnoasisnamestcSAML2_0protocol_AuthnQueryType_SessionIndex', pyxb.binding.datatypes.string)
    __SessionIndex._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 110, 16)
    __SessionIndex._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 110, 16)
    
    SessionIndex = property(__SessionIndex.value, __SessionIndex.set, None, None)


    _ElementMap = SubjectQueryAbstractType._ElementMap.copy()
    _ElementMap.update({
        __RequestedAuthnContext.name() : __RequestedAuthnContext
    })
    _AttributeMap = SubjectQueryAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        __SessionIndex.name() : __SessionIndex
    })
Namespace.addCategoryObject('typeBinding', u'AuthnQueryType', AuthnQueryType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}AttributeQueryType with content type ELEMENT_ONLY
class AttributeQueryType (SubjectQueryAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}AttributeQueryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AttributeQueryType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 131, 4)
    # Base type is SubjectQueryAbstractType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Subject ({urn:oasis:names:tc:SAML:2.0:assertion}Subject) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}SubjectQueryAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Attribute uses Python identifier Attribute
    __Attribute = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Attribute'), 'Attribute', '__urnoasisnamestcSAML2_0protocol_AttributeQueryType_urnoasisnamestcSAML2_0assertionAttribute', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 271, 4), )

    
    Attribute = property(__Attribute.value, __Attribute.set, None, None)

    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType

    _ElementMap = SubjectQueryAbstractType._ElementMap.copy()
    _ElementMap.update({
        __Attribute.name() : __Attribute
    })
    _AttributeMap = SubjectQueryAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AttributeQueryType', AttributeQueryType)


# Complex type {urn:oasis:names:tc:SAML:2.0:protocol}AuthzDecisionQueryType with content type ELEMENT_ONLY
class AuthzDecisionQueryType (SubjectQueryAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:protocol}AuthzDecisionQueryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AuthzDecisionQueryType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 141, 4)
    # Base type is SubjectQueryAbstractType
    
    # Element Signature ({http://www.w3.org/2000/09/xmldsig#}Signature) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Issuer ({urn:oasis:names:tc:SAML:2.0:assertion}Issuer) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Element Subject ({urn:oasis:names:tc:SAML:2.0:assertion}Subject) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}SubjectQueryAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Action uses Python identifier Action
    __Action = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Action'), 'Action', '__urnoasisnamestcSAML2_0protocol_AuthzDecisionQueryType_urnoasisnamestcSAML2_0assertionAction', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 243, 4), )

    
    Action = property(__Action.value, __Action.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Evidence uses Python identifier Evidence
    __Evidence = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Evidence'), 'Evidence', '__urnoasisnamestcSAML2_0protocol_AuthzDecisionQueryType_urnoasisnamestcSAML2_0assertionEvidence', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 251, 4), )

    
    Evidence = property(__Evidence.value, __Evidence.set, None, None)

    
    # Element Extensions ({urn:oasis:names:tc:SAML:2.0:protocol}Extensions) inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute ID inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Version inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute IssueInstant inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Destination inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Consent inherited from {urn:oasis:names:tc:SAML:2.0:protocol}RequestAbstractType
    
    # Attribute Resource uses Python identifier Resource
    __Resource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Resource'), 'Resource', '__urnoasisnamestcSAML2_0protocol_AuthzDecisionQueryType_Resource', pyxb.binding.datatypes.anyURI, required=True)
    __Resource._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 148, 16)
    __Resource._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 148, 16)
    
    Resource = property(__Resource.value, __Resource.set, None, None)


    _ElementMap = SubjectQueryAbstractType._ElementMap.copy()
    _ElementMap.update({
        __Action.name() : __Action,
        __Evidence.name() : __Evidence
    })
    _AttributeMap = SubjectQueryAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        __Resource.name() : __Resource
    })
Namespace.addCategoryObject('typeBinding', u'AuthzDecisionQueryType', AuthzDecisionQueryType)


StatusMessage = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'StatusMessage'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 76, 4))
Namespace.addCategoryObject('elementBinding', StatusMessage.name().localName(), StatusMessage)

RequesterID = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RequesterID'), pyxb.binding.datatypes.anyURI, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 187, 4))
Namespace.addCategoryObject('elementBinding', RequesterID.name().localName(), RequesterID)

GetComplete = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetComplete'), pyxb.binding.datatypes.anyURI, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 201, 4))
Namespace.addCategoryObject('elementBinding', GetComplete.name().localName(), GetComplete)

Artifact = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Artifact'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 223, 4))
Namespace.addCategoryObject('elementBinding', Artifact.name().localName(), Artifact)

NewID = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NewID'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 252, 4))
Namespace.addCategoryObject('elementBinding', NewID.name().localName(), NewID)

NewEncryptedID = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NewEncryptedID'), pyxb.bundles.saml20.assertion.EncryptedElementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 253, 4))
Namespace.addCategoryObject('elementBinding', NewEncryptedID.name().localName(), NewEncryptedID)

SessionIndex = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SessionIndex'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 274, 4))
Namespace.addCategoryObject('elementBinding', SessionIndex.name().localName(), SessionIndex)

Extensions = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Extensions'), ExtensionsType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 41, 4))
Namespace.addCategoryObject('elementBinding', Extensions.name().localName(), Extensions)

Status = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Status'), StatusType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 61, 4))
Namespace.addCategoryObject('elementBinding', Status.name().localName(), Status)

StatusCode = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'StatusCode'), StatusCodeType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 69, 4))
Namespace.addCategoryObject('elementBinding', StatusCode.name().localName(), StatusCode)

StatusDetail = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'StatusDetail'), StatusDetailType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 77, 4))
Namespace.addCategoryObject('elementBinding', StatusDetail.name().localName(), StatusDetail)

NameIDPolicy = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NameIDPolicy'), NameIDPolicyType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 173, 4))
Namespace.addCategoryObject('elementBinding', NameIDPolicy.name().localName(), NameIDPolicy)

Scoping = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Scoping'), ScopingType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 179, 4))
Namespace.addCategoryObject('elementBinding', Scoping.name().localName(), Scoping)

IDPList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IDPList'), IDPListType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 188, 4))
Namespace.addCategoryObject('elementBinding', IDPList.name().localName(), IDPList)

IDPEntry = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IDPEntry'), IDPEntryType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 195, 4))
Namespace.addCategoryObject('elementBinding', IDPEntry.name().localName(), IDPEntry)

Terminate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Terminate'), TerminateType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 254, 4))
Namespace.addCategoryObject('elementBinding', Terminate.name().localName(), Terminate)

ManageNameIDResponse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ManageNameIDResponse'), StatusResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 256, 4))
Namespace.addCategoryObject('elementBinding', ManageNameIDResponse.name().localName(), ManageNameIDResponse)

LogoutResponse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'LogoutResponse'), StatusResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 275, 4))
Namespace.addCategoryObject('elementBinding', LogoutResponse.name().localName(), LogoutResponse)

AssertionIDRequest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AssertionIDRequest'), AssertionIDRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 83, 4))
Namespace.addCategoryObject('elementBinding', AssertionIDRequest.name().localName(), AssertionIDRequest)

SubjectQuery = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SubjectQuery'), SubjectQueryAbstractType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 93, 4))
Namespace.addCategoryObject('elementBinding', SubjectQuery.name().localName(), SubjectQuery)

RequestedAuthnContext = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RequestedAuthnContext'), RequestedAuthnContextType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 114, 4))
Namespace.addCategoryObject('elementBinding', RequestedAuthnContext.name().localName(), RequestedAuthnContext)

AuthnRequest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnRequest'), AuthnRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 152, 4))
Namespace.addCategoryObject('elementBinding', AuthnRequest.name().localName(), AuthnRequest)

Response = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Response'), ResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 202, 4))
Namespace.addCategoryObject('elementBinding', Response.name().localName(), Response)

ArtifactResolve = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ArtifactResolve'), ArtifactResolveType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 213, 4))
Namespace.addCategoryObject('elementBinding', ArtifactResolve.name().localName(), ArtifactResolve)

ArtifactResponse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ArtifactResponse'), ArtifactResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 224, 4))
Namespace.addCategoryObject('elementBinding', ArtifactResponse.name().localName(), ArtifactResponse)

ManageNameIDRequest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ManageNameIDRequest'), ManageNameIDRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 234, 4))
Namespace.addCategoryObject('elementBinding', ManageNameIDRequest.name().localName(), ManageNameIDRequest)

LogoutRequest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'LogoutRequest'), LogoutRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 257, 4))
Namespace.addCategoryObject('elementBinding', LogoutRequest.name().localName(), LogoutRequest)

NameIDMappingRequest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NameIDMappingRequest'), NameIDMappingRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 276, 4))
Namespace.addCategoryObject('elementBinding', NameIDMappingRequest.name().localName(), NameIDMappingRequest)

NameIDMappingResponse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NameIDMappingResponse'), NameIDMappingResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 291, 4))
Namespace.addCategoryObject('elementBinding', NameIDMappingResponse.name().localName(), NameIDMappingResponse)

AuthnQuery = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnQuery'), AuthnQueryType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 103, 4))
Namespace.addCategoryObject('elementBinding', AuthnQuery.name().localName(), AuthnQuery)

AttributeQuery = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AttributeQuery'), AttributeQueryType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 130, 4))
Namespace.addCategoryObject('elementBinding', AttributeQuery.name().localName(), AttributeQuery)

AuthzDecisionQuery = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthzDecisionQuery'), AuthzDecisionQueryType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 140, 4))
Namespace.addCategoryObject('elementBinding', AuthzDecisionQuery.name().localName(), AuthzDecisionQuery)



RequestAbstractType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature'), pyxb.bundles.wssplat.ds.SignatureType, scope=RequestAbstractType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/ds.xsd', 43, 0)))

RequestAbstractType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer'), pyxb.bundles.saml20.assertion.NameIDType, scope=RequestAbstractType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 54, 4)))

RequestAbstractType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Extensions'), ExtensionsType, scope=RequestAbstractType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 41, 4)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(RequestAbstractType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(RequestAbstractType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(RequestAbstractType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
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
RequestAbstractType._Automaton = _BuildAutomaton()




def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, u'urn:oasis:names:tc:SAML:2.0:protocol')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 44, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ExtensionsType._Automaton = _BuildAutomaton_()




StatusResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature'), pyxb.bundles.wssplat.ds.SignatureType, scope=StatusResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/ds.xsd', 43, 0)))

StatusResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer'), pyxb.bundles.saml20.assertion.NameIDType, scope=StatusResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 54, 4)))

StatusResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Extensions'), ExtensionsType, scope=StatusResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 41, 4)))

StatusResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Status'), StatusType, scope=StatusResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 61, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 49, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 50, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 51, 12))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StatusResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 49, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StatusResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 50, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(StatusResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 51, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(StatusResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Status')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 52, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
StatusResponseType._Automaton = _BuildAutomaton_2()




StatusType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'StatusCode'), StatusCodeType, scope=StatusType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 69, 4)))

StatusType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'StatusMessage'), pyxb.binding.datatypes.string, scope=StatusType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 76, 4)))

StatusType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'StatusDetail'), StatusDetailType, scope=StatusType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 77, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 65, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 66, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(StatusType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'StatusCode')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 64, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(StatusType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'StatusMessage')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 65, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(StatusType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'StatusDetail')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 66, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
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
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
StatusType._Automaton = _BuildAutomaton_3()




StatusCodeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'StatusCode'), StatusCodeType, scope=StatusCodeType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 69, 4)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 72, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(StatusCodeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'StatusCode')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 72, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
StatusCodeType._Automaton = _BuildAutomaton_4()




def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 80, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 80, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
StatusDetailType._Automaton = _BuildAutomaton_5()




ScopingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RequesterID'), pyxb.binding.datatypes.anyURI, scope=ScopingType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 187, 4)))

ScopingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IDPList'), IDPListType, scope=ScopingType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 188, 4)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 182, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 183, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ScopingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'IDPList')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 182, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ScopingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'RequesterID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 183, 12))
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
ScopingType._Automaton = _BuildAutomaton_6()




IDPListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IDPEntry'), IDPEntryType, scope=IDPListType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 195, 4)))

IDPListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetComplete'), pyxb.binding.datatypes.anyURI, scope=IDPListType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 201, 4)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 192, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(IDPListType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'IDPEntry')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 191, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(IDPListType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'GetComplete')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 192, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
IDPListType._Automaton = _BuildAutomaton_7()




AssertionIDRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'AssertionIDRef'), pyxb.binding.datatypes.NCName, scope=AssertionIDRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 55, 4)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AssertionIDRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AssertionIDRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AssertionIDRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AssertionIDRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'AssertionIDRef')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 88, 20))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AssertionIDRequestType._Automaton = _BuildAutomaton_8()




SubjectQueryAbstractType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Subject'), pyxb.bundles.saml20.assertion.SubjectType, scope=SubjectQueryAbstractType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 76, 4)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SubjectQueryAbstractType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SubjectQueryAbstractType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(SubjectQueryAbstractType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SubjectQueryAbstractType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Subject')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 98, 20))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SubjectQueryAbstractType._Automaton = _BuildAutomaton_9()




RequestedAuthnContextType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'AuthnContextClassRef'), pyxb.binding.datatypes.anyURI, scope=RequestedAuthnContextType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 219, 4)))

RequestedAuthnContextType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'AuthnContextDeclRef'), pyxb.binding.datatypes.anyURI, scope=RequestedAuthnContextType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 220, 4)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(RequestedAuthnContextType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'AuthnContextClassRef')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 117, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(RequestedAuthnContextType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'AuthnContextDeclRef')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 118, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
RequestedAuthnContextType._Automaton = _BuildAutomaton_10()




AuthnRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Subject'), pyxb.bundles.saml20.assertion.SubjectType, scope=AuthnRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 76, 4)))

AuthnRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Conditions'), pyxb.bundles.saml20.assertion.ConditionsType, scope=AuthnRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 127, 4)))

AuthnRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RequestedAuthnContext'), RequestedAuthnContextType, scope=AuthnRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 114, 4)))

AuthnRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NameIDPolicy'), NameIDPolicyType, scope=AuthnRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 173, 4)))

AuthnRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Scoping'), ScopingType, scope=AuthnRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 179, 4)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 157, 20))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 158, 20))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 159, 20))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 160, 20))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 161, 20))
    counters.add(cc_7)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AuthnRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(AuthnRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(AuthnRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(AuthnRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Subject')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 157, 20))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(AuthnRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'NameIDPolicy')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 158, 20))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(AuthnRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Conditions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 159, 20))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(AuthnRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'RequestedAuthnContext')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 160, 20))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(AuthnRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Scoping')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 161, 20))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
AuthnRequestType._Automaton = _BuildAutomaton_11()




ResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Assertion'), pyxb.bundles.saml20.assertion.AssertionType, scope=ResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 57, 4)))

ResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedAssertion'), pyxb.bundles.saml20.assertion.EncryptedElementType, scope=ResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 178, 4)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 49, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 50, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 51, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 206, 16))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 49, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 50, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 51, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Status')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 52, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(ResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Assertion')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 207, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(ResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedAssertion')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 208, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ResponseType._Automaton = _BuildAutomaton_12()




ArtifactResolveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Artifact'), pyxb.binding.datatypes.string, scope=ArtifactResolveType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 223, 4)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArtifactResolveType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArtifactResolveType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArtifactResolveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ArtifactResolveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Artifact')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 218, 20))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ArtifactResolveType._Automaton = _BuildAutomaton_13()




def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 49, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 50, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 51, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 229, 20))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArtifactResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 49, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArtifactResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 50, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ArtifactResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 51, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ArtifactResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Status')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 52, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 229, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ArtifactResponseType._Automaton = _BuildAutomaton_14()




ManageNameIDRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID'), pyxb.bundles.saml20.assertion.NameIDType, scope=ManageNameIDRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4)))

ManageNameIDRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID'), pyxb.bundles.saml20.assertion.EncryptedElementType, scope=ManageNameIDRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4)))

ManageNameIDRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NewID'), pyxb.binding.datatypes.string, scope=ManageNameIDRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 252, 4)))

ManageNameIDRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NewEncryptedID'), pyxb.bundles.saml20.assertion.EncryptedElementType, scope=ManageNameIDRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 253, 4)))

ManageNameIDRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Terminate'), TerminateType, scope=ManageNameIDRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 254, 4)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ManageNameIDRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ManageNameIDRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ManageNameIDRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ManageNameIDRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 240, 24))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ManageNameIDRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 241, 24))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ManageNameIDRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'NewID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 244, 24))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ManageNameIDRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'NewEncryptedID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 245, 24))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ManageNameIDRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Terminate')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 246, 24))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    transitions = []
    st_6._set_transitionSet(transitions)
    transitions = []
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ManageNameIDRequestType._Automaton = _BuildAutomaton_15()




LogoutRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'BaseID'), pyxb.bundles.saml20.assertion.BaseIDAbstractType, scope=LogoutRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 33, 4)))

LogoutRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID'), pyxb.bundles.saml20.assertion.NameIDType, scope=LogoutRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4)))

LogoutRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID'), pyxb.bundles.saml20.assertion.EncryptedElementType, scope=LogoutRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4)))

LogoutRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SessionIndex'), pyxb.binding.datatypes.string, scope=LogoutRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 274, 4)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 267, 20))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogoutRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogoutRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(LogoutRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LogoutRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'BaseID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 263, 24))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LogoutRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 264, 24))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(LogoutRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 265, 24))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(LogoutRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SessionIndex')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 267, 20))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
LogoutRequestType._Automaton = _BuildAutomaton_16()




NameIDMappingRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'BaseID'), pyxb.bundles.saml20.assertion.BaseIDAbstractType, scope=NameIDMappingRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 33, 4)))

NameIDMappingRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID'), pyxb.bundles.saml20.assertion.NameIDType, scope=NameIDMappingRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4)))

NameIDMappingRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID'), pyxb.bundles.saml20.assertion.EncryptedElementType, scope=NameIDMappingRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4)))

NameIDMappingRequestType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NameIDPolicy'), NameIDPolicyType, scope=NameIDMappingRequestType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 173, 4)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(NameIDMappingRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(NameIDMappingRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(NameIDMappingRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(NameIDMappingRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'BaseID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 282, 24))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(NameIDMappingRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 283, 24))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(NameIDMappingRequestType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 284, 24))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(NameIDMappingRequestType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'NameIDPolicy')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 286, 20))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
NameIDMappingRequestType._Automaton = _BuildAutomaton_17()




NameIDMappingResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID'), pyxb.bundles.saml20.assertion.NameIDType, scope=NameIDMappingResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4)))

NameIDMappingResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID'), pyxb.bundles.saml20.assertion.EncryptedElementType, scope=NameIDMappingResponseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 49, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 50, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 51, 12))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(NameIDMappingResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 49, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(NameIDMappingResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 50, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(NameIDMappingResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 51, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(NameIDMappingResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Status')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 52, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(NameIDMappingResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'NameID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 296, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(NameIDMappingResponseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'EncryptedID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 297, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
NameIDMappingResponseType._Automaton = _BuildAutomaton_18()




AuthnQueryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RequestedAuthnContext'), RequestedAuthnContextType, scope=AuthnQueryType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 114, 4)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 108, 20))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AuthnQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AuthnQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AuthnQueryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AuthnQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Subject')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 98, 20))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(AuthnQueryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'RequestedAuthnContext')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 108, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AuthnQueryType._Automaton = _BuildAutomaton_19()




AttributeQueryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Attribute'), pyxb.bundles.saml20.assertion.AttributeType, scope=AttributeQueryType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 271, 4)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 135, 20))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AttributeQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AttributeQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AttributeQueryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AttributeQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Subject')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 98, 20))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(AttributeQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Attribute')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 135, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AttributeQueryType._Automaton = _BuildAutomaton_20()




AuthzDecisionQueryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Action'), pyxb.bundles.saml20.assertion.ActionType, scope=AuthzDecisionQueryType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 243, 4)))

AuthzDecisionQueryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Evidence'), pyxb.bundles.saml20.assertion.EvidenceType, scope=AuthzDecisionQueryType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 251, 4)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 146, 20))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AuthzDecisionQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 31, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AuthzDecisionQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 32, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AuthzDecisionQueryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Extensions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AuthzDecisionQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Subject')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 98, 20))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AuthzDecisionQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Action')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 145, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(AuthzDecisionQueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion'), u'Evidence')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/protocol.xsd', 146, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AuthzDecisionQueryType._Automaton = _BuildAutomaton_21()

