<!--
XSLT applied to eml-2.0.0 eml.xsd.

libxml2 is unable to load a schema containing a <sequence> that includes both an <any>
and an <element> with minOccurs="0". The error message is:

element complexType: Schemas parser error : local complex type: The content model is not
determinist.

The additionalMetadata structure in eml-2.0.0/eml.xsd contains such a structure. This
works around the issue by removing the additionalMetadata/any structure from the
eml.xsd.

A corresponding transform that removes additionalMetadata/any elements from eml-2.0.0
XML docs is applied before validation.

As the only requirement for the additionalMetadata/any element is that it is well
formed, and well-formedness is checked separately when the document is parsed, this does
not lower the quality of the validation.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
>
  <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
  <!--  omit-xml-declaration="yes" -->

  <xsl:strip-space elements="*"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="node()|@*"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="xs:element[@name='additionalMetadata']/xs:complexType/xs:sequence/xs:any"/>

</xsl:stylesheet>
