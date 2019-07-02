<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
  <!--  omit-xml-declaration="yes" -->

  <xsl:strip-space elements="*"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="node()|@*"/>
    </xsl:copy>
  </xsl:template>

  <!--  Work arounds for regex handling mismatch -->
  <xsl:template
      match="attrdef|attrdefs|attrlabl|cntemail|cntpos|cntvoice|edition|ellips|enttypd|enttypds|enttypl|geoform|horizdn|indspref|native|othercit|placekt|supplinf|tempkey|tempkt[normalize-space()='']">
    <xsl:copy>[DUMMY FOR VALIDATION]</xsl:copy>
  </xsl:template>

  <xsl:template match="metrd|metfrd[normalize-space()='']">
    <xsl:copy>cd00000</xsl:copy>
  </xsl:template>

  <xsl:template match="denflat|semiaxis|latres|longres[normalize-space()='']">
    <xsl:copy>1.0</xsl:copy>
  </xsl:template>

  <xsl:template match="eastbc|westbc|northbc|southbc">
    <xsl:copy>0</xsl:copy>
  </xsl:template>

  <!--  Remove elements-->
  <xsl:template match="Source|mercury|dataqual|title|pubinfo"/>

  <xsl:template match="attrdomv[not(edom)]">
    <xsl:copy>
      <edom>
        <edomv>[DUMMY]</edomv>
        <edomvd>[DUMMY]</edomvd>
        <edomvds>[DUMMY]</edomvds>
      </edom>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="geogunit">
    <xsl:copy>Decimal degrees</xsl:copy>
  </xsl:template>

</xsl:stylesheet>
