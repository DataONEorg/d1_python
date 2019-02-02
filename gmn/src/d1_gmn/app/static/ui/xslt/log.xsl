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
  <xsl:import href="slice.xsl"/>

  <xsl:template match="v1:log | v2:log">
    <z:type>
      <z:section>
        <div class="type-header">
          <xsl:value-of select="name()"/>
        </div>
      </z:section>
    </z:type>

    <xsl:call-template name="slice">
      <xsl:with-param name="label">events</xsl:with-param>
    </xsl:call-template>

    <xsl:apply-templates select="logEntry"/>
  </xsl:template>

  <xsl:template match="logEntry">
    <!-- Force section delimiter -->
    <z:type>
    </z:type>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section" select="name()"/>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="entryId" mode="format_integer">
          <xsl:with-param name="units"/>
        </xsl:apply-templates>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section" select="name()"/>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="identifier" mode="format_identifier"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section" select="name()"/>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="ipAddress" mode="format_ip_address"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section" select="name()"/>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="userAgent" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section" select="name()"/>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="subject" mode="format_subject"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section" select="name()"/>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="event" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section" select="name()"/>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="dateLogged" mode="format_timestamp"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section" select="name()"/>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="nodeIdentifier" mode="format_node_id"/>
      </xsl:with-param>
    </xsl:call-template>

  </xsl:template>
</xsl:stylesheet>

