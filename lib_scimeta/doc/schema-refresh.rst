Synchronizing the schemas with the Coordinating Node
====================================================

The goal of the `d1_scimeta` Science Metadata validator is to match the validation results of the CN as closely as possible. As such, `d1_scimeta` uses the same set of schemas as that used by the CN, and they are included in the `d1_scimeta` package. If changes are made to the schemas used by the CN, the schemas included in the `d1_scimeta` package should be replaced with a fresh set of schemas from the CN.

The `d1_scimeta` validator is based on the `lxml` library. `lxml` cannot easily be blocked from following HTTP URLs referenced in `schemaLocation` attributes in `xs:include` and `xs:import` elements in XSD schemas used while validating an XML doc. As outgoing network connections and associated delays are not acceptable in many validation scenarios, we use schemas in which URLs have been rewritten to point to existing local XSD files. Or, where there were no existing local XSDs, we include cached versions which were downloaded while preparing the schemas for distribution.

See the `prepare_schema.py` module for details.


Schema syncronization procedure
===============================

Synchronize the XSD files used by the `d1_scimeta` Science Metadata validator with the schemas used by the CN.


- Delete the old schema directory and cache

      $ rm -r ./schema


- Download the new schema files, either from GitHub, or from a CN.

    - GitHub

          https://github.com/NCEAS/metacat/tree/master/lib/schema

    - CN

          $ rsync --recursive cn:/var/lib/tomcat8/webapps/metacat/schema/ ./schema


- Prepare the new schema files for use by `lxml` and create a local cache of schemas not directly included in the CN schema set:

      $ ./prepare_schema.py


- If support for new schemas have been added, add them to the `format_id_to_schema.json` file.


- Run `d1_scimeta` unit tests to ensure that validation still works as expected.


Troubleshooting
===============

As `lxml` is a thin wrapper around the `libxml2` C library, there is no easy way to get insight into the validation process from Python. To help with investigation of validation errors, a command, `resolve_schema.py` is included in `d1_scimeta`. `resolve_schema.py` recursively follows XSD
`xs:include` and `xs:import` elements and lists any issues as they are encountered.
