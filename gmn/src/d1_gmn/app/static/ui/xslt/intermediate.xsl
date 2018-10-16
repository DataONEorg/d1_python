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
  <xsl:import href="util.xsl"/>

  <!--
  ################# Generate a <type> with children
  -->

  <!-- <type> with single logical value -->
  <xsl:template name="single_type">
    <xsl:param name="section" select="name(..)"/>
    <xsl:param name="nodes" select="."/>
    <xsl:param name="label" select="name(exsl:node-set($nodes)/*)"/>
    <xsl:if test="boolean(exsl:node-set($nodes))">
      <z:type>
        <z:section>
          <xsl:value-of select="$section"/>
        </z:section>
        <z:label>
          <xsl:value-of select="$label"/>
        </z:label>
        <z:tree>
          <xsl:copy-of select="exsl:node-set($nodes)/node()/node()"/>
        </z:tree>
      </z:type>
    </xsl:if>
  </xsl:template>

  <!-- <type> with bullets -->
  <xsl:template name="bullet_type">
    <xsl:param name="section" select="name(..)"/>
    <xsl:param name="nodes" select="."/>
    <xsl:param name="label" select="name(exsl:node-set($nodes))"/>
    <xsl:call-template name="single_type">
      <xsl:with-param name="section" select="$section"/>
      <xsl:with-param name="label" select="$label"/>
      <xsl:with-param name="nodes">
        <xsl:call-template name="bullet_tree">
          <xsl:with-param name="nodes" select="exsl:node-set($nodes)/node()"/>
        </xsl:call-template>
      </xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <!--
  ################# Generate a <tree>
  -->

  <!-- <tree> containing a bullets -->
  <xsl:template name="bullet_tree">
    <xsl:param name="nodes" select="."/>
    <xsl:if test="boolean(exsl:node-set($nodes))">
      <z:tree>
        <ul>
          <xsl:apply-templates select="exsl:node-set($nodes)"
                               mode="bullet_value"/>
        </ul>
      </z:tree>
    </xsl:if>
  </xsl:template>

  <!-- <tree> containing a single logical item -->
  <xsl:template name="single_tree">
    <xsl:param name="nodes" select="."/>
    <xsl:if test="boolean(exsl:node-set($nodes))">
      <z:tree>
        <xsl:copy-of select="exsl:node-set($nodes)"/>
      </z:tree>
    </xsl:if>
  </xsl:template>

  <!-- Wrap nodes in <li> elements (deep copy) -->
  <xsl:template match="node()|@*" mode="bullet_value">
    <li>
      <xsl:copy-of select="."/>
    </li>
  </xsl:template>

  <!--
  ################# Format values
  -->

  <!-- pid or sid
  - Links to download and resolve object
  -->
  <xsl:template match="node()|@*" mode="format_identifier">
    <xsl:element name="{ name() }">
      <xsl:call-template name="link_with_button">
        <xsl:with-param name="abs_url" select="concat($base_url, 'v2/object')"/>
        <xsl:with-param name="rel_url" select="."/>
        <xsl:with-param name="link_classes" select="identifier"/>
        <xsl:with-param name="button_text" select="'R'"/>
        <xsl:with-param name="button_abs_url"
                        select="concat($env_root_url, 'v2/resolve')"/>
        <xsl:with-param name="button_2_text" select="'S'"/>
        <xsl:with-param name="button_2_abs_url" select="concat($base_url, 'v2/meta')"/>
      </xsl:call-template>
    </xsl:element>
  </xsl:template>

  <!-- baseURL and other absolute urls, value -->
  <xsl:template match="node()|@*" mode="format_url">
    <xsl:element name="{ name() }">
      <a>
        <xsl:call-template name="add_href_and_text">
          <xsl:with-param name="abs_url" select="."/>
          <xsl:with-param name="rel_url" select="''"/>
          <xsl:with-param name="text" select="."/>
        </xsl:call-template>
      </a>
    </xsl:element>
  </xsl:template>


  <!-- ipAddress, value -->
  <xsl:template match="node()|@*" mode="format_ip_address">
    <xsl:element name="{ name() }">
      <a>
        <xsl:call-template name="add_href_and_text">
          <xsl:with-param name="abs_url"
                          select="'http://api.hostip.info/get_html.php?position=true&amp;ip='"/>
          <xsl:with-param name="rel_url" select="."/>
        </xsl:call-template>
      </a>
    </xsl:element>
  </xsl:template>

  <!-- formatId, value -->
  <xsl:template match="node()|@*" mode="format_format_id">
    <xsl:element name="{ name() }">
      <a>
        <xsl:call-template name="add_href_and_text">
          <xsl:with-param name="abs_url"
                          select="concat($env_root_url, 'v2/formats')"/>
          <xsl:with-param name="rel_url" select="."/>
        </xsl:call-template>
      </a>
    </xsl:element>
  </xsl:template>

  <!-- nodeId, value -->
  <xsl:template match="node()|@*" mode="format_node_id">
    <xsl:element name="{ name() }">
      <a>
        <xsl:call-template name="add_href_and_text">
          <xsl:with-param name="abs_url"
                          select="concat($search_root_url, 'profile')"/>
          <xsl:with-param name="rel_url" select="substring-after(substring-after(.,':'),':')"/>
          <xsl:with-param name="text" select="."/>
          <xsl:with-param name="noencode" select="'y'"/>
        </xsl:call-template>
      </a>
    </xsl:element>
  </xsl:template>

  <!-- subject, value -->
  <xsl:template match="node()|@*" mode="format_subject">
    <xsl:element name="{ name() }">
      <a>
        <xsl:call-template name="add_href_and_text">
          <xsl:with-param name="abs_url"
                          select="concat($search_root_url, 'profile')"/>
          <xsl:with-param name="rel_url" select="."/>
          <!--<xsl:with-param name="text" select="."/>-->
          <!--<xsl:with-param name="noencode" select="'y'"/>-->
        </xsl:call-template>
      </a>
    </xsl:element>
    <!--<xsl:element name="{ name() }">-->
      <!--<a>-->
        <!--<xsl:call-template name="add_href_and_text">-->
          <!--<xsl:with-param name="abs_url" select="'/'"/>-->
          <!--<xsl:with-param name="rel_url" select="."/>-->
        <!--</xsl:call-template>-->
      <!--</a>-->
    <!--</xsl:element>-->
    <!--<xsl:apply-templates select="." mode="format_short_text"/>-->
  </xsl:template>

  <!-- dateTime, value -->
  <xsl:template match="node()|@*" mode="format_timestamp">
    <xsl:element name="{ name() }">
      <xsl:call-template name="format_date_time">
        <xsl:with-param name="iso" select="."/>
      </xsl:call-template>
    </xsl:element>
  </xsl:template>

  <!-- integer, value
  - Grouped by thousands (US)
  -->
  <xsl:template match="node()|@*" mode="format_integer">
    <xsl:param name="units" select="'bytes'"/>
    <xsl:element name="{ name() }">
      <xsl:call-template name="group_thousands">
        <xsl:with-param name="integer" select="."/>
        <xsl:with-param name="units" select="$units"/>
      </xsl:call-template>
    </xsl:element>
  </xsl:template>

  <!-- checksum, value
  - Includes checksum algorithm
  -->
  <xsl:template match="node()|@*" mode="format_checksum">
    <xsl:element name="{ name() }">
      <xsl:value-of select="."/>
      (<xsl:value-of select="@algorithm"/>)
    </xsl:element>
  </xsl:template>

  <!-- short text field, value
  - Never wraps
  - Truncated with ellipsis if too long
  - Full value displayed in tooltip
  -->
  <xsl:template match="node()|@*" mode="format_short_text">
    <xsl:element name="{ name() }">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:template>

  <!-- long text field, value
  - May wrap
  - Never truncated
  -->
  <xsl:template match="node()|@*" mode="format_long_text">
    <xsl:element name="{ name() }">
      <div class="long-text">
        <xsl:value-of select="."/>
      </div>
    </xsl:element>
  </xsl:template>

  <!-- Link text with button
  - The link displays {rel_url} and points to {abs_url}/{rel_url}.
  - The button displays {button_text} and points to {button_abs_url}/{rel_url}.
  - See the CSS for description of this element structure and styling.
  -->
  <xsl:template name="link_with_button">
    <xsl:param name="abs_url" select="/"/>
    <xsl:param name="rel_url" select="''"/>
    <xsl:param name="button_text" select="'R'"/>
    <xsl:param name="button_abs_url" select="'/'"/>
    <xsl:param name="button_2_text" select="''"/>
    <xsl:param name="button_2_abs_url" select="''"/>
    <xsl:param name="link_classes" select="''"/>
    <div class="parent">
      <div class="description">
        <a class="text">
          <xsl:call-template name="add_href_and_text">
            <xsl:with-param name="abs_url" select="$abs_url"/>
            <xsl:with-param name="rel_url" select="$rel_url"/>
          </xsl:call-template>
        </a>
      </div>
      <div>
        <a class="round-button { $link_classes }">
          <xsl:call-template name="add_href_and_text">
            <xsl:with-param name="abs_url" select="$button_abs_url"/>
            <xsl:with-param name="rel_url" select="$rel_url"/>
            <xsl:with-param name="text" select="$button_text"/>
          </xsl:call-template>
        </a>
      </div>
      <xsl:if test="$button_2_text != ''">
        <div>
          <a class="round-button">
            <xsl:call-template name="add_href_and_text">
              <xsl:with-param name="abs_url" select="$button_2_abs_url"/>
              <xsl:with-param name="rel_url" select="$rel_url"/>
              <xsl:with-param name="text" select="$button_2_text"/>
            </xsl:call-template>
          </a>
        </div>
      </xsl:if>
    </div>
  </xsl:template>

  <!-- Add href and text to an open <a> -->
  <xsl:template name="add_href_and_text">
    <xsl:param name="abs_url" select="'/'"/>
    <xsl:param name="rel_url" select="."/>
    <xsl:param name="text" select="$rel_url"/>
    <xsl:param name="noencode" select="'n'"/>
    <xsl:variable name="enc_element">
      <xsl:choose>
        <xsl:when test="$noencode = 'n'">
          <xsl:call-template name="url_encode">
            <xsl:with-param name="str" select="$rel_url"/>
          </xsl:call-template>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$rel_url"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:attribute name="href">
      <xsl:value-of select="concat($abs_url, '/', $enc_element)"/>
    </xsl:attribute>
    <xsl:value-of select="$text"/>
  </xsl:template>

</xsl:stylesheet>
