# ./pyxb/bundles/saml20/raw/assertion.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:c67eab1e6d7826a8e79aaf9536d1cb355237afad
# Generated 2012-12-17 13:09:31.529662 by PyXB version 1.2.1
# Namespace urn:oasis:names:tc:SAML:2.0:assertion

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:496ccb02-487d-11e2-9031-c8600024e903')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.wssplat.xenc
import pyxb.bundles.wssplat.ds

Namespace = pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:assertion', create_if_missing=True)
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


# Atomic simple type: {urn:oasis:names:tc:SAML:2.0:assertion}DecisionType
class DecisionType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DecisionType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 236, 4)
    _Documentation = None
DecisionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=DecisionType, enum_prefix=None)
DecisionType.Permit = DecisionType._CF_enumeration.addEnumeration(unicode_value=u'Permit', tag=u'Permit')
DecisionType.Deny = DecisionType._CF_enumeration.addEnumeration(unicode_value=u'Deny', tag=u'Deny')
DecisionType.Indeterminate = DecisionType._CF_enumeration.addEnumeration(unicode_value=u'Indeterminate', tag=u'Indeterminate')
DecisionType._InitializeFacetMap(DecisionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'DecisionType', DecisionType)

# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}BaseIDAbstractType with content type EMPTY
class BaseIDAbstractType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}BaseIDAbstractType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BaseIDAbstractType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 34, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute NameQualifier uses Python identifier NameQualifier
    __NameQualifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NameQualifier'), 'NameQualifier', '__urnoasisnamestcSAML2_0assertion_BaseIDAbstractType_NameQualifier', pyxb.binding.datatypes.string)
    __NameQualifier._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 30, 8)
    __NameQualifier._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 30, 8)
    
    NameQualifier = property(__NameQualifier.value, __NameQualifier.set, None, None)

    
    # Attribute SPNameQualifier uses Python identifier SPNameQualifier
    __SPNameQualifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SPNameQualifier'), 'SPNameQualifier', '__urnoasisnamestcSAML2_0assertion_BaseIDAbstractType_SPNameQualifier', pyxb.binding.datatypes.string)
    __SPNameQualifier._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 31, 8)
    __SPNameQualifier._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 31, 8)
    
    SPNameQualifier = property(__SPNameQualifier.value, __SPNameQualifier.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __NameQualifier.name() : __NameQualifier,
        __SPNameQualifier.name() : __SPNameQualifier
    }
Namespace.addCategoryObject('typeBinding', u'BaseIDAbstractType', BaseIDAbstractType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}NameIDType with content type SIMPLE
class NameIDType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}NameIDType with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NameIDType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 38, 4)
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute NameQualifier uses Python identifier NameQualifier
    __NameQualifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NameQualifier'), 'NameQualifier', '__urnoasisnamestcSAML2_0assertion_NameIDType_NameQualifier', pyxb.binding.datatypes.string)
    __NameQualifier._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 30, 8)
    __NameQualifier._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 30, 8)
    
    NameQualifier = property(__NameQualifier.value, __NameQualifier.set, None, None)

    
    # Attribute SPNameQualifier uses Python identifier SPNameQualifier
    __SPNameQualifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SPNameQualifier'), 'SPNameQualifier', '__urnoasisnamestcSAML2_0assertion_NameIDType_SPNameQualifier', pyxb.binding.datatypes.string)
    __SPNameQualifier._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 31, 8)
    __SPNameQualifier._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 31, 8)
    
    SPNameQualifier = property(__SPNameQualifier.value, __SPNameQualifier.set, None, None)

    
    # Attribute Format uses Python identifier Format
    __Format = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Format'), 'Format', '__urnoasisnamestcSAML2_0assertion_NameIDType_Format', pyxb.binding.datatypes.anyURI)
    __Format._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 42, 16)
    __Format._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 42, 16)
    
    Format = property(__Format.value, __Format.set, None, None)

    
    # Attribute SPProvidedID uses Python identifier SPProvidedID
    __SPProvidedID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SPProvidedID'), 'SPProvidedID', '__urnoasisnamestcSAML2_0assertion_NameIDType_SPProvidedID', pyxb.binding.datatypes.string)
    __SPProvidedID._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 43, 16)
    __SPProvidedID._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 43, 16)
    
    SPProvidedID = property(__SPProvidedID.value, __SPProvidedID.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __NameQualifier.name() : __NameQualifier,
        __SPNameQualifier.name() : __SPNameQualifier,
        __Format.name() : __Format,
        __SPProvidedID.name() : __SPProvidedID
    }
