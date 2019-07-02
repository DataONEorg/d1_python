<!--
XSLT applied to eml-2.0.0 XML docs before validation.
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

  <!--  Workaround for issue described in eml-2.0.0.eml.xslt-->
  <xsl:template match="additionalMetadata/*[not(self::describes)]"/>

  <!--
  Workaround for:

  <string>: Line 166: Element 'url':
  'srb://seek:/home/beam.seek/IPCC_climate/Future/Differences/CGCM1B2a/CCCma_B2a_TMAX_2020.dif'
  is not a valid value of the atomic type 'xs:anyURI'.
  -->
  <xsl:template match="url">
    <xsl:copy>
      <xsl:value-of select="translate(text(), 'seek:/', '')"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
