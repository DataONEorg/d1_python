<?xml version="1.0"?>
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
  <xsl:import href="intermediate.xsl"/>

  <xsl:template match="error">
    <z:type>
      <z:section>
        <div class="type-header http-error-header">
          <xsl:value-of select="name()"/>
        </div>
      </z:section>
    </z:type>

    <z:type>
      <z:section>
        <xsl:value-of select="name()"/>
      </z:section>
      <z:tree>
        <div class="http-error-code">
          <xsl:apply-templates select="@errorCode" mode="format_short_text"/>
        </div>
      </z:tree>
      <z:tree>
        <div class="http-error-name">
          <xsl:apply-templates select="@name" mode="format_short_text"/>
        </div>
      </z:tree>
    </z:type>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">error</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="./@detailCode[. != '1']"
                             mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">error</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="./@nodeId" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:apply-templates select="description"/>
    <xsl:apply-templates select="traceInformation"/>

  </xsl:template>

  <!--description, traceInformation-->

  <xsl:template match="error/description|error/traceInformation">
    <z:type>
      <z:section><xsl:value-of select="name()"/></z:section>
      <xsl:call-template name="single_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="."
                               mode="format_long_text"/>
        </xsl:with-param>
      </xsl:call-template>
    </z:type>
  </xsl:template>

</xsl:stylesheet>

