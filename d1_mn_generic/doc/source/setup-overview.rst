GMN Setup Overview
==================

Overview of the GMN software stack
----------------------------------

:term:`DataONE` :term:`GMN` is web a app implemented in :term:`Python` based on
the :term:`Django` web app framework. Django is a :term:`WSGI` compliant
application. It is served by :term:`Apache` via :term:`mod_wsgi`. The DataONE
infrastructure uses :term:`SSL` and :term:`X.509` :term:`certificate` s for
security and this aspect of GMN is handled by :term:`mod_ssl`.

.. graphviz::

  digraph foo {
    Ubuntu -> Apache -> mod_wsgi -> Django -> GMN
    Apache -> mod_ssl -> "GMN security"
  }


It may be possible to deploy GMN using a different stack, such as one based on
nginx and uwsgi. Such setups are unsuported, but if they are attempted and
prove to have benefits, please let us know.

We will set up the components in the same order as they appear in tree above.


:doc:`setup-hardware`


