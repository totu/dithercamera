<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="utf-8" indent="yes" />
<xsl:template match="/">
    <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html&gt;</xsl:text>
    <html>
    <head>
        <title><xsl:value-of select="$title" /></title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style>
        img, video {
            display: inline-block;
            margin: 0.25em;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        html, body {
            margin: 0.25em;
        }
        </style>
    </head>
    <body>
        <xsl:for-each select="list/directory">
          <p>
		  <a href="{.}">Directory: <xsl:value-of select="." /></a>
          </p>
        </xsl:for-each>
        <xsl:for-each select="list/file">
            <xsl:sort select="position()" data-type="number" order="descending"/>
            <xsl:choose>
                <xsl:when test="contains(' mp4 webm mkv avi wmv flv ogv ', concat(' ', substring-after(., '.'), ' '))">
                    <video controls="" src="{.}" alt="{.}" title="{.}"/>
                </xsl:when>
                <xsl:otherwise>
                  <a href="{.}">
                    <img src="{.}" alt="{.}" title="{.}"/>
                  </a>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </body>
    </html>
</xsl:template>
</xsl:stylesheet>

