# ./d1_common/types/generated/dataoneTypes_v1_1.py
# PyXB bindings for NM:360f646bcacd4796da7a71be6ffd7cac7a35ff8a
# Generated 2012-12-09 17:42:37.208572 by PyXB version 1.1.3
# Namespace http://ns.dataone.org/service/types/v1.1

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:7dd5c126-4262-11e2-b43a-000c294230b4')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import _d1

Namespace = pyxb.namespace.NamespaceForURI(u'http://ns.dataone.org/service/types/v1.1', create_if_missing=True)
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


# Complex type QueryField with content type ELEMENT_ONLY
class QueryField (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'QueryField')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesv1_1_QueryField_name', False)

    
    name = property(__name.value, __name.set, None, u'The name of the field as used programmatically when \n            constructing queries or other rferences to the field.')

    
    # Element multivalued uses Python identifier multivalued
    __multivalued = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'multivalued'), 'multivalued', '__httpns_dataone_orgservicetypesv1_1_QueryField_multivalued', False)

    
    multivalued = property(__multivalued.value, __multivalued.set, None, u'Indicates if the field may contain multiple values. Some query engines\n          such as SOLR support this capability.')

    
    # Element type uses Python identifier type
    __type = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'type'), 'type', '__httpns_dataone_orgservicetypesv1_1_QueryField_type', False)

    
    type = property(__type.value, __type.set, None, u'The type of the field, expressed in the language peculiar to the \n          query engine being described.')

    
    # Element sortable uses Python identifier sortable
    __sortable = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'sortable'), 'sortable', '__httpns_dataone_orgservicetypesv1_1_QueryField_sortable', False)

    
    sortable = property(__sortable.value, __sortable.set, None, u'Indicates if the field can be used for sorting results.')

    
    # Element searchable uses Python identifier searchable
    __searchable = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'searchable'), 'searchable', '__httpns_dataone_orgservicetypesv1_1_QueryField_searchable', False)

    
    searchable = property(__searchable.value, __searchable.set, None, u'Indicates if the field may be used in constructing queries (as opposed \n            to only appearing in results)')

    
    # Element returnable uses Python identifier returnable
    __returnable = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'returnable'), 'returnable', '__httpns_dataone_orgservicetypesv1_1_QueryField_returnable', False)

    
    returnable = property(__returnable.value, __returnable.set, None, u'Indicates if the field values may be returned in search results.')

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__httpns_dataone_orgservicetypesv1_1_QueryField_description', True)

    
    description = property(__description.value, __description.set, None, u'An optional, repeatable, brief description of the field that can be\n          used to help guide developers or end users in appropriate use of the field. May for \n          example, contain a links to additional documentation.')


    _ElementMap = {
        __name.name() : __name,
        __multivalued.name() : __multivalued,
        __type.name() : __type,
        __sortable.name() : __sortable,
        __searchable.name() : __searchable,
        __returnable.name() : __returnable,
        __description.name() : __description
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'QueryField', QueryField)


# Complex type QueryEngineDescription with content type ELEMENT_ONLY
class QueryEngineDescription (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'QueryEngineDescription')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element queryField uses Python identifier queryField
    __queryField = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'queryField'), 'queryField', '__httpns_dataone_orgservicetypesv1_1_QueryEngineDescription_queryField', True)

    
    queryField = property(__queryField.value, __queryField.set, None, u'A list of query fields supported by the query engine.')

    
    # Element queryEngineVersion uses Python identifier queryEngineVersion
    __queryEngineVersion = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'queryEngineVersion'), 'queryEngineVersion', '__httpns_dataone_orgservicetypesv1_1_QueryEngineDescription_queryEngineVersion', False)

    
    queryEngineVersion = property(__queryEngineVersion.value, __queryEngineVersion.set, None, u'The version of the underlying query engine. Used by clients to determine possible\n          compatibility concerns or features available.')

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpns_dataone_orgservicetypesv1_1_QueryEngineDescription_name', False)

    
    name = property(__name.value, __name.set, None, u'The full, human readable name of the query engine. For example: \n            "Apache SOLR"')

    
    # Element querySchemaVersion uses Python identifier querySchemaVersion
    __querySchemaVersion = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'querySchemaVersion'), 'querySchemaVersion', '__httpns_dataone_orgservicetypesv1_1_QueryEngineDescription_querySchemaVersion', False)

    
    querySchemaVersion = property(__querySchemaVersion.value, __querySchemaVersion.set, None, u'Version of the schema in use by the query engine, e.g. "1.0.1"')

    
    # Element additionalInfo uses Python identifier additionalInfo
    __additionalInfo = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'additionalInfo'), 'additionalInfo', '__httpns_dataone_orgservicetypesv1_1_QueryEngineDescription_additionalInfo', True)

    
    additionalInfo = property(__additionalInfo.value, __additionalInfo.set, None, u'An optional human readable description of the query engine. This can be \n            used to describe any special capabilities or intended uses for the query engine. For example, \n            a query engine may be tuned to suit a particular audience or domain as opposed to providing \n            a general purpose discovery mechanism.This field may also contain links to additional information about the query engine, \n          such as documentation for the search syntax provided by the query engine implemntors.')


    _ElementMap = {
        __queryField.name() : __queryField,
        __queryEngineVersion.name() : __queryEngineVersion,
        __name.name() : __name,
        __querySchemaVersion.name() : __querySchemaVersion,
        __additionalInfo.name() : __additionalInfo
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'QueryEngineDescription', QueryEngineDescription)


