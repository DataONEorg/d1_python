# Render DataONE XML types as XHTML

This package contains an XSLT transform for DataONE XML types. Output is XHTML intended for display in a browser.

Note: Currently, only types that are returned from v1 and v2 Member Node APIs are supported.

This package is not Python specific but includes a Python script that applies the transform to a set of sample XML documents, stored in `samples/xml`. The resulting XHTML documents are written to `samples/html`. The script depends on the `xsltproc` command line program. It has no Python dependencies outside of the standard library. 
