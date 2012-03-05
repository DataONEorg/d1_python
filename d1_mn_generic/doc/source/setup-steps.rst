Setup steps
===========

The GMN setup process has been broken down into a series of steps. Perform
the steps in order to set up a working instance of GMN.

Along with the steps, some background information is provided. The actual steps
that need to be performed are indented to separate them from the background
information.

Commands that need to be run from the shell are prefixed with "$" or "#". "$"
specifies that the command can be run as a regular user, while "#" specifies
that it must be run as root.

\

.. toctree::
  :maxdepth: 1

  setup-hardware
  setup-apache
  setup-mod-wsgi
  setup-mod-ssl
  setup-authn-server
  setup-authn-client
  setup-python-deps
  setup-d1-libs
  setup-postgresql
  setup-psycopg2
  setup-django
  setup-x509extract
  setup-d1-gmn
  setup-registration
  setup-workers
  setup-startup
