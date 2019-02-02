<?xml version="1.0"?>
<!--
Must be imported before other imports
-->
<xsl:stylesheet xmlns:exsl="http://exslt.org/common"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:v1="http://ns.dataone.org/service/types/v1"
                xmlns:v1_1="http://ns.dataone.org/service/types/v1_1"
                xmlns:v2="http://ns.dataone.org/service/types/v2.0"
                xmlns:z="intermediate.types" version="1.0"
                xmlns="http://www.w3.org/1999/xhtml"
                exclude-result-prefixes="exsl xsl xs v1 v1_1 v2 z"
                extension-element-prefixes="exsl"
>
  <!--
  XSLT has some implicit templates which match if there are no other templates that match. One of these copies
  all text contents of the elements to the output, which generally seems like a bad dea. This template overrides the
  implicit template and suppresses text in non-matched nodes.

  For debugging, uncomment the xsl:message to get a list of unmatched nodes in the console. Note that unmatched nodes
  does not necessarily mean that information has been lost, the nodes could be handled directly via xpaths.
  -->
  <xsl:template match="node()|@*" priority="0">
    <!--
    Eat any leftover text
    -->

    <!--<xsl:message terminate="yes">-->
    <!--<z:msg>Unmatched node:</z:msg>-->
    <!--<z:path><xsl:call-template name="get_path_list"/></z:path>-->
    <!--<z:node><xsl:copy-of select="."/></z:node>-->
    <!--</xsl:message>-->

    <!--<z:msg>Unmatched node:</z:msg>-->
    <!--<z:path>-->
    <!--<xsl:call-template name="get_path_list"/>-->
    <!--</z:path>-->
    <!--<z:node>-->
    <!--<xsl:copy-of select="."/>-->
    <!--</z:node>-->
    <xsl:apply-templates/>
  </xsl:template>

  <!--<xsl:template match="text()" priority="0"/>-->


  <!-- Identity templates -->

  <!--<xsl:template match="*">-->
  <!--<xsl:copy>-->
  <!--<xsl:apply-templates select="@*"/>-->
  <!--<xsl:apply-templates select="node()"/>-->
  <!--</xsl:copy>-->
  <!--</xsl:template>-->

  <!--<xsl:template match="*">-->
  <!--<xsl:copy>-->
  <!--<xsl:apply-templates select="*"/>-->
  <!--</xsl:copy>-->
  <!--</xsl:template>-->

  <!--<xsl:template match="*">-->
  <!--<xsl:element name="{name()}">-->
  <!--<xsl:apply-templates select="@*"/>-->
  <!--<xsl:apply-templates select="node()"/>-->
  <!--</xsl:element>-->
  <!--</xsl:template>-->

  <!--<xsl:template match="@* | text() | comment() | processing-instruction()">-->
  <!--<xsl:copy/>-->
  <!--</xsl:template>-->
</xsl:stylesheet>
