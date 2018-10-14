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

  <xsl:template match="v1:systemMetadata | v2:systemMetadata">
    <z:type>
      <z:section>
        <div class="type-header">
          <xsl:value-of select="name()"/>
        </div>
      </z:section>
    </z:type>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">object</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="identifier" mode="format_identifier"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">object</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="seriesId" mode="format_identifier"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">object</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="fileName" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">object</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="mediaType/@name" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">object</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="serialVersion" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">object</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="formatId" mode="format_format_id"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">object</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="size" mode="format_integer"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">object</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="checksum" mode="format_checksum"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">subjects</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="submitter" mode="format_subject"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">subjects</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="rightsHolder" mode="format_subject"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">revisions</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="archived" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">revisions</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="obsoletes" mode="format_node_id"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">revisions</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="obsoletedBy" mode="format_node_id"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">locations</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="originMemberNode" mode="format_node_id"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">locations</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="authoritativeMemberNode"
                             mode="format_node_id"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">timestamps</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="dateUploaded" mode="format_timestamp"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:call-template name="single_type">
      <xsl:with-param name="section">timestamps</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="dateSysMetadataModified"
                             mode="format_timestamp"/>
      </xsl:with-param>
    </xsl:call-template>

    <xsl:apply-templates select="accessPolicy/allow"/>

    <xsl:apply-templates select="replicationPolicy"/>

    <xsl:apply-templates select="replica"/>

    <xsl:apply-templates select="mediaType/property"/>

  </xsl:template>

  <!--accessPolicy-->

  <xsl:template match="accessPolicy/allow">
    <z:type>
      <z:section>
        <xsl:value-of select="name(..)"/>
      </z:section>
      <z:label>
        <xsl:value-of select="name()"/>
      </z:label>
      <xsl:call-template name="bullet_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="permission" mode="format_short_text"/>
        </xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="bullet_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="subject" mode="format_subject"/>
        </xsl:with-param>
      </xsl:call-template>
    </z:type>
  </xsl:template>

  <!--replicationPolicy-->

  <xsl:template match="replicationPolicy">
    <xsl:call-template name="single_type">
      <xsl:with-param name="section">replicationPolicy</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="@replicationAllowed"
                             mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>
    <xsl:call-template name="single_type">
      <xsl:with-param name="section">replicationPolicy</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="@numberReplicas" mode="format_short_text"/>
      </xsl:with-param>
    </xsl:call-template>
    <xsl:call-template name="bullet_type">
      <xsl:with-param name="section">replicationPolicy</xsl:with-param>
      <xsl:with-param name="label">preferredMemberNode</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="preferredMemberNode"
                             mode="format_node_id"/>
      </xsl:with-param>
    </xsl:call-template>
    <xsl:call-template name="bullet_type">
      <xsl:with-param name="section">replicationPolicy</xsl:with-param>
      <xsl:with-param name="label">blockedMemberNode</xsl:with-param>
      <xsl:with-param name="nodes">
        <xsl:apply-templates select="blockedMemberNode" mode="format_node_id"/>
      </xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <!-- replicas -->

  <xsl:template match="replica">
    <xsl:if test="position() = 1">
      <z:type>
        <z:section>replica</z:section>
        <z:label>replicaMemberNode</z:label>
        <z:label>replicationStatus</z:label>
        <z:label>replicaVerified</z:label>
      </z:type>
    </xsl:if>
    <z:type>
      <z:section>replica</z:section>
      <xsl:call-template name="single_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="replicaVerified"
                               mode="format_timestamp"/>
        </xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="single_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="replicationStatus"
                               mode="format_short_text"/>
        </xsl:with-param>
      </xsl:call-template>
      <xsl:call-template name="single_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="replicaMemberNode"
                               mode="format_node_id"/>
        </xsl:with-param>
      </xsl:call-template>
    </z:type>
  </xsl:template>

  <!-- property (name, value) -->

  <xsl:template match="property[@name]">
    <xsl:if test="position() = 1">
      <z:type>
        <z:section>properties</z:section>
        <z:label>name</z:label>
        <z:label>value</z:label>
      </z:type>
    </xsl:if>
    <z:type>
      <z:section>properties</z:section>
      <xsl:call-template name="single_tree">
        <xsl:with-param name="nodes">
          <xsl:apply-templates select="@name" mode="format_short_text"/>
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