Namespace.addCategoryObject('typeBinding', u'NameIDType', NameIDType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedElementType with content type ELEMENT_ONLY
class EncryptedElementType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedElementType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'EncryptedElementType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 47, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3.org/2001/04/xmlenc#}EncryptedData uses Python identifier EncryptedData
    __EncryptedData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2001/04/xmlenc#'), u'EncryptedData'), 'EncryptedData', '__urnoasisnamestcSAML2_0assertion_EncryptedElementType_httpwww_w3_org200104xmlencEncryptedData', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/xenc.xsd', 72, 2), )

    
    EncryptedData = property(__EncryptedData.value, __EncryptedData.set, None, None)

    
    # Element {http://www.w3.org/2001/04/xmlenc#}EncryptedKey uses Python identifier EncryptedKey
    __EncryptedKey = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2001/04/xmlenc#'), u'EncryptedKey'), 'EncryptedKey', '__urnoasisnamestcSAML2_0assertion_EncryptedElementType_httpwww_w3_org200104xmlencEncryptedKey', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/xenc.xsd', 82, 2), )

    
    EncryptedKey = property(__EncryptedKey.value, __EncryptedKey.set, None, None)


    _ElementMap = {
        __EncryptedData.name() : __EncryptedData,
        __EncryptedKey.name() : __EncryptedKey
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'EncryptedElementType', EncryptedElementType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AssertionType with content type ELEMENT_ONLY
class AssertionType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AssertionType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AssertionType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 58, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature'), 'Signature', '__urnoasisnamestcSAML2_0assertion_AssertionType_httpwww_w3_org200009xmldsigSignature', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/ds.xsd', 43, 0), )

    
    Signature = property(__Signature.value, __Signature.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Issuer uses Python identifier Issuer
    __Issuer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Issuer'), 'Issuer', '__urnoasisnamestcSAML2_0assertion_AssertionType_urnoasisnamestcSAML2_0assertionIssuer', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 54, 4), )

    
    Issuer = property(__Issuer.value, __Issuer.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Subject uses Python identifier Subject
    __Subject = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Subject'), 'Subject', '__urnoasisnamestcSAML2_0assertion_AssertionType_urnoasisnamestcSAML2_0assertionSubject', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 76, 4), )

    
    Subject = property(__Subject.value, __Subject.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Conditions uses Python identifier Conditions
    __Conditions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Conditions'), 'Conditions', '__urnoasisnamestcSAML2_0assertion_AssertionType_urnoasisnamestcSAML2_0assertionConditions', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 127, 4), )

    
    Conditions = property(__Conditions.value, __Conditions.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Advice uses Python identifier Advice
    __Advice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Advice'), 'Advice', '__urnoasisnamestcSAML2_0assertion_AssertionType_urnoasisnamestcSAML2_0assertionAdvice', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 168, 4), )

    
    Advice = property(__Advice.value, __Advice.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Statement uses Python identifier Statement
    __Statement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Statement'), 'Statement', '__urnoasisnamestcSAML2_0assertion_AssertionType_urnoasisnamestcSAML2_0assertionStatement', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 179, 4), )

    
    Statement = property(__Statement.value, __Statement.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AuthnStatement uses Python identifier AuthnStatement
    __AuthnStatement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AuthnStatement'), 'AuthnStatement', '__urnoasisnamestcSAML2_0assertion_AssertionType_urnoasisnamestcSAML2_0assertionAuthnStatement', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 181, 4), )

    
    AuthnStatement = property(__AuthnStatement.value, __AuthnStatement.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AuthzDecisionStatement uses Python identifier AuthzDecisionStatement
    __AuthzDecisionStatement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AuthzDecisionStatement'), 'AuthzDecisionStatement', '__urnoasisnamestcSAML2_0assertion_AssertionType_urnoasisnamestcSAML2_0assertionAuthzDecisionStatement', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 223, 4), )

    
    AuthzDecisionStatement = property(__AuthzDecisionStatement.value, __AuthzDecisionStatement.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AttributeStatement uses Python identifier AttributeStatement
    __AttributeStatement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AttributeStatement'), 'AttributeStatement', '__urnoasisnamestcSAML2_0assertion_AssertionType_urnoasisnamestcSAML2_0assertionAttributeStatement', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 260, 4), )

    
    AttributeStatement = property(__AttributeStatement.value, __AttributeStatement.set, None, None)

    
    # Attribute Version uses Python identifier Version
    __Version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Version'), 'Version', '__urnoasisnamestcSAML2_0assertion_AssertionType_Version', pyxb.binding.datatypes.string, required=True)
    __Version._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 72, 8)
    __Version._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 72, 8)
    
    Version = property(__Version.value, __Version.set, None, None)

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__urnoasisnamestcSAML2_0assertion_AssertionType_ID', pyxb.binding.datatypes.ID, required=True)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 73, 8)
    __ID._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 73, 8)
    
    ID = property(__ID.value, __ID.set, None, None)

    
    # Attribute IssueInstant uses Python identifier IssueInstant
    __IssueInstant = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'IssueInstant'), 'IssueInstant', '__urnoasisnamestcSAML2_0assertion_AssertionType_IssueInstant', pyxb.binding.datatypes.dateTime, required=True)
    __IssueInstant._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 74, 8)
    __IssueInstant._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 74, 8)
    
    IssueInstant = property(__IssueInstant.value, __IssueInstant.set, None, None)


    _ElementMap = {
        __Signature.name() : __Signature,
        __Issuer.name() : __Issuer,
        __Subject.name() : __Subject,
        __Conditions.name() : __Conditions,
        __Advice.name() : __Advice,
        __Statement.name() : __Statement,
        __AuthnStatement.name() : __AuthnStatement,
        __AuthzDecisionStatement.name() : __AuthzDecisionStatement,
        __AttributeStatement.name() : __AttributeStatement
    }
    _AttributeMap = {
        __Version.name() : __Version,
        __ID.name() : __ID,
        __IssueInstant.name() : __IssueInstant
    }
Namespace.addCategoryObject('typeBinding', u'AssertionType', AssertionType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}SubjectType with content type ELEMENT_ONLY
class SubjectType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}SubjectType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SubjectType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 77, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}BaseID uses Python identifier BaseID
    __BaseID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'BaseID'), 'BaseID', '__urnoasisnamestcSAML2_0assertion_SubjectType_urnoasisnamestcSAML2_0assertionBaseID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 33, 4), )

    
    BaseID = property(__BaseID.value, __BaseID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}NameID uses Python identifier NameID
    __NameID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'NameID'), 'NameID', '__urnoasisnamestcSAML2_0assertion_SubjectType_urnoasisnamestcSAML2_0assertionNameID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4), )

    
    NameID = property(__NameID.value, __NameID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedID uses Python identifier EncryptedID
    __EncryptedID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'EncryptedID'), 'EncryptedID', '__urnoasisnamestcSAML2_0assertion_SubjectType_urnoasisnamestcSAML2_0assertionEncryptedID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4), )

    
    EncryptedID = property(__EncryptedID.value, __EncryptedID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmation uses Python identifier SubjectConfirmation
    __SubjectConfirmation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmation'), 'SubjectConfirmation', '__urnoasisnamestcSAML2_0assertion_SubjectType_urnoasisnamestcSAML2_0assertionSubjectConfirmation', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 90, 4), )

    
    SubjectConfirmation = property(__SubjectConfirmation.value, __SubjectConfirmation.set, None, None)


    _ElementMap = {
        __BaseID.name() : __BaseID,
        __NameID.name() : __NameID,
        __EncryptedID.name() : __EncryptedID,
        __SubjectConfirmation.name() : __SubjectConfirmation
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SubjectType', SubjectType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmationType with content type ELEMENT_ONLY
class SubjectConfirmationType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmationType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmationType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 91, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}BaseID uses Python identifier BaseID
    __BaseID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'BaseID'), 'BaseID', '__urnoasisnamestcSAML2_0assertion_SubjectConfirmationType_urnoasisnamestcSAML2_0assertionBaseID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 33, 4), )

    
    BaseID = property(__BaseID.value, __BaseID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}NameID uses Python identifier NameID
    __NameID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'NameID'), 'NameID', '__urnoasisnamestcSAML2_0assertion_SubjectConfirmationType_urnoasisnamestcSAML2_0assertionNameID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4), )

    
    NameID = property(__NameID.value, __NameID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedID uses Python identifier EncryptedID
    __EncryptedID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'EncryptedID'), 'EncryptedID', '__urnoasisnamestcSAML2_0assertion_SubjectConfirmationType_urnoasisnamestcSAML2_0assertionEncryptedID', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4), )

    
    EncryptedID = property(__EncryptedID.value, __EncryptedID.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmationData uses Python identifier SubjectConfirmationData
    __SubjectConfirmationData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmationData'), 'SubjectConfirmationData', '__urnoasisnamestcSAML2_0assertion_SubjectConfirmationType_urnoasisnamestcSAML2_0assertionSubjectConfirmationData', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 102, 4), )

    
    SubjectConfirmationData = property(__SubjectConfirmationData.value, __SubjectConfirmationData.set, None, None)

    
    # Attribute Method uses Python identifier Method
    __Method = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Method'), 'Method', '__urnoasisnamestcSAML2_0assertion_SubjectConfirmationType_Method', pyxb.binding.datatypes.anyURI, required=True)
    __Method._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 100, 8)
    __Method._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 100, 8)
    
    Method = property(__Method.value, __Method.set, None, None)


    _ElementMap = {
        __BaseID.name() : __BaseID,
        __NameID.name() : __NameID,
        __EncryptedID.name() : __EncryptedID,
        __SubjectConfirmationData.name() : __SubjectConfirmationData
    }
    _AttributeMap = {
        __Method.name() : __Method
    }
