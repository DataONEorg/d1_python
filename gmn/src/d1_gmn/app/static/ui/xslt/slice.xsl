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
  <xsl:import href="util.xsl"/>

  <!--
  ################# Slice browser
  - Show slice information and provide links to previous and next slices.
  -->

  <xsl:template name="slice">
    <xsl:param name="label" select="'records'"/>
    <z:type>
      <z:section>slice</z:section>
      <z:label>
        <xsl:value-of select="$label"/>
      </z:label>
      <z:tree>
        <xsl:choose>
          <xsl:when test="@total=0">
            &lt;none>
          </xsl:when>
          <xsl:otherwise>
            <xsl:call-template name="group_thousands">
              <xsl:with-param name="integer" select="@start + 1"/>
            </xsl:call-template>
            to
            <xsl:call-template name="group_thousands">
              <xsl:with-param name="integer" select="@start + @count"/>
            </xsl:call-template>
            of
            <xsl:call-template name="group_thousands">
              <xsl:with-param name="integer" select="@total"/>
            </xsl:call-template>
            <xsl:variable name="grouped_count">
              <xsl:call-template name="group_thousands">
                <xsl:with-param name="integer" select="@count"/>
              </xsl:call-template>
            </xsl:variable>
            <xsl:value-of
                select="concat('(count: ', normalize-space($grouped_count), ')')"/>
          </xsl:otherwise>
        </xsl:choose>
      </z:tree>
    </z:type>
    <z:type>
      <z:section>slice</z:section>
      <z:label/>
      <z:tree>
        <xsl:choose>
          <xsl:when test="@start > 0 and @start - @count >= 0">
            <a class="round-button" onclick="open_slice({ @start - @count });">
              Previous
            </a>
          </xsl:when>
          <xsl:when test="@start > 0">
            <a class="round-button" onclick="open_slice(0);">
              Previous
            </a>
          </xsl:when>
          <xsl:otherwise>
            <a class="round-button round-button-disabled">
              Previous
            </a>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:choose>
          <xsl:when test="@start + @count &lt; @total">
            <a class="round-button" onclick="open_slice({ @start + @count });">
              Next
            </a>
          </xsl:when>
          <xsl:otherwise>
            <a class="round-button round-button-disabled">
              Next
            </a>
          </xsl:otherwise>
        </xsl:choose>
      </z:tree>
    </z:type>
  </xsl:template>
</xsl:stylesheet>
