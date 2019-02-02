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
  <!-- implicit.xsl must be imported before other imports -->
  <xsl:import href="implicit.xsl"/>
  <xsl:import href="debug.xsl"/>

  <xsl:import href="error.xsl"/>
  <xsl:import href="gmn_status.xsl"/>
  <xsl:import href="intermediate.xsl"/>
  <xsl:import href="log.xsl"/>
  <xsl:import href="node.xsl"/>
  <xsl:import href="object_format.xsl"/>
  <xsl:import href="object_list.xsl"/>
  <xsl:import href="sysmeta.xsl"/>

  <xsl:output doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
              doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
              encoding="utf-8" indent="yes" method="xml"/>

  <xsl:decimal-format name="US"/>
  <xsl:decimal-format name="EU" decimal-separator="," grouping-separator="."/>
  <!--
  The root of the tree of transforms. Set up the basic HTML document structure
  and initiate processing of the rest of the tree.
  -->
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <xsl:call-template name="document_header"/>
      <body>
        <xsl:call-template name="d1_type_to_xhtml_grid"/>
      </body>
    </html>
  </xsl:template>

  <xsl:template name="d1_type_to_xhtml_grid">
    <!-- Transform the DataONE type to a simple intermediate nodeset, described
    in intermediate.xsl.
    -->
    <xsl:variable name="intermediate_nodeset">
      <xsl:apply-templates/>
    </xsl:variable>

    <!-- Trim and collapse whitespace in the intermediate nodeset.
    -->
    <xsl:variable name="trimmed_nodeset">
      <xsl:apply-templates mode="trim_and_normalize"
                           select="exsl:node-set($intermediate_nodeset)/*"/>
    </xsl:variable>

    <!--Dump trimmed nodeset -->
    <!--<xsl:call-template name="dump_nodeset">-->
    <!--<xsl:with-param name="nodes" select="$trimmed_nodeset"/>-->
    <!--</xsl:call-template>-->

    <!-- Transform the intermediate types to XHTML, using CSS Grid for layout.
    -->
    <xsl:call-template name="generate_grid">
      <xsl:with-param name="nodeset">
        <xsl:copy-of select="$trimmed_nodeset"/>
      </xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="generate_grid">
    <xsl:param name="nodeset"/>
    <!--
    The number of columns required for the generated grid is determined by the
    number of <tree> elements in the the largest <type> element, plus one column
    each for <section> and <label>.
    -->
    <xsl:variable name="column_count">
      <xsl:call-template name="max">
        <xsl:with-param name="sequence">
          <xsl:for-each select="exsl:node-set($nodeset)/z:type">
            <z:count>
              <xsl:value-of select="count(./*)"/>
            </z:count>
          </xsl:for-each>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <!-- Generate grid-->
    <div id="d1-type">
      <div class="grid-outer">
        <div class="grid-inner">
          <xsl:apply-templates select="exsl:node-set($nodeset)/*">
            <xsl:with-param name="column_count" select="$column_count"/>
          </xsl:apply-templates>
        </div>
      </div>
    </div>
  </xsl:template>

  <!--
  - Generate grid rows
  - Apply section -> label -> text -> tree ordering
  -->
  <xsl:template match="z:type">
    <xsl:param name="column_count"/>
    <xsl:variable name="is_first_section"
                  select="not(preceding-sibling::z:type)"/>
    <xsl:variable name="is_new_section"
                  select="boolean(z:section/. != preceding-sibling::*[1]/z:section/.)
                  or not(preceding-sibling::*[1]/z:section)"/>

    <!-- Populate even rows with regular items and use the odd rows for inserting
    section delimiters and spacing. The grid is styled so that empty rows take
    up no space.
    -->
    <xsl:variable name="row_idx">
      <xsl:value-of select="count(preceding-sibling::z:type) * 2 + 2"/>
    </xsl:variable>

    <xsl:if test="$is_new_section">
      <xsl:if test="not($is_first_section)">
        <div class="hline"
             style="grid-row:{$row_idx - 1}; grid-column:1/{$column_count + 1}"></div>
      </xsl:if>
      <div class="section" style="grid-row:{$row_idx}; grid-column:1">
        <xsl:copy-of select="z:section/node()"/>
      </div>
    </xsl:if>

    <xsl:apply-templates select="z:*">
      <xsl:with-param name="column_count" select="$column_count"/>
      <xsl:with-param name="row_idx" select="$row_idx"/>
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="z:label|z:text|z:tree">
    <xsl:param name="column_count"/>
    <xsl:param name="row_idx"/>

    <!-- Column to which this item will be assigned -->
    <xsl:variable name="col_idx">
      <xsl:value-of select="count(preceding-sibling::z:section) +
          count(preceding-sibling::z:label) +
          count(preceding-sibling::z:text) +
          count(preceding-sibling::z:tree) + 1"/>
    </xsl:variable>

    <!-- A column span is assigned to the last item in each row in order for
    the item to be able to take up all remaining room without pushing columns
    in other rows that have more columns further out.
    -->
    <xsl:variable name="col_span">
      <xsl:if
          test="not(following-sibling::z:label | following-sibling::z:text | following-sibling::z:tree)">
        <xsl:value-of select="concat('/', $column_count + 1)"/>
      </xsl:if>
    </xsl:variable>

    <xsl:variable name="long_text">
      <xsl:if test=".//*[@class = 'long-text']">
        long-text
      </xsl:if>
    </xsl:variable>

    <!-- The root div that is directly managed by CSS Grid -->
    <div class="grid-item { local-name() } { $long_text }">
      <!-- Position the item by assigning an inline style -->
      <xsl:attribute name="style">
        <xsl:value-of select="concat(
          'grid-row', ':', $row_idx, ';',
          'grid-column', ':', $col_idx, $col_span)"/>
      </xsl:attribute>

      <xsl:copy-of select="./*|text()"/>
    </div>
  </xsl:template>

  <xsl:template name="document_header">
    <head>
      <title>DataONE GMN</title>
      <script
          src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
      <script
          src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
      <link
          href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css"
          rel="stylesheet" type="text/css"/>
      <link href="{concat($static_root_url, 'gmn.css')}"
            rel="stylesheet" type="text/css"/>
    </head>
  </xsl:template>

  <!-- Trim and collapse whitespace in text and attribute nodes.
  Makes for fewer surprises in general. Ensures that duplicated section headers
  are removed even if they were generated with different whitespace.
  -->
  <xsl:template match="*" mode="trim_and_normalize">
    <xsl:copy>
      <xsl:apply-templates mode="trim_and_normalize" select="node()|@*"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="@*" mode="trim_and_normalize">
    <xsl:attribute name="{ name() }">
      <xsl:value-of select="normalize-space(.)"/>
    </xsl:attribute>
  </xsl:template>

  <xsl:template match="text()" mode="trim_and_normalize">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

</xsl:stylesheet>