# Complex type QueryEngineList with content type ELEMENT_ONLY
class QueryEngineList (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'QueryEngineList')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element queryEngine uses Python identifier queryEngine
    __queryEngine = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'queryEngine'), 'queryEngine', '__httpns_dataone_orgservicetypesv1_1_QueryEngineList_queryEngine', True)

    
    queryEngine = property(__queryEngine.value, __queryEngine.set, None, u'The name of a queryEngine. This value will be used as a path element in \n            REST API calls and so should not contain characters that will need to be escaped.')


    _ElementMap = {
        __queryEngine.name() : __queryEngine
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'QueryEngineList', QueryEngineList)


queryEngineDescription = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'queryEngineDescription'), QueryEngineDescription)
Namespace.addCategoryObject('elementBinding', queryEngineDescription.name().localName(), queryEngineDescription)

queryEngineList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'queryEngineList'), QueryEngineList)
Namespace.addCategoryObject('elementBinding', queryEngineList.name().localName(), queryEngineList)



QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), _d1.NonEmptyString, scope=QueryField, documentation=u'The name of the field as used programmatically when \n            constructing queries or other rferences to the field.'))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'multivalued'), pyxb.binding.datatypes.boolean, scope=QueryField, documentation=u'Indicates if the field may contain multiple values. Some query engines\n          such as SOLR support this capability.'))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'type'), _d1.NonEmptyString, scope=QueryField, documentation=u'The type of the field, expressed in the language peculiar to the \n          query engine being described.'))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'sortable'), pyxb.binding.datatypes.boolean, scope=QueryField, documentation=u'Indicates if the field can be used for sorting results.'))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'searchable'), pyxb.binding.datatypes.boolean, scope=QueryField, documentation=u'Indicates if the field may be used in constructing queries (as opposed \n            to only appearing in results)'))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'returnable'), pyxb.binding.datatypes.boolean, scope=QueryField, documentation=u'Indicates if the field values may be returned in search results.'))

QueryField._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'description'), pyxb.binding.datatypes.string, scope=QueryField, documentation=u'An optional, repeatable, brief description of the field that can be\n          used to help guide developers or end users in appropriate use of the field. May for \n          example, contain a links to additional documentation.'))
QueryField._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, u'name')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, u'description')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, u'type')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, u'searchable')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, u'returnable')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, u'sortable')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(QueryField._UseForTag(pyxb.namespace.ExpandedName(None, u'multivalued')), min_occurs=0L, max_occurs=1L)
    )
QueryField._ContentModel = pyxb.binding.content.ParticleModel(QueryField._GroupModel, min_occurs=1, max_occurs=1)



QueryEngineDescription._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'queryField'), QueryField, scope=QueryEngineDescription, documentation=u'A list of query fields supported by the query engine.'))

QueryEngineDescription._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'queryEngineVersion'), pyxb.binding.datatypes.string, scope=QueryEngineDescription, documentation=u'The version of the underlying query engine. Used by clients to determine possible\n          compatibility concerns or features available.'))

QueryEngineDescription._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'name'), pyxb.binding.datatypes.string, scope=QueryEngineDescription, documentation=u'The full, human readable name of the query engine. For example: \n            "Apache SOLR"'))

QueryEngineDescription._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'querySchemaVersion'), pyxb.binding.datatypes.string, scope=QueryEngineDescription, documentation=u'Version of the schema in use by the query engine, e.g. "1.0.1"'))

QueryEngineDescription._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'additionalInfo'), _d1.NonEmptyString, scope=QueryEngineDescription, documentation=u'An optional human readable description of the query engine. This can be \n            used to describe any special capabilities or intended uses for the query engine. For example, \n            a query engine may be tuned to suit a particular audience or domain as opposed to providing \n            a general purpose discovery mechanism.This field may also contain links to additional information about the query engine, \n          such as documentation for the search syntax provided by the query engine implemntors.'))
QueryEngineDescription._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(QueryEngineDescription._UseForTag(pyxb.namespace.ExpandedName(None, u'queryEngineVersion')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(QueryEngineDescription._UseForTag(pyxb.namespace.ExpandedName(None, u'querySchemaVersion')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(QueryEngineDescription._UseForTag(pyxb.namespace.ExpandedName(None, u'name')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(QueryEngineDescription._UseForTag(pyxb.namespace.ExpandedName(None, u'additionalInfo')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(QueryEngineDescription._UseForTag(pyxb.namespace.ExpandedName(None, u'queryField')), min_occurs=0L, max_occurs=None)
    )
QueryEngineDescription._ContentModel = pyxb.binding.content.ParticleModel(QueryEngineDescription._GroupModel, min_occurs=1, max_occurs=1)



QueryEngineList._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'queryEngine'), _d1.NonEmptyString, scope=QueryEngineList, documentation=u'The name of a queryEngine. This value will be used as a path element in \n            REST API calls and so should not contain characters that will need to be escaped.'))
QueryEngineList._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(QueryEngineList._UseForTag(pyxb.namespace.ExpandedName(None, u'queryEngine')), min_occurs=0L, max_occurs=None)
    )
QueryEngineList._ContentModel = pyxb.binding.content.ParticleModel(QueryEngineList._GroupModel, min_occurs=1, max_occurs=1)
