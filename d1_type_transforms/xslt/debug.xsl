<?xml version="1.0" encoding="UTF-8"?>
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
  <xsl:template name="dump_nodeset">
    <xsl:param name="nodes" select="."/>
    <!--<xsl:message>-->
    <div>
    ################# BEGIN: NODESET #################
    <xsl:apply-templates select="exsl:node-set($nodes)/* |
    exsl:node-set($nodes)/text()" mode="nodetostring"/>
    ################# END: NODESET #################
    </div>
    <!--</xsl:message>-->
  </xsl:template>

  <!--
    Converts a nodeset to string, especially useful for json conversions.

    ===================================================================================

    Copyright 2011, Thomas Appel, http://thomas-appel.com, mail(at)thomas-appel.com
    dual licensed under MIT and GPL license
    http://dev.thomas-appel.com/licenses/mit.txt
    http://dev.thomas-appel.com/licenses/gpl.txt

    ===================================================================================

    Example usage:

    (convert a exsl nodeset to string: )
    ___

    <xsl:variable name="somelink">
      <a href="{url}" class="some-class"><xsl:value-of select="name"/></a>
    </xsl:variable>
    <xsl:apply-templates select="exsl:node-set($somelink)/* | exsl:node-set($some-link)/text()"/>
    ___

    (convert xml noset to string: )
    ___

    <xsl:apply-templates select="node | node[text()]"/>
  -->
  <xsl:variable name="q">
    <xsl:text>"</xsl:text>
  </xsl:variable>
  <xsl:variable name="empty"/>

  <xsl:template match="*" mode="selfclosetag">
    <xsl:text>&lt;</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:apply-templates select="@*" mode="attribs"/>
    <xsl:text>/&gt;</xsl:text>
  </xsl:template>

  <xsl:template match="*" mode="opentag">
    <xsl:text>&lt;</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:apply-templates select="@*" mode="attribs"/>
    <xsl:text>&gt;</xsl:text>
  </xsl:template>

  <xsl:template match="*" mode="closetag">
    <xsl:text>&lt;/</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>&gt;</xsl:text>
  </xsl:template>

  <xsl:template match="* | text()" mode="nodetostring">
    <xsl:choose>
      <xsl:when test="boolean(name())">
        <xsl:choose>
          <!--
             if element is not empty
          -->
          <xsl:when test="normalize-space(.) != $empty or *">
            <xsl:apply-templates select="." mode="opentag"/>
            <xsl:apply-templates select="* | text()" mode="nodetostring"/>
            <xsl:apply-templates select="." mode="closetag"/>
          </xsl:when>
          <!--
             assuming emty tags are self closing, e.g. <img/>, <source/>, <input/>
          -->
          <xsl:otherwise>
            <xsl:apply-templates select="." mode="selfclosetag"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="@*" mode="attribs">
    <xsl:if test="position() = 1">
      <xsl:text></xsl:text>
    </xsl:if>
    <xsl:value-of select="concat(name(), '=', $q, ., $q)"/>
    <xsl:if test="position() != last()">
      <xsl:text></xsl:text>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>