Namespace.addCategoryObject('typeBinding', u'SubjectConfirmationType', SubjectConfirmationType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmationDataType with content type MIXED
class SubjectConfirmationDataType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmationDataType with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmationDataType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 103, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute NotBefore uses Python identifier NotBefore
    __NotBefore = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NotBefore'), 'NotBefore', '__urnoasisnamestcSAML2_0assertion_SubjectConfirmationDataType_NotBefore', pyxb.binding.datatypes.dateTime)
    __NotBefore._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 109, 16)
    __NotBefore._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 109, 16)
    
    NotBefore = property(__NotBefore.value, __NotBefore.set, None, None)

    
    # Attribute NotOnOrAfter uses Python identifier NotOnOrAfter
    __NotOnOrAfter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NotOnOrAfter'), 'NotOnOrAfter', '__urnoasisnamestcSAML2_0assertion_SubjectConfirmationDataType_NotOnOrAfter', pyxb.binding.datatypes.dateTime)
    __NotOnOrAfter._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 110, 16)
    __NotOnOrAfter._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 110, 16)
    
    NotOnOrAfter = property(__NotOnOrAfter.value, __NotOnOrAfter.set, None, None)

    
    # Attribute Recipient uses Python identifier Recipient
    __Recipient = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Recipient'), 'Recipient', '__urnoasisnamestcSAML2_0assertion_SubjectConfirmationDataType_Recipient', pyxb.binding.datatypes.anyURI)
    __Recipient._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 111, 16)
    __Recipient._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 111, 16)
    
    Recipient = property(__Recipient.value, __Recipient.set, None, None)

    
    # Attribute InResponseTo uses Python identifier InResponseTo
    __InResponseTo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'InResponseTo'), 'InResponseTo', '__urnoasisnamestcSAML2_0assertion_SubjectConfirmationDataType_InResponseTo', pyxb.binding.datatypes.NCName)
    __InResponseTo._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 112, 16)
    __InResponseTo._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 112, 16)
    
    InResponseTo = property(__InResponseTo.value, __InResponseTo.set, None, None)

    
    # Attribute Address uses Python identifier Address
    __Address = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Address'), 'Address', '__urnoasisnamestcSAML2_0assertion_SubjectConfirmationDataType_Address', pyxb.binding.datatypes.string)
    __Address._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 113, 16)
    __Address._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 113, 16)
    
    Address = property(__Address.value, __Address.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, u'urn:oasis:names:tc:SAML:2.0:assertion'))
    _HasWildcardElement = True

    _ElementMap = {
        
    }
    _AttributeMap = {
        __NotBefore.name() : __NotBefore,
        __NotOnOrAfter.name() : __NotOnOrAfter,
        __Recipient.name() : __Recipient,
        __InResponseTo.name() : __InResponseTo,
        __Address.name() : __Address
    }
Namespace.addCategoryObject('typeBinding', u'SubjectConfirmationDataType', SubjectConfirmationDataType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}ConditionsType with content type ELEMENT_ONLY
class ConditionsType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}ConditionsType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ConditionsType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 128, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Condition uses Python identifier Condition
    __Condition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Condition'), 'Condition', '__urnoasisnamestcSAML2_0assertion_ConditionsType_urnoasisnamestcSAML2_0assertionCondition', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 138, 4), )

    
    Condition = property(__Condition.value, __Condition.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AudienceRestriction uses Python identifier AudienceRestriction
    __AudienceRestriction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AudienceRestriction'), 'AudienceRestriction', '__urnoasisnamestcSAML2_0assertion_ConditionsType_urnoasisnamestcSAML2_0assertionAudienceRestriction', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 140, 4), )

    
    AudienceRestriction = property(__AudienceRestriction.value, __AudienceRestriction.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}OneTimeUse uses Python identifier OneTimeUse
    __OneTimeUse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'OneTimeUse'), 'OneTimeUse', '__urnoasisnamestcSAML2_0assertion_ConditionsType_urnoasisnamestcSAML2_0assertionOneTimeUse', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 151, 4), )

    
    OneTimeUse = property(__OneTimeUse.value, __OneTimeUse.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}ProxyRestriction uses Python identifier ProxyRestriction
    __ProxyRestriction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'ProxyRestriction'), 'ProxyRestriction', '__urnoasisnamestcSAML2_0assertion_ConditionsType_urnoasisnamestcSAML2_0assertionProxyRestriction', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 157, 4), )

    
    ProxyRestriction = property(__ProxyRestriction.value, __ProxyRestriction.set, None, None)

    
    # Attribute NotBefore uses Python identifier NotBefore
    __NotBefore = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NotBefore'), 'NotBefore', '__urnoasisnamestcSAML2_0assertion_ConditionsType_NotBefore', pyxb.binding.datatypes.dateTime)
    __NotBefore._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 135, 8)
    __NotBefore._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 135, 8)
    
    NotBefore = property(__NotBefore.value, __NotBefore.set, None, None)

    
    # Attribute NotOnOrAfter uses Python identifier NotOnOrAfter
    __NotOnOrAfter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NotOnOrAfter'), 'NotOnOrAfter', '__urnoasisnamestcSAML2_0assertion_ConditionsType_NotOnOrAfter', pyxb.binding.datatypes.dateTime)
    __NotOnOrAfter._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 136, 8)
    __NotOnOrAfter._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 136, 8)
    
    NotOnOrAfter = property(__NotOnOrAfter.value, __NotOnOrAfter.set, None, None)


    _ElementMap = {
        __Condition.name() : __Condition,
        __AudienceRestriction.name() : __AudienceRestriction,
        __OneTimeUse.name() : __OneTimeUse,
        __ProxyRestriction.name() : __ProxyRestriction
    }
    _AttributeMap = {
        __NotBefore.name() : __NotBefore,
        __NotOnOrAfter.name() : __NotOnOrAfter
    }
