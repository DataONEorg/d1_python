ObjectFormatInfo
================

Map DataONE ObjectFormatIDs to mimetype and filename extension.

As part of the metadata for a science object, DataONE stores a type identifier called an Object Format ID. Many client utilities need a mimetype to determine how to process or display the object and/or a filename extension for use when saving the object to a local file. This module provides convenient functions for performing such mappings.

By default, ObjectFormatInfo uses DataONE's standard table of mappings. If desired, a custom table can be provided.
