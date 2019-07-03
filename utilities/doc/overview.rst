The :doc:`/utilities/index` package contains command line utilities for interacting with the DataONE infrastructure.

The utilities are implemented using the DataONE :doc:`Common </common/index>` and :doc:`Client </client/index>` libraries for Python. Effort has been made to keep the implementations clear, in order to allow the utilities to also serve as examples on how to use the DataONE Python libraries.

After setup, binary entry stubs are generated for all the utilities using the a pattern where all `_` and translated to `_`, and `d1-` is prepended to the name. For instance, the module `d1_util/cert_create_csr.py` can be started from the command line with `d1-cert-create-csr`.