Namespace.addCategoryObject('typeBinding', u'ConditionsType', ConditionsType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}ConditionAbstractType with content type EMPTY
class ConditionAbstractType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}ConditionAbstractType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ConditionAbstractType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 139, 4)
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ConditionAbstractType', ConditionAbstractType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AdviceType with content type ELEMENT_ONLY
class AdviceType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AdviceType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AdviceType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 169, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AssertionIDRef uses Python identifier AssertionIDRef
    __AssertionIDRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AssertionIDRef'), 'AssertionIDRef', '__urnoasisnamestcSAML2_0assertion_AdviceType_urnoasisnamestcSAML2_0assertionAssertionIDRef', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 55, 4), )

    
    AssertionIDRef = property(__AssertionIDRef.value, __AssertionIDRef.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AssertionURIRef uses Python identifier AssertionURIRef
    __AssertionURIRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AssertionURIRef'), 'AssertionURIRef', '__urnoasisnamestcSAML2_0assertion_AdviceType_urnoasisnamestcSAML2_0assertionAssertionURIRef', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 56, 4), )

    
    AssertionURIRef = property(__AssertionURIRef.value, __AssertionURIRef.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Assertion uses Python identifier Assertion
    __Assertion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Assertion'), 'Assertion', '__urnoasisnamestcSAML2_0assertion_AdviceType_urnoasisnamestcSAML2_0assertionAssertion', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 57, 4), )

    
    Assertion = property(__Assertion.value, __Assertion.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedAssertion uses Python identifier EncryptedAssertion
    __EncryptedAssertion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAssertion'), 'EncryptedAssertion', '__urnoasisnamestcSAML2_0assertion_AdviceType_urnoasisnamestcSAML2_0assertionEncryptedAssertion', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 178, 4), )

    
    EncryptedAssertion = property(__EncryptedAssertion.value, __EncryptedAssertion.set, None, None)

    _HasWildcardElement = True

    _ElementMap = {
        __AssertionIDRef.name() : __AssertionIDRef,
        __AssertionURIRef.name() : __AssertionURIRef,
        __Assertion.name() : __Assertion,
        __EncryptedAssertion.name() : __EncryptedAssertion
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AdviceType', AdviceType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}StatementAbstractType with content type EMPTY
class StatementAbstractType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}StatementAbstractType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StatementAbstractType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 180, 4)
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'StatementAbstractType', StatementAbstractType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}SubjectLocalityType with content type EMPTY
class SubjectLocalityType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}SubjectLocalityType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SubjectLocalityType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 196, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute Address uses Python identifier Address
    __Address = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Address'), 'Address', '__urnoasisnamestcSAML2_0assertion_SubjectLocalityType_Address', pyxb.binding.datatypes.string)
    __Address._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 197, 8)
    __Address._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 197, 8)
    
    Address = property(__Address.value, __Address.set, None, None)

    
    # Attribute DNSName uses Python identifier DNSName
    __DNSName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'DNSName'), 'DNSName', '__urnoasisnamestcSAML2_0assertion_SubjectLocalityType_DNSName', pyxb.binding.datatypes.string)
    __DNSName._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 198, 8)
    __DNSName._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 198, 8)
    
    DNSName = property(__DNSName.value, __DNSName.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __Address.name() : __Address,
        __DNSName.name() : __DNSName
    }
Namespace.addCategoryObject('typeBinding', u'SubjectLocalityType', SubjectLocalityType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AuthnContextType with content type ELEMENT_ONLY
class AuthnContextType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AuthnContextType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AuthnContextType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 201, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AuthnContextClassRef uses Python identifier AuthnContextClassRef
    __AuthnContextClassRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextClassRef'), 'AuthnContextClassRef', '__urnoasisnamestcSAML2_0assertion_AuthnContextType_urnoasisnamestcSAML2_0assertionAuthnContextClassRef', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 219, 4), )

    
    AuthnContextClassRef = property(__AuthnContextClassRef.value, __AuthnContextClassRef.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AuthnContextDeclRef uses Python identifier AuthnContextDeclRef
    __AuthnContextDeclRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextDeclRef'), 'AuthnContextDeclRef', '__urnoasisnamestcSAML2_0assertion_AuthnContextType_urnoasisnamestcSAML2_0assertionAuthnContextDeclRef', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 220, 4), )

    
    AuthnContextDeclRef = property(__AuthnContextDeclRef.value, __AuthnContextDeclRef.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AuthnContextDecl uses Python identifier AuthnContextDecl
    __AuthnContextDecl = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextDecl'), 'AuthnContextDecl', '__urnoasisnamestcSAML2_0assertion_AuthnContextType_urnoasisnamestcSAML2_0assertionAuthnContextDecl', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 221, 4), )

    
    AuthnContextDecl = property(__AuthnContextDecl.value, __AuthnContextDecl.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AuthenticatingAuthority uses Python identifier AuthenticatingAuthority
    __AuthenticatingAuthority = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AuthenticatingAuthority'), 'AuthenticatingAuthority', '__urnoasisnamestcSAML2_0assertion_AuthnContextType_urnoasisnamestcSAML2_0assertionAuthenticatingAuthority', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 222, 4), )

    
    AuthenticatingAuthority = property(__AuthenticatingAuthority.value, __AuthenticatingAuthority.set, None, None)


    _ElementMap = {
        __AuthnContextClassRef.name() : __AuthnContextClassRef,
        __AuthnContextDeclRef.name() : __AuthnContextDeclRef,
        __AuthnContextDecl.name() : __AuthnContextDecl,
        __AuthenticatingAuthority.name() : __AuthenticatingAuthority
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AuthnContextType', AuthnContextType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}ActionType with content type SIMPLE
class ActionType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}ActionType with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ActionType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 244, 4)
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute Namespace uses Python identifier Namespace
    __Namespace = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Namespace'), 'Namespace', '__urnoasisnamestcSAML2_0assertion_ActionType_Namespace', pyxb.binding.datatypes.anyURI, required=True)
    __Namespace._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 247, 16)
    __Namespace._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 247, 16)
    
    Namespace = property(__Namespace.value, __Namespace.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __Namespace.name() : __Namespace
    }
Namespace.addCategoryObject('typeBinding', u'ActionType', ActionType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}EvidenceType with content type ELEMENT_ONLY
class EvidenceType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}EvidenceType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'EvidenceType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 252, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AssertionIDRef uses Python identifier AssertionIDRef
    __AssertionIDRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AssertionIDRef'), 'AssertionIDRef', '__urnoasisnamestcSAML2_0assertion_EvidenceType_urnoasisnamestcSAML2_0assertionAssertionIDRef', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 55, 4), )

    
    AssertionIDRef = property(__AssertionIDRef.value, __AssertionIDRef.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AssertionURIRef uses Python identifier AssertionURIRef
    __AssertionURIRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AssertionURIRef'), 'AssertionURIRef', '__urnoasisnamestcSAML2_0assertion_EvidenceType_urnoasisnamestcSAML2_0assertionAssertionURIRef', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 56, 4), )

    
    AssertionURIRef = property(__AssertionURIRef.value, __AssertionURIRef.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Assertion uses Python identifier Assertion
    __Assertion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Assertion'), 'Assertion', '__urnoasisnamestcSAML2_0assertion_EvidenceType_urnoasisnamestcSAML2_0assertionAssertion', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 57, 4), )

    
    Assertion = property(__Assertion.value, __Assertion.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedAssertion uses Python identifier EncryptedAssertion
    __EncryptedAssertion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAssertion'), 'EncryptedAssertion', '__urnoasisnamestcSAML2_0assertion_EvidenceType_urnoasisnamestcSAML2_0assertionEncryptedAssertion', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 178, 4), )

    
    EncryptedAssertion = property(__EncryptedAssertion.value, __EncryptedAssertion.set, None, None)


    _ElementMap = {
        __AssertionIDRef.name() : __AssertionIDRef,
        __AssertionURIRef.name() : __AssertionURIRef,
        __Assertion.name() : __Assertion,
        __EncryptedAssertion.name() : __EncryptedAssertion
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'EvidenceType', EvidenceType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AttributeType with content type ELEMENT_ONLY
class AttributeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AttributeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AttributeType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 272, 4)
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue uses Python identifier AttributeValue
    __AttributeValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AttributeValue'), 'AttributeValue', '__urnoasisnamestcSAML2_0assertion_AttributeType_urnoasisnamestcSAML2_0assertionAttributeValue', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 281, 4), )

    
    AttributeValue = property(__AttributeValue.value, __AttributeValue.set, None, None)

    
    # Attribute Name uses Python identifier Name
    __Name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Name'), 'Name', '__urnoasisnamestcSAML2_0assertion_AttributeType_Name', pyxb.binding.datatypes.string, required=True)
    __Name._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 276, 8)
    __Name._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 276, 8)
    
    Name = property(__Name.value, __Name.set, None, None)

    
    # Attribute NameFormat uses Python identifier NameFormat
    __NameFormat = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NameFormat'), 'NameFormat', '__urnoasisnamestcSAML2_0assertion_AttributeType_NameFormat', pyxb.binding.datatypes.anyURI)
    __NameFormat._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 277, 8)
    __NameFormat._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 277, 8)
    
    NameFormat = property(__NameFormat.value, __NameFormat.set, None, None)

    
    # Attribute FriendlyName uses Python identifier FriendlyName
    __FriendlyName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'FriendlyName'), 'FriendlyName', '__urnoasisnamestcSAML2_0assertion_AttributeType_FriendlyName', pyxb.binding.datatypes.string)
    __FriendlyName._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 278, 8)
    __FriendlyName._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 278, 8)
    
    FriendlyName = property(__FriendlyName.value, __FriendlyName.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, u'urn:oasis:names:tc:SAML:2.0:assertion'))

    _ElementMap = {
        __AttributeValue.name() : __AttributeValue
    }
    _AttributeMap = {
        __Name.name() : __Name,
        __NameFormat.name() : __NameFormat,
        __FriendlyName.name() : __FriendlyName
    }
