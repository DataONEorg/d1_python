DataONE Test Utilities
======================

Various utilities useful for testing within the DataONE infrastructure.


create_dataone_test_certificate.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a DataONE compliant certificate. The certificate can optionally include
a SubjectInfo XML document in which equivalent identities and group
memberships are described. The certificate will normally be signed with a test
CA that is trusted by a test instance of a Member Node. Test instances set up
by DataONE will normally trust the DataONE Test CA.

::

  Options:
    -h, --help            show this help message and exit
    --subject-info-path=SUBJECT_INFO_PATH
    --subject-alt-name=SUBJECT_ALT_NAME
    --long-term           Create a certificate that is valid for 10 years
    --ca-path=CA_PATH
    --ca-key-path=CA_KEY_PATH
    --ca-key-pw=CA_KEY_PW
    --public-key-path=PUBLIC_KEY_PATH
    --verbose

Example::

  ./create_dataone_test_certificate.py --ca-path test_files/ca_test.crt
  --ca-key-path test_files/ca_test.key --ca-key-pw ca_test --public-key-path
  test_files/new_cert_public_key.pem --subject-info-path
  test_files/subject_info.xml 'CN=my name,O=mydomain,DC=com'


d1_test_case.py
~~~~~~~~~~~~~~~

Extend unit tests with methods for checking DataONE types.


generate_sysmeta_for_sciobj.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate randomized System Metadata for a Science Object. Used for preparing
a object for inserting into a Member Node that holds tests objects.

::

  export OBJECT=/some/file
  generate_sysmeta.py -f $OBJECT \
                      -i "Some_Identifier" \
                      -s "CN=My Name,O=Google,C=US,DC=cilogon,DC=org" \
                      -t "some_format"



generate_test_subject_certs.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create set of test certificates. The certificates will normally be signed by
the DataONE Test CA so that they can be used for authenticating on test
instances of DataONE nodes.


list_effective_subjects.py
~~~~~~~~~~~~~~~~~~~~~~~~~~

Given a DataONE X.509 v3 Certificate, list all subjects, equivalent
identities and groups for which the certificate holder is authenticated.

::

  Usage: list_effective_subjects.py [options] <certificate>

  Options:
    -h, --help  show this help message and exit
    --verbose



urlencode.py
~~~~~~~~~~~~

Url encode or decode a string passed on the command line.

Used for manually preparing arguments for REST calls.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
