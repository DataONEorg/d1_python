# ./generated/gmn_types.py
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2012-03-13 11:16:30.065415 by PyXB version 1.1.3
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:46239026-6d30-11e1-bd08-000c294230b4')

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
    
    # Element timestamp uses Python identifier timestamp
    __timestamp = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'timestamp'), 'timestamp', '__AbsentNamespace0_CTD_ANON_timestamp', False)

    
    timestamp = property(__timestamp.value, __timestamp.set, None, None)

    
    # Element taskId uses Python identifier taskId
    __taskId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'taskId'), 'taskId', '__AbsentNamespace0_CTD_ANON_taskId', False)

    
    taskId = property(__taskId.value, __taskId.set, None, None)

    
    # Element pid uses Python identifier pid
    __pid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'pid'), 'pid', '__AbsentNamespace0_CTD_ANON_pid', False)

    
    pid = property(__pid.value, __pid.set, None, None)

    
    # Element sourceNode uses Python identifier sourceNode
    __sourceNode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'sourceNode'), 'sourceNode', '__AbsentNamespace0_CTD_ANON_sourceNode', False)

    
    sourceNode = property(__sourceNode.value, __sourceNode.set, None, None)

    
    # Element status uses Python identifier status
    __status = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'status'), 'status', '__AbsentNamespace0_CTD_ANON_status', False)

    
    status = property(__status.value, __status.set, None, None)


    _ElementMap = {
        __timestamp.name() : __timestamp,
        __taskId.name() : __taskId,
        __pid.name() : __pid,
        __sourceNode.name() : __sourceNode,
        __status.name() : __status
    }
    _AttributeMap = {
        
    }



replicationRequest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'replicationRequest'), CTD_ANON)
Namespace.addCategoryObject('elementBinding', replicationRequest.name().localName(), replicationRequest)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'timestamp'), pyxb.binding.datatypes.dateTime, scope=CTD_ANON))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'taskId'), pyxb.binding.datatypes.unsignedLong, scope=CTD_ANON))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'pid'), pyxb.binding.datatypes.string, scope=CTD_ANON))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'sourceNode'), pyxb.binding.datatypes.string, scope=CTD_ANON))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'status'), pyxb.binding.datatypes.string, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'taskId')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'status')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'pid')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'sourceNode')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'timestamp')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)