Namespace.addCategoryObject('typeBinding', u'AttributeType', AttributeType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}KeyInfoConfirmationDataType with content type ELEMENT_ONLY
class KeyInfoConfirmationDataType (SubjectConfirmationDataType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}KeyInfoConfirmationDataType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'KeyInfoConfirmationDataType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 118, 4)
    # Base type is SubjectConfirmationDataType
    
    # Element {http://www.w3.org/2000/09/xmldsig#}KeyInfo uses Python identifier KeyInfo
    __KeyInfo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'KeyInfo'), 'KeyInfo', '__urnoasisnamestcSAML2_0assertion_KeyInfoConfirmationDataType_httpwww_w3_org200009xmldsigKeyInfo', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/ds.xsd', 144, 0), )

    
    KeyInfo = property(__KeyInfo.value, __KeyInfo.set, None, None)

    
    # Attribute NotBefore inherited from {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmationDataType
    
    # Attribute NotOnOrAfter inherited from {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmationDataType
    
    # Attribute Recipient inherited from {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmationDataType
    
    # Attribute InResponseTo inherited from {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmationDataType
    
    # Attribute Address inherited from {urn:oasis:names:tc:SAML:2.0:assertion}SubjectConfirmationDataType

    _ElementMap = SubjectConfirmationDataType._ElementMap.copy()
    _ElementMap.update({
        __KeyInfo.name() : __KeyInfo
    })
    _AttributeMap = SubjectConfirmationDataType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'KeyInfoConfirmationDataType', KeyInfoConfirmationDataType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AudienceRestrictionType with content type ELEMENT_ONLY
class AudienceRestrictionType (ConditionAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AudienceRestrictionType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AudienceRestrictionType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 141, 4)
    # Base type is ConditionAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Audience uses Python identifier Audience
    __Audience = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Audience'), 'Audience', '__urnoasisnamestcSAML2_0assertion_AudienceRestrictionType_urnoasisnamestcSAML2_0assertionAudience', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 150, 4), )

    
    Audience = property(__Audience.value, __Audience.set, None, None)


    _ElementMap = ConditionAbstractType._ElementMap.copy()
    _ElementMap.update({
        __Audience.name() : __Audience
    })
    _AttributeMap = ConditionAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AudienceRestrictionType', AudienceRestrictionType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}OneTimeUseType with content type EMPTY
class OneTimeUseType (ConditionAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}OneTimeUseType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'OneTimeUseType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 152, 4)
    # Base type is ConditionAbstractType

    _ElementMap = ConditionAbstractType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ConditionAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'OneTimeUseType', OneTimeUseType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}ProxyRestrictionType with content type ELEMENT_ONLY
class ProxyRestrictionType (ConditionAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}ProxyRestrictionType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ProxyRestrictionType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 158, 4)
    # Base type is ConditionAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Audience uses Python identifier Audience
    __Audience = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Audience'), 'Audience', '__urnoasisnamestcSAML2_0assertion_ProxyRestrictionType_urnoasisnamestcSAML2_0assertionAudience', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 150, 4), )

    
    Audience = property(__Audience.value, __Audience.set, None, None)

    
    # Attribute Count uses Python identifier Count
    __Count = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Count'), 'Count', '__urnoasisnamestcSAML2_0assertion_ProxyRestrictionType_Count', pyxb.binding.datatypes.nonNegativeInteger)
    __Count._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 164, 12)
    __Count._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 164, 12)
    
    Count = property(__Count.value, __Count.set, None, None)


    _ElementMap = ConditionAbstractType._ElementMap.copy()
    _ElementMap.update({
        __Audience.name() : __Audience
    })
    _AttributeMap = ConditionAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        __Count.name() : __Count
    })
