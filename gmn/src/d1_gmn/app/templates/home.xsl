<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/1999/xhtml"
                exclude-result-prefixes="xsl"
                extension-element-prefixes=""
                version="1.0"
>
  {% load static %}

  <xsl:import href="{% static '/ui/xslt/xhtml_grid.xsl' %}"/>

  <xsl:output doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
              doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
              encoding="utf-8" indent="yes" method="xml"/>

  <xsl:param name="static_root_url">{% static '/' %}</xsl:param>
  <xsl:param name="base_url">{{ baseUrl }}/</xsl:param>
  <xsl:param name="env_root_url">{{ envRootUrl }}/</xsl:param>
  <xsl:param name="search_root_url">{{ searchRootUrl }}/</xsl:param>
  <xsl:param name="node_id">{{ nodeId }}</xsl:param>
  <xsl:param name="mn_logo_url">{{ mnLogoUrl }}</xsl:param>
  <xsl:param name="node_name">{{ nodeName }}</xsl:param>
  <xsl:param name="d1_logo_url">{% static 'images/d1_logo.png' %}</xsl:param>
  <xsl:param name="gmn_logo_url">{% static 'images/gmn_logo.png' %}</xsl:param>

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
        <div class="container">
          <!--<div class="flex-head">-->
          <div class="container-grid">
            <div class="header-left">
            </div>
            <div class="header-right">
            </div>

            <div class="sidebar">
              <div class="flex-vert">

                <!--left panel top-->
                <div>
                  <div class="nav-outer">
                    <div class="mn-logo">
                      <xsl:call-template name="insert_logo">
                        <xsl:with-param name="url" select="$mn_logo_url"/>
                      </xsl:call-template>
                    </div>
                  </div>

                  <div class="nav-outer">
                    <div>
                      <a class="nav-button"
                         href="{ concat($base_url, 'home') }">
                        Status
                      </a>
                    </div>
                    <div>
                      <a class="nav-button"
                         href="{ concat($base_url, 'v2/node') }">
                        Node
                      </a>
                    </div>
                    <div>
                      <a class="nav-button"
                         href="{ concat($base_url, 'v2/object') }">
                        Objects
                      </a>
                    </div>
                    <div>
                      <a class="nav-button"
                         href="{ concat($base_url, 'v2/log') }">
                        Events
                      </a>
                    </div>
                  </div>

                  <div class="nav-outer">
                    <div class="d1-logo">
                      <xsl:call-template name="insert_logo">
                        <xsl:with-param name="url" select="$d1_logo_url"/>
                      </xsl:call-template>
                    </div>
                    <div>
                      <a class="nav-button"
                         href="https://search.dataone.org/data">
                        Search
                      </a>
                    </div>
                  </div>

                  <div class="nav-outer">
                    <a class="nav-link" href="http://dataone.org">
                      DataONE.org
                    </a>
                    <a class="nav-link"
                       href="https://www.dataone.org/what-dataone">
                      About DataONE
                    </a>
                    <a class="nav-link"
                       href="https://www.dataone.org/current-member-nodes">
                      Member Nodes
                    </a>
                  </div>

                  <div class="nav-outer">
                    <div class="gmn-logo">
                      <xsl:call-template name="insert_logo">
                        <xsl:with-param name="url">
                          {% static 'images/gmn_logo.png' %}
                        </xsl:with-param>
                      </xsl:call-template>
                    </div>
                    <a class="nav-link"
                       href="https://dataone-python.readthedocs.io/en/latest/gmn/index.html">
                      Documentation
                    </a>
                    <a class="nav-link"
                       href="https://github.com/DataONEorg/d1_python">
                      DataONE Python
                    </a>
                  </div>
                </div>
              </div>

              <!-- left panel bottom -->
              <!--<div>-->
              <!--</div>-->
            </div>

            <!--right panel-->
            <div class="flex-vert">
              <div>
                <div class="nav-outer">
                  <div class="mn-name">
                    <xsl:value-of select="$node_name"/>
                  </div>
                </div>
                <div class="nav-outer">
                  <div class="d1-type">
                    <xsl:call-template name="d1_type_to_xhtml_grid"/>
                  </div>
                </div>
              </div>
            </div>

            <!-- right panel bottom -->
            <!--<div>-->
            <!--</div>-->

            <div class="footer">
              <div class="copyright">
                Copyright © 2018 Participating institutions in DataONE
              </div>
            </div>

          </div>
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template name="document_header">
    <head>
      <title>
        <xsl:value-of select="$node_name"/>
      </title>
      <script
          src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"
          type="text/javascript"/>
      <link href="{% static '/ui/d1type.css' %}" rel="stylesheet"
            type="text/css"/>
      <script src="{% static '/ui/d1type.js' %}" type="text/javascript"/>
    </head>
  </xsl:template>

  <!-- Insert logo while falling back to GMN logo if fetch from url fails -->
  <xsl:template name="insert_logo">
    <xsl:param name="url"/>
      <img class="logo" src="{ $url }" onerror="this.src='{ $gmn_logo_url }'" alt="logo"/>
  </xsl:template>

</xsl:stylesheet>
