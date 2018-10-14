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

  <xsl:template match="status">

    <z:type>
      <z:section>
        <div class="type-header">
          <xsl:value-of select="name()"/>
        </div>
      </z:section>
    </z:type>

    <!--node-->

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">node</xsl:with-param>
      <xsl:with-param name="label">nodeId</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='nodeId']"
                             mode="format_node_id"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">node</xsl:with-param>
      <xsl:with-param name="label">nodeName</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='nodeName']"
                             mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">node</xsl:with-param>
      <xsl:with-param name="label">envRootUrl</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='envRootUrl']"
                             mode="format_url">
        </xsl:apply-templates>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">node</xsl:with-param>
      <xsl:with-param name="label">serverTime</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='serverTime']"
                             mode="format_timestamp"/>
      </xsl:with-param>
    </xsl:call-template>

    <!--objects-->


    <!--versions-->

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">versions</xsl:with-param>
      <xsl:with-param name="label">gmnVersion</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='gmnVersion']"
                             mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">versions</xsl:with-param>
      <xsl:with-param name="label">pythonVersion</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='pythonVersion']"
                             mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">versions</xsl:with-param>
      <xsl:with-param name="label">djangoVersion</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='djangoVersion']"
                             mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">versions</xsl:with-param>
      <xsl:with-param name="label">postgresVersion</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='postgresVersion']"
                             mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <!--storage-->

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">storage</xsl:with-param>
      <xsl:with-param name="label">avgSciDataSize</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='avgSciDataSize']"
                             mode="format_integer"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">storage</xsl:with-param>
      <xsl:with-param name="label">sciobjStorageSpaceUsed</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='sciobjStorageSpaceUsed']"
                             mode="format_integer"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">storage</xsl:with-param>
      <xsl:with-param name="label">sciobjStorageSpaceFree</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='sciobjStorageSpaceFree']"
                             mode="format_integer"/>
      </xsl:with-param>
    </xsl:call-template>

    <!--counts-->

    <z:type>
      <z:section>counts</z:section>
      <z:label>totalSciObjCount</z:label>
      <z:tree>
        <xsl:apply-templates select="value[@name='totalSciObjCount']"
                             mode="format_integer">
          <xsl:with-param name="units"/>
        </xsl:apply-templates>
      </z:tree>
      <z:tree>
        <div>
          <a class="round-button" href="{ concat($base_url, 'v2/object') }">
            browse
          </a>
        </div>
      </z:tree>
    </z:type>

    <z:type>
      <z:section>counts</z:section>
      <z:label>totalEventCount</z:label>
      <z:tree>
        <xsl:apply-templates select="value[@name='totalEventCount']"
                             mode="format_integer">
          <xsl:with-param name="units"/>
        </xsl:apply-templates>
      </z:tree>
      <z:tree>
        <div>
          <a class="round-button" href="{ concat($base_url, 'v2/log') }">
            browse
          </a>
        </div>
      </z:tree>
    </z:type>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">counts</xsl:with-param>
      <xsl:with-param name="label">lastHourEventCount</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='lastHourEventCount']"
                             mode="format_integer">
          <xsl:with-param name="units"/>
        </xsl:apply-templates>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">counts</xsl:with-param>
      <xsl:with-param name="label">uniqueSubjectCount</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='uniqueSubjectCount']"
                             mode="format_integer">
          <xsl:with-param name="units"/>
        </xsl:apply-templates>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">counts</xsl:with-param>
      <xsl:with-param name="label">totalPermissionCount</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="value[@name='totalPermissionCount']"
                             mode="format_integer">
          <xsl:with-param name="units"/>
        </xsl:apply-templates>
      </xsl:with-param>
    </xsl:call-template>

    <!-- formats -->
    <xsl:apply-templates select="value[@name='sciobjCountByFormat']/*"/>

    <!--description-->
    <xsl:apply-templates select="value[@name='description']"/>
  </xsl:template>

  <xsl:template match="value[@name='sciobjCountByFormat']/*">
    <z:type>
      <z:section>formats</z:section>
      <z:tree>
        <a>
          <!--TODO: Refactor formatters to also handle attributes.-->
          <xsl:call-template name="add_href_and_text">
            <xsl:with-param name="abs_url"
                            select="concat($env_root_url, 'v2/formats')"/>
            <xsl:with-param name="rel_url" select="string(@name)"/>
          </xsl:call-template>
        </a>
      </z:tree>
      <z:tree>
        <xsl:apply-templates select="."
                             mode="format_integer">
          <xsl:with-param name="units"/>
        </xsl:apply-templates>
      </z:tree>
    </z:type>
  </xsl:template>

  <xsl:template match="value[@name='description']">
    <z:type>
      <z:section>description</z:section>
      <xsl:call-template name="single_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="."
                               mode="format_long_text"/>
        </xsl:with-param>
      </xsl:call-template>
    </z:type>
  </xsl:template>

</xsl:stylesheet>