Namespace.addCategoryObject('typeBinding', u'ProxyRestrictionType', ProxyRestrictionType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AuthnStatementType with content type ELEMENT_ONLY
class AuthnStatementType (StatementAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AuthnStatementType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AuthnStatementType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 182, 4)
    # Base type is StatementAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}SubjectLocality uses Python identifier SubjectLocality
    __SubjectLocality = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'SubjectLocality'), 'SubjectLocality', '__urnoasisnamestcSAML2_0assertion_AuthnStatementType_urnoasisnamestcSAML2_0assertionSubjectLocality', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 195, 4), )

    
    SubjectLocality = property(__SubjectLocality.value, __SubjectLocality.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}AuthnContext uses Python identifier AuthnContext
    __AuthnContext = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'AuthnContext'), 'AuthnContext', '__urnoasisnamestcSAML2_0assertion_AuthnStatementType_urnoasisnamestcSAML2_0assertionAuthnContext', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 200, 4), )

    
    AuthnContext = property(__AuthnContext.value, __AuthnContext.set, None, None)

    
    # Attribute AuthnInstant uses Python identifier AuthnInstant
    __AuthnInstant = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'AuthnInstant'), 'AuthnInstant', '__urnoasisnamestcSAML2_0assertion_AuthnStatementType_AuthnInstant', pyxb.binding.datatypes.dateTime, required=True)
    __AuthnInstant._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 189, 16)
    __AuthnInstant._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 189, 16)
    
    AuthnInstant = property(__AuthnInstant.value, __AuthnInstant.set, None, None)

    
    # Attribute SessionIndex uses Python identifier SessionIndex
    __SessionIndex = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SessionIndex'), 'SessionIndex', '__urnoasisnamestcSAML2_0assertion_AuthnStatementType_SessionIndex', pyxb.binding.datatypes.string)
    __SessionIndex._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 190, 16)
    __SessionIndex._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 190, 16)
    
    SessionIndex = property(__SessionIndex.value, __SessionIndex.set, None, None)

    
    # Attribute SessionNotOnOrAfter uses Python identifier SessionNotOnOrAfter
    __SessionNotOnOrAfter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'SessionNotOnOrAfter'), 'SessionNotOnOrAfter', '__urnoasisnamestcSAML2_0assertion_AuthnStatementType_SessionNotOnOrAfter', pyxb.binding.datatypes.dateTime)
    __SessionNotOnOrAfter._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 191, 16)
    __SessionNotOnOrAfter._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 191, 16)
    
    SessionNotOnOrAfter = property(__SessionNotOnOrAfter.value, __SessionNotOnOrAfter.set, None, None)


    _ElementMap = StatementAbstractType._ElementMap.copy()
    _ElementMap.update({
        __SubjectLocality.name() : __SubjectLocality,
        __AuthnContext.name() : __AuthnContext
    })
    _AttributeMap = StatementAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        __AuthnInstant.name() : __AuthnInstant,
        __SessionIndex.name() : __SessionIndex,
        __SessionNotOnOrAfter.name() : __SessionNotOnOrAfter
    })
Namespace.addCategoryObject('typeBinding', u'AuthnStatementType', AuthnStatementType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AuthzDecisionStatementType with content type ELEMENT_ONLY
class AuthzDecisionStatementType (StatementAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AuthzDecisionStatementType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AuthzDecisionStatementType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 224, 4)
    # Base type is StatementAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Action uses Python identifier Action
    __Action = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Action'), 'Action', '__urnoasisnamestcSAML2_0assertion_AuthzDecisionStatementType_urnoasisnamestcSAML2_0assertionAction', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 243, 4), )

    
    Action = property(__Action.value, __Action.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Evidence uses Python identifier Evidence
    __Evidence = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Evidence'), 'Evidence', '__urnoasisnamestcSAML2_0assertion_AuthzDecisionStatementType_urnoasisnamestcSAML2_0assertionEvidence', False, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 251, 4), )

    
    Evidence = property(__Evidence.value, __Evidence.set, None, None)

    
    # Attribute Resource uses Python identifier Resource
    __Resource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Resource'), 'Resource', '__urnoasisnamestcSAML2_0assertion_AuthzDecisionStatementType_Resource', pyxb.binding.datatypes.anyURI, required=True)
    __Resource._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 231, 16)
    __Resource._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 231, 16)
    
    Resource = property(__Resource.value, __Resource.set, None, None)

    
    # Attribute Decision uses Python identifier Decision
    __Decision = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'Decision'), 'Decision', '__urnoasisnamestcSAML2_0assertion_AuthzDecisionStatementType_Decision', DecisionType, required=True)
    __Decision._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 232, 16)
    __Decision._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 232, 16)
    
    Decision = property(__Decision.value, __Decision.set, None, None)


    _ElementMap = StatementAbstractType._ElementMap.copy()
    _ElementMap.update({
        __Action.name() : __Action,
        __Evidence.name() : __Evidence
    })
    _AttributeMap = StatementAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        __Resource.name() : __Resource,
        __Decision.name() : __Decision
    })
Namespace.addCategoryObject('typeBinding', u'AuthzDecisionStatementType', AuthzDecisionStatementType)


# Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AttributeStatementType with content type ELEMENT_ONLY
class AttributeStatementType (StatementAbstractType):
    """Complex type {urn:oasis:names:tc:SAML:2.0:assertion}AttributeStatementType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AttributeStatementType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 261, 4)
    # Base type is StatementAbstractType
    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}Attribute uses Python identifier Attribute
    __Attribute = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'Attribute'), 'Attribute', '__urnoasisnamestcSAML2_0assertion_AttributeStatementType_urnoasisnamestcSAML2_0assertionAttribute', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 271, 4), )

    
    Attribute = property(__Attribute.value, __Attribute.set, None, None)

    
    # Element {urn:oasis:names:tc:SAML:2.0:assertion}EncryptedAttribute uses Python identifier EncryptedAttribute
    __EncryptedAttribute = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAttribute'), 'EncryptedAttribute', '__urnoasisnamestcSAML2_0assertion_AttributeStatementType_urnoasisnamestcSAML2_0assertionEncryptedAttribute', True, pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 282, 4), )

    
    EncryptedAttribute = property(__EncryptedAttribute.value, __EncryptedAttribute.set, None, None)


    _ElementMap = StatementAbstractType._ElementMap.copy()
    _ElementMap.update({
        __Attribute.name() : __Attribute,
        __EncryptedAttribute.name() : __EncryptedAttribute
    })
    _AttributeMap = StatementAbstractType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AttributeStatementType', AttributeStatementType)


AssertionIDRef = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AssertionIDRef'), pyxb.binding.datatypes.NCName, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 55, 4))
Namespace.addCategoryObject('elementBinding', AssertionIDRef.name().localName(), AssertionIDRef)

AssertionURIRef = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AssertionURIRef'), pyxb.binding.datatypes.anyURI, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 56, 4))
Namespace.addCategoryObject('elementBinding', AssertionURIRef.name().localName(), AssertionURIRef)

Audience = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Audience'), pyxb.binding.datatypes.anyURI, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 150, 4))
Namespace.addCategoryObject('elementBinding', Audience.name().localName(), Audience)

AuthnContextClassRef = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextClassRef'), pyxb.binding.datatypes.anyURI, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 219, 4))
Namespace.addCategoryObject('elementBinding', AuthnContextClassRef.name().localName(), AuthnContextClassRef)

AuthnContextDeclRef = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextDeclRef'), pyxb.binding.datatypes.anyURI, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 220, 4))
Namespace.addCategoryObject('elementBinding', AuthnContextDeclRef.name().localName(), AuthnContextDeclRef)

AuthnContextDecl = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextDecl'), pyxb.binding.datatypes.anyType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 221, 4))
Namespace.addCategoryObject('elementBinding', AuthnContextDecl.name().localName(), AuthnContextDecl)

AuthenticatingAuthority = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthenticatingAuthority'), pyxb.binding.datatypes.anyURI, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 222, 4))
Namespace.addCategoryObject('elementBinding', AuthenticatingAuthority.name().localName(), AuthenticatingAuthority)

AttributeValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AttributeValue'), pyxb.binding.datatypes.anyType, nillable=pyxb.binding.datatypes.boolean(1), location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 281, 4))
Namespace.addCategoryObject('elementBinding', AttributeValue.name().localName(), AttributeValue)

BaseID = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BaseID'), BaseIDAbstractType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 33, 4))
Namespace.addCategoryObject('elementBinding', BaseID.name().localName(), BaseID)

NameID = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NameID'), NameIDType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4))
Namespace.addCategoryObject('elementBinding', NameID.name().localName(), NameID)

EncryptedID = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EncryptedID'), EncryptedElementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4))
Namespace.addCategoryObject('elementBinding', EncryptedID.name().localName(), EncryptedID)

Issuer = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Issuer'), NameIDType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 54, 4))
Namespace.addCategoryObject('elementBinding', Issuer.name().localName(), Issuer)

Assertion = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Assertion'), AssertionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 57, 4))
Namespace.addCategoryObject('elementBinding', Assertion.name().localName(), Assertion)

Subject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Subject'), SubjectType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 76, 4))
Namespace.addCategoryObject('elementBinding', Subject.name().localName(), Subject)

SubjectConfirmation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmation'), SubjectConfirmationType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 90, 4))
Namespace.addCategoryObject('elementBinding', SubjectConfirmation.name().localName(), SubjectConfirmation)

SubjectConfirmationData = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmationData'), SubjectConfirmationDataType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 102, 4))
Namespace.addCategoryObject('elementBinding', SubjectConfirmationData.name().localName(), SubjectConfirmationData)

Conditions = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Conditions'), ConditionsType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 127, 4))
Namespace.addCategoryObject('elementBinding', Conditions.name().localName(), Conditions)

Condition = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Condition'), ConditionAbstractType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 138, 4))
Namespace.addCategoryObject('elementBinding', Condition.name().localName(), Condition)

Advice = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Advice'), AdviceType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 168, 4))
Namespace.addCategoryObject('elementBinding', Advice.name().localName(), Advice)

EncryptedAssertion = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAssertion'), EncryptedElementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 178, 4))
Namespace.addCategoryObject('elementBinding', EncryptedAssertion.name().localName(), EncryptedAssertion)

Statement = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Statement'), StatementAbstractType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 179, 4))
Namespace.addCategoryObject('elementBinding', Statement.name().localName(), Statement)

SubjectLocality = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SubjectLocality'), SubjectLocalityType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 195, 4))
Namespace.addCategoryObject('elementBinding', SubjectLocality.name().localName(), SubjectLocality)

AuthnContext = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnContext'), AuthnContextType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 200, 4))
Namespace.addCategoryObject('elementBinding', AuthnContext.name().localName(), AuthnContext)

Action = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Action'), ActionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 243, 4))
Namespace.addCategoryObject('elementBinding', Action.name().localName(), Action)

Evidence = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Evidence'), EvidenceType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 251, 4))
Namespace.addCategoryObject('elementBinding', Evidence.name().localName(), Evidence)

Attribute = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Attribute'), AttributeType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 271, 4))
Namespace.addCategoryObject('elementBinding', Attribute.name().localName(), Attribute)

EncryptedAttribute = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAttribute'), EncryptedElementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 282, 4))
Namespace.addCategoryObject('elementBinding', EncryptedAttribute.name().localName(), EncryptedAttribute)

AudienceRestriction = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AudienceRestriction'), AudienceRestrictionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 140, 4))
Namespace.addCategoryObject('elementBinding', AudienceRestriction.name().localName(), AudienceRestriction)

OneTimeUse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OneTimeUse'), OneTimeUseType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 151, 4))
Namespace.addCategoryObject('elementBinding', OneTimeUse.name().localName(), OneTimeUse)

ProxyRestriction = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ProxyRestriction'), ProxyRestrictionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 157, 4))
Namespace.addCategoryObject('elementBinding', ProxyRestriction.name().localName(), ProxyRestriction)

AuthnStatement = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnStatement'), AuthnStatementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 181, 4))
Namespace.addCategoryObject('elementBinding', AuthnStatement.name().localName(), AuthnStatement)

AuthzDecisionStatement = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthzDecisionStatement'), AuthzDecisionStatementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 223, 4))
Namespace.addCategoryObject('elementBinding', AuthzDecisionStatement.name().localName(), AuthzDecisionStatement)

AttributeStatement = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AttributeStatement'), AttributeStatementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 260, 4))
Namespace.addCategoryObject('elementBinding', AttributeStatement.name().localName(), AttributeStatement)



EncryptedElementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2001/04/xmlenc#'), u'EncryptedData'), pyxb.bundles.wssplat.xenc.EncryptedDataType, scope=EncryptedElementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/xenc.xsd', 72, 2)))

EncryptedElementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2001/04/xmlenc#'), u'EncryptedKey'), pyxb.bundles.wssplat.xenc.EncryptedKeyType, scope=EncryptedElementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/xenc.xsd', 82, 2)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 50, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(EncryptedElementType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2001/04/xmlenc#'), u'EncryptedData')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 49, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(EncryptedElementType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2001/04/xmlenc#'), u'EncryptedKey')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 50, 12))
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
EncryptedElementType._Automaton = _BuildAutomaton()




AssertionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature'), pyxb.bundles.wssplat.ds.SignatureType, scope=AssertionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/ds.xsd', 43, 0)))

AssertionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Issuer'), NameIDType, scope=AssertionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 54, 4)))

AssertionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Subject'), SubjectType, scope=AssertionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 76, 4)))

AssertionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Conditions'), ConditionsType, scope=AssertionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 127, 4)))

AssertionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Advice'), AdviceType, scope=AssertionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 168, 4)))

AssertionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Statement'), StatementAbstractType, scope=AssertionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 179, 4)))

AssertionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnStatement'), AuthnStatementType, scope=AssertionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 181, 4)))

AssertionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthzDecisionStatement'), AuthzDecisionStatementType, scope=AssertionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 223, 4)))

AssertionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AttributeStatement'), AttributeStatementType, scope=AssertionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 260, 4)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 61, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 62, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 63, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 64, 12))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 65, 12))
    counters.add(cc_4)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AssertionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Issuer')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 60, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AssertionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'Signature')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 61, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(AssertionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Subject')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 62, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(AssertionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Conditions')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 63, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(AssertionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Advice')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 64, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(AssertionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Statement')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 66, 16))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(AssertionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AuthnStatement')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 67, 16))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(AssertionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AuthzDecisionStatement')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 68, 16))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(AssertionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AttributeStatement')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 69, 16))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
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
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
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
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AssertionType._Automaton = _BuildAutomaton_()




SubjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BaseID'), BaseIDAbstractType, scope=SubjectType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 33, 4)))

SubjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NameID'), NameIDType, scope=SubjectType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4)))

SubjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EncryptedID'), EncryptedElementType, scope=SubjectType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4)))

SubjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmation'), SubjectConfirmationType, scope=SubjectType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 90, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 85, 16))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SubjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'BaseID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 81, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SubjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'NameID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 82, 20))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SubjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'EncryptedID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 83, 20))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmation')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 85, 16))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(SubjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmation')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 87, 12))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
SubjectType._Automaton = _BuildAutomaton_2()




SubjectConfirmationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BaseID'), BaseIDAbstractType, scope=SubjectConfirmationType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 33, 4)))

SubjectConfirmationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NameID'), NameIDType, scope=SubjectConfirmationType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 37, 4)))

SubjectConfirmationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EncryptedID'), EncryptedElementType, scope=SubjectConfirmationType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 53, 4)))

SubjectConfirmationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmationData'), SubjectConfirmationDataType, scope=SubjectConfirmationType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 102, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 93, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 98, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubjectConfirmationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'BaseID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 94, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubjectConfirmationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'NameID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 95, 16))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SubjectConfirmationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'EncryptedID')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 96, 16))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(SubjectConfirmationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SubjectConfirmationData')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 98, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SubjectConfirmationType._Automaton = _BuildAutomaton_3()




def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 107, 20))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 107, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SubjectConfirmationDataType._Automaton = _BuildAutomaton_4()




ConditionsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Condition'), ConditionAbstractType, scope=ConditionsType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 138, 4)))

ConditionsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AudienceRestriction'), AudienceRestrictionType, scope=ConditionsType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 140, 4)))

ConditionsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OneTimeUse'), OneTimeUseType, scope=ConditionsType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 151, 4)))

ConditionsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ProxyRestriction'), ProxyRestrictionType, scope=ConditionsType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 157, 4)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 129, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ConditionsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Condition')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 130, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ConditionsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AudienceRestriction')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 131, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ConditionsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'OneTimeUse')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 132, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ConditionsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ProxyRestriction')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 133, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ConditionsType._Automaton = _BuildAutomaton_5()




AdviceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AssertionIDRef'), pyxb.binding.datatypes.NCName, scope=AdviceType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 55, 4)))

AdviceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AssertionURIRef'), pyxb.binding.datatypes.anyURI, scope=AdviceType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 56, 4)))

AdviceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Assertion'), AssertionType, scope=AdviceType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 57, 4)))

AdviceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAssertion'), EncryptedElementType, scope=AdviceType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 178, 4)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 170, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AdviceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AssertionIDRef')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 171, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AdviceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AssertionURIRef')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 172, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AdviceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Assertion')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 173, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AdviceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAssertion')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 174, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, u'urn:oasis:names:tc:SAML:2.0:assertion')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 175, 12))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
AdviceType._Automaton = _BuildAutomaton_6()




AuthnContextType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextClassRef'), pyxb.binding.datatypes.anyURI, scope=AuthnContextType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 219, 4)))

AuthnContextType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextDeclRef'), pyxb.binding.datatypes.anyURI, scope=AuthnContextType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 220, 4)))

AuthnContextType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextDecl'), pyxb.binding.datatypes.anyType, scope=AuthnContextType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 221, 4)))

AuthnContextType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthenticatingAuthority'), pyxb.binding.datatypes.anyURI, scope=AuthnContextType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 222, 4)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 206, 20))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 216, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AuthnContextType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextClassRef')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 205, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AuthnContextType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextDecl')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 207, 24))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AuthnContextType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextDeclRef')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 208, 24))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AuthnContextType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextDecl')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 212, 20))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AuthnContextType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AuthnContextDeclRef')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 213, 20))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(AuthnContextType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AuthenticatingAuthority')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 216, 12))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AuthnContextType._Automaton = _BuildAutomaton_7()




EvidenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AssertionIDRef'), pyxb.binding.datatypes.NCName, scope=EvidenceType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 55, 4)))

EvidenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AssertionURIRef'), pyxb.binding.datatypes.anyURI, scope=EvidenceType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 56, 4)))

EvidenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Assertion'), AssertionType, scope=EvidenceType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 57, 4)))

EvidenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAssertion'), EncryptedElementType, scope=EvidenceType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 178, 4)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(EvidenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AssertionIDRef')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 254, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(EvidenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AssertionURIRef')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 255, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(EvidenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Assertion')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 256, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(EvidenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAssertion')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 257, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
EvidenceType._Automaton = _BuildAutomaton_8()




AttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AttributeValue'), pyxb.binding.datatypes.anyType, nillable=pyxb.binding.datatypes.boolean(1), scope=AttributeType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 281, 4)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 274, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AttributeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AttributeValue')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 274, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
AttributeType._Automaton = _BuildAutomaton_9()




KeyInfoConfirmationDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'KeyInfo'), pyxb.bundles.wssplat.ds.KeyInfoType, scope=KeyInfoConfirmationDataType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/wssplat/schemas/ds.xsd', 144, 0)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(KeyInfoConfirmationDataType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2000/09/xmldsig#'), u'KeyInfo')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 122, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
KeyInfoConfirmationDataType._Automaton = _BuildAutomaton_10()




AudienceRestrictionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Audience'), pyxb.binding.datatypes.anyURI, scope=AudienceRestrictionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 150, 4)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AudienceRestrictionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Audience')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 145, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AudienceRestrictionType._Automaton = _BuildAutomaton_11()




ProxyRestrictionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Audience'), pyxb.binding.datatypes.anyURI, scope=ProxyRestrictionType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 150, 4)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=None, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 162, 16))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ProxyRestrictionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Audience')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 162, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ProxyRestrictionType._Automaton = _BuildAutomaton_12()




AuthnStatementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SubjectLocality'), SubjectLocalityType, scope=AuthnStatementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 195, 4)))

AuthnStatementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AuthnContext'), AuthnContextType, scope=AuthnStatementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 200, 4)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 186, 20))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AuthnStatementType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SubjectLocality')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 186, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AuthnStatementType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AuthnContext')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 187, 20))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AuthnStatementType._Automaton = _BuildAutomaton_13()




AuthzDecisionStatementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Action'), ActionType, scope=AuthzDecisionStatementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 243, 4)))

AuthzDecisionStatementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Evidence'), EvidenceType, scope=AuthzDecisionStatementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 251, 4)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 229, 20))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AuthzDecisionStatementType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Action')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 228, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AuthzDecisionStatementType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Evidence')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 229, 20))
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
AuthzDecisionStatementType._Automaton = _BuildAutomaton_14()




AttributeStatementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Attribute'), AttributeType, scope=AttributeStatementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 271, 4)))

AttributeStatementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAttribute'), EncryptedElementType, scope=AttributeStatementType, location=pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 282, 4)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it's invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AttributeStatementType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Attribute')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 265, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AttributeStatementType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'EncryptedAttribute')), pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/assertion.xsd', 266, 20))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AttributeStatementType._Automaton = _BuildAutomaton_15()

