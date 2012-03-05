GMN setup overview
==================

Overview of the GMN software stack
----------------------------------

:term:`DataONE` :term:`GMN` is a web app implemented in :term:`Python` based on
the :term:`Django` web app framework. Django is a :term:`WSGI` compliant
application. It is served by :term:`Apache` via :term:`mod_wsgi`. The DataONE
infrastructure uses :term:`SSL` and :term:`X.509` :term:`certificate`\ s for
security and certificate validation is handled for GMN by :term:`mod_ssl`.

.. graphviz::

  digraph G {
    OS -> Apache -> mod_wsgi -> Django -> GMN;
    Apache -> mod_ssl -> "GMN access control";
  }


It may be possible to deploy GMN using a different stack, such as one based on
`nginx <http://nginx.net/>`_ and `uWSGI
<http://projects.unbit.it/uwsgi/wiki/>`_. Such setups are currently untested,
but if they are attempted and prove to have benefits, please let us know.

