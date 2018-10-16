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

  <xsl:template match="v1:node | v2:node">
    <z:type>
      <z:section>
        <div class="type-header">
          <xsl:value-of select="name()"/>
        </div>
      </z:section>
    </z:type>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">node</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="identifier" mode="format_node_id"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">node</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="name" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">node</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="baseURL" mode="format_url"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">state</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="@replicate" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">state</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="@synchronize" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">state</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="@type" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">state</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="@state" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:apply-templates select="ping"/>

    <!--subjects-->

    <xsl:call-template name="bullet_type">
      <xsl:with-param name="section">subjects</xsl:with-param>
      <xsl:with-param name="label">nodeSubject</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="subject" mode="format_subject"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="bullet_type">
      <xsl:with-param name="section">subjects</xsl:with-param>
      <xsl:with-param name="label">contactSubject</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="contactSubject" mode="format_subject"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:apply-templates select="description"/>

    <xsl:apply-templates select="synchronization"/>

    <xsl:apply-templates select="services"/>

    <xsl:call-template name="restrictions"/>

    <xsl:apply-templates select="nodeReplicationPolicy"/>

    <xsl:apply-templates select="property"/>

  </xsl:template>

  <!-- services -->

  <xsl:template match="services">
    <z:type>
      <z:section>
        <xsl:value-of select="name()"/>
      </z:section>
      <z:label>name</z:label>
      <z:label>version</z:label>
      <z:label>available</z:label>
    </z:type>
    <xsl:apply-templates select="service"/>
  </xsl:template>

  <xsl:template match="service">
    <z:type>
      <z:section>services
      </z:section>
      <z:tree>
        <xsl:value-of select="@name"/>
      </z:tree>
      <z:tree>
        <xsl:value-of select="@version"/>
      </z:tree>
      <z:tree>
        <xsl:value-of select="@available"/>
      </z:tree>
    </z:type>
  </xsl:template>

  <!-- Service restrictions -->

  <xsl:template name="restrictions">
    <xsl:if test="boolean(services/service/restriction)">
      <z:type>
        <z:section>restrictions</z:section>
        <z:label>service</z:label>
        <z:label>methodName</z:label>
        <z:label>subject</z:label>
      </z:type>
      <xsl:apply-templates select="services/service/restriction"/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="services/service/restriction">
    <z:type>
      <z:section>restrictions</z:section>
      <z:tree>
        <xsl:value-of select="../@name"/>
      </z:tree>
      <z:tree>
        <xsl:value-of select="@methodName"/>
      </z:tree>
      <xsl:call-template name="bullet_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="./subject" mode="format_subject"/>
        </xsl:with-param>
      </xsl:call-template>
    </z:type>
  </xsl:template>

  <!-- synchronization -->

  <xsl:template match="synchronization">
    <xsl:apply-templates select="schedule"/>
    <xsl:apply-templates select="lastHarvested"/>
    <xsl:apply-templates select="lastCompleteHarvest"/>
  </xsl:template>

  <xsl:template match="schedule">
    <z:type>
      <z:section>
        <xsl:value-of select="name(..)"/>
      </z:section>
      <z:label>
        <xsl:value-of select="name(.)"/>
      </z:label>
      <z:tree>
        <xsl:apply-templates select="@*"/>
      </z:tree>
    </z:type>
  </xsl:template>

  <xsl:template match="schedule/@*">
    <xsl:value-of select="concat(name(), ':', .)"/>
    <xsl:if test="position() != last()">
      <xsl:value-of select="' '"/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="lastHarvested|lastCompleteHarvest">
    <xsl:call-template name="single_type">
      <xsl:with-param name="section">synchronization</xsl:with-param>
      <!--<xsl:with-param name="label">lastHarvested</xsl:with-param>-->
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="." mode="format_timestamp"/>
      </xsl:with-param>
    </xsl:call-template>
  </xsl:template>


  <!-- nodeReplicationPolicy -->

  <xsl:template match="nodeReplicationPolicy">
    <xsl:apply-templates select="maxObjectSize"/>
    <xsl:apply-templates select="spaceAllocated"/>

    <xsl:call-template name="bullet_type">
      <xsl:with-param name="section">nodeReplicationPolicy</xsl:with-param>
      <xsl:with-param name="label">allowedNode</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="allowedNode" mode="format_node_id"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="bullet_type">
      <xsl:with-param name="section">nodeReplicationPolicy</xsl:with-param>
      <xsl:with-param name="label">allowedObjectFormat</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="allowedObjectFormat"
                             mode="format_format_id"/>
      </xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="maxObjectSize | spaceAllocated">
    <xsl:call-template name="single_type">
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="." mode="format_integer"/>
      </xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <!-- ping -->

  <xsl:template match="ping">
    <xsl:call-template name="single_type">
      <xsl:with-param name="section">ping</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="@success" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>
    <xsl:call-template name="single_type">
      <xsl:with-param name="section">ping</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="@lastSuccess" mode="format_timestamp"/>
      </xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <!--description-->

  <xsl:template match="v1:node|v2:node/description">
    <z:type>
      <z:section>description</z:section>
      <xsl:call-template name="single_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="." mode="format_long_text"/>
        </xsl:with-param>
      </xsl:call-template>
    </z:type>
  </xsl:template>

  <!-- Node doc property (contains key, type, value)  -->

  <xsl:template match="property[@key]">
    <xsl:if test="position() = 1">
      <z:type>
        <z:section>properties</z:section>
        <z:label>key</z:label>
        <z:label>type</z:label>
        <z:label>value</z:label>
      </z:type>
    </xsl:if>
    <z:type>
      <z:section>properties</z:section>
      <xsl:call-template name="single_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="@key" mode="format_short_text"/>
        </xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="single_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="@type" mode="format_short_text"/>
        </xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="single_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="." mode="format_short_text"/>
        </xsl:with-param>
      </xsl:call-template>
    </z:type>

  </xsl:template>

</xsl:stylesheet>
