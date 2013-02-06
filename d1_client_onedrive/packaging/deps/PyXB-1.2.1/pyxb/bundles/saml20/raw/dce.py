# ./pyxb/bundles/saml20/raw/dce.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:f6fa0461f265c04a0bd0017089ca6057a2aade76
# Generated 2012-12-17 13:09:32.538512 by PyXB version 1.2.1
# Namespace urn:oasis:names:tc:SAML:2.0:profiles:attribute:DCE

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:4a10cdba-487d-11e2-94aa-c8600024e903')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'urn:oasis:names:tc:SAML:2.0:profiles:attribute:DCE', create_if_missing=True)
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


# Complex type {urn:oasis:names:tc:SAML:2.0:profiles:attribute:DCE}DCEValueType with content type SIMPLE
class DCEValueType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:oasis:names:tc:SAML:2.0:profiles:attribute:DCE}DCEValueType with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.anyURI
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DCEValueType')
    _XSDLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/dce.xsd', 18, 4)
    # Base type is pyxb.binding.datatypes.anyURI
    
    # Attribute {urn:oasis:names:tc:SAML:2.0:profiles:attribute:DCE}Realm uses Python identifier Realm
    __Realm = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'Realm'), 'Realm', '__urnoasisnamestcSAML2_0profilesattributeDCE_DCEValueType_urnoasisnamestcSAML2_0profilesattributeDCERealm', pyxb.binding.datatypes.anyURI)
    __Realm._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/dce.xsd', 26, 4)
    __Realm._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/dce.xsd', 21, 16)
    
    Realm = property(__Realm.value, __Realm.set, None, None)

    
    # Attribute {urn:oasis:names:tc:SAML:2.0:profiles:attribute:DCE}FriendlyName uses Python identifier FriendlyName
    __FriendlyName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'FriendlyName'), 'FriendlyName', '__urnoasisnamestcSAML2_0profilesattributeDCE_DCEValueType_urnoasisnamestcSAML2_0profilesattributeDCEFriendlyName', pyxb.binding.datatypes.string)
    __FriendlyName._DeclarationLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/dce.xsd', 27, 4)
    __FriendlyName._UseLocation = pyxb.utils.utility.Location('/tmp/pyxbdist.gTSiuHf/PyXB-1.2.1/pyxb/bundles/saml20/schemas/dce.xsd', 22, 16)
    
    FriendlyName = property(__FriendlyName.value, __FriendlyName.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __Realm.name() : __Realm,
        __FriendlyName.name() : __FriendlyName
    }
Namespace.addCategoryObject('typeBinding', u'DCEValueType', DCEValueType)

