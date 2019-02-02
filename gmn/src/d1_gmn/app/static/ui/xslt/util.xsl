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
  <!-- Templates to do basic things in XSLT 1.0.
  Later versions of XSLT, not supported by browsers as of late 2018, have most
  or all of this built in.
  -->

  <!-- max()  -->
  <xsl:template name="max">
    <xsl:param name="sequence"/>
    <xsl:for-each select="exsl:node-set($sequence)/*">
      <xsl:sort data-type="number" order="descending"/>
      <xsl:if test="position()=1">
        <xsl:value-of select="."/>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <!-- url_encode(iso-string)
  Written and put in the public domain by Mike J. Brown, mike@skew.org.
  iso-string: Unicode in the ASCII and ISO-8859-1 ranges (32-126 and 160-255)
  E.g.: <xsl:param name="str" select="'&#161;Hola, C&#233;sar!'"/>
  -->
  <xsl:variable name="ascii">&#x20;!"#$%&amp;'()*+,-./0123456789:;&lt;=&gt;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~</xsl:variable>
  <xsl:variable name="latin1">&#160;&#161;&#162;&#163;&#164;&#165;&#166;&#167;&#168;&#169;&#170;&#171;&#172;&#173;&#174;&#175;&#176;&#177;&#178;&#179;&#180;&#181;&#182;&#183;&#184;&#185;&#186;&#187;&#188;&#189;&#190;&#191;&#192;&#193;&#194;&#195;&#196;&#197;&#198;&#199;&#200;&#201;&#202;&#203;&#204;&#205;&#206;&#207;&#208;&#209;&#210;&#211;&#212;&#213;&#214;&#215;&#216;&#217;&#218;&#219;&#220;&#221;&#222;&#223;&#224;&#225;&#226;&#227;&#228;&#229;&#230;&#231;&#232;&#233;&#234;&#235;&#236;&#237;&#238;&#239;&#240;&#241;&#242;&#243;&#244;&#245;&#246;&#247;&#248;&#249;&#250;&#251;&#252;&#253;&#254;&#255;</xsl:variable>
  <xsl:variable name="safe">
    !'()*-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz~
  </xsl:variable>
  <xsl:variable name="hex">0123456789ABCDEF</xsl:variable>
  <xsl:template name="url_encode">
    <xsl:param name="str"/>
    <xsl:if test="boolean($str)">
      <xsl:variable name="first-char" select="substring($str,1,1)"/>
      <xsl:choose>
        <xsl:when test="contains($safe,$first-char)">
          <xsl:value-of select="$first-char"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:variable name="codepoint">
            <xsl:choose>
              <xsl:when test="contains($ascii,$first-char)">
                <xsl:value-of
                    select="string-length(substring-before($ascii,$first-char)) + 32"/>
              </xsl:when>
              <xsl:when test="contains($latin1,$first-char)">
                <xsl:value-of
                    select="string-length(substring-before($latin1,$first-char)) + 160"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:message>Warning: string contains a character that is out of
                  range! Substituting
                  "?".
                </xsl:message>
                <xsl:text>63</xsl:text>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:variable>
          <xsl:variable name="hex-digit1"
                        select="substring($hex,floor($codepoint div 16) + 1,1)"/>
          <xsl:variable name="hex-digit2"
                        select="substring($hex,$codepoint mod 16 + 1,1)"/>
          <xsl:value-of select="concat('%',$hex-digit1,$hex-digit2)"/>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:if test="string-length($str) &gt; 1">
        <xsl:call-template name="url_encode">
          <xsl:with-param name="str" select="substring($str,2)"/>
        </xsl:call-template>
      </xsl:if>
    </xsl:if>
  </xsl:template>

  <!-- Get the path to the XSLT current context node (for debugging).  -->
  <xsl:template name="get_path">
    <xsl:param name="prev_path"/>
    <xsl:variable name="cur_path" select="concat('/',name(),'[',
      count(preceding-sibling::*[name() = name(current())])+1,']',$prev_path)"/>
    <xsl:for-each select="parent::*">
      <xsl:call-template name="get_path">
        <xsl:with-param name="prev_path" select="$cur_path"/>
      </xsl:call-template>
    </xsl:for-each>
    <xsl:if test="not(parent::*)">
      <xsl:value-of select="$cur_path"/>
    </xsl:if>
  </xsl:template>

  <!-- Friendly format of ISO 8601 datetime with or without timezone
  2006-08-19T11:27:14-06:00 -> 2006-08-19 11:27:14 (06:00)
  yyyy-mm-ddThh:mm:ss.ffffff	 2008-09-15T15:53:00
  yyyy-mm-ddThh:mm:ss.nnnnnn+|-hh:mm	2008-09-15T15:53:00+05:00
  -->
  <xsl:template name="format_date_time">
    <xsl:param name="iso"/>

    <xsl:variable name="dt"
                  select="concat(substring($iso, 1, 10), ' ', substring($iso, 12, 8))"/>

    <xsl:variable name="tz">
      <xsl:choose>
        <xsl:when test="substring($iso, string-length($iso), 1) = 'Z'">
          Z
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of
              select="concat('(', substring($iso, string-length($iso) - 5, 6), ')')"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <xsl:choose>
      <xsl:when test="boolean($tz)">
        <xsl:value-of select="concat($dt, ' ', $tz)"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$dt"/>
      </xsl:otherwise>
    </xsl:choose>

  </xsl:template>


  <xsl:template name="group_thousands">
    <xsl:param name="integer"/>
    <xsl:param name="units"/>
    <xsl:value-of
        select="concat(format-number($integer, '#,###.##', 'US'), ' ', $units)"/>
  </xsl:template>

  <!--Split string-->

  <xsl:variable name="delimiter">
    <xsl:text>:</xsl:text>
  </xsl:variable>

  <xsl:template match="mark">
    <xsl:variable name="dataList">
      <xsl:value-of select="."/>
    </xsl:variable>
    <xsl:call-template name="processingTemplate">
      <xsl:with-param name="datalist" select="$dataList"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="processingTemplate">
    <xsl:param name="datalist"/>
    <xsl:choose>
      <xsl:when test="contains($datalist,$delimiter)  ">
        <xsl:element name="processedItem">
          <xsl:value-of select="substring-before($datalist,$delimiter) * 10"/>
        </xsl:element>
        <xsl:call-template name="processingTemplate">
          <xsl:with-param name="datalist"
                          select="substring-after($datalist,$delimiter)"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="string-length($datalist)=1">
        <xsl:element name="processedItem">
          <xsl:value-of select="$datalist * 10"/>
        </xsl:element>
      </xsl:when>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
