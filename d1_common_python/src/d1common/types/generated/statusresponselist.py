# ./pyxb/statusresponselist.py
# PyXB bindings for NamespaceModule
# NSM:d63af8e216143d5eec0988eda9c8e00a33d17d07
# Generated 2010-09-08 11:58:31.805498 by PyXB version 1.1.2
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:b0f5de20-bb72-11df-8809-000c29f765e9')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import _common

Namespace = pyxb.namespace.NamespaceForURI(u'http://dataone.org/service/types/ComponentList/0.1', create_if_missing=True)
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


# Complex type ComponentList with content type ELEMENT_ONLY
class ComponentList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ComponentList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Component uses Python identifier Component
    __Component = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Component'), 'Component', '__httpdataone_orgservicetypesComponentList0_1_ComponentList_Component', False)

    
    Component = property(__Component.value, __Component.set, None, None)


    _ElementMap = {
        __Component.name() : __Component
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ComponentList', ComponentList)


# Complex type CTD_ANON with content type EMPTY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpdataone_orgservicetypesComponentList0_1_CTD_ANON_version', _common.ComponentVersion, required=True)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpdataone_orgservicetypesComponentList0_1_CTD_ANON_name', _common.ComponentName, required=True)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __version.name() : __version,
        __name.name() : __name
    }



componentList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'componentList'), ComponentList)
Namespace.addCategoryObject('elementBinding', componentList.name().localName(), componentList)



ComponentList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Component'), CTD_ANON, scope=ComponentList))
ComponentList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ComponentList._UseForTag(pyxb.namespace.ExpandedName(None, u'Component')), min_occurs=1, max_occurs=1)
    )
ComponentList._ContentModel = pyxb.binding.content.ParticleModel(ComponentList._GroupModel, min_occurs=1, max_occurs=1)
