:term:`DataONE` :term:`GMN` is a web app implemented in :term:`Python` based on
the :term:`Django` web app framework. Django is a :term:`WSGI` compliant
application. It is served by :term:`Apache` via :term:`mod_wsgi`. The DataONE
infrastructure uses :term:`SSL` and :term:`X.509` :term:`certificate`\ s for
security and certificate validation is handled for GMN by :term:`mod_ssl`.

.. graphviz::

  digraph G {
    dpi=72;
    OS -> "DataONE Common" -> "DataONE Client" -> GMN;
    "DataONE Common" -> GMN;
    OS -> Apache -> mod_wsgi -> Django -> GMN;
    Apache -> mod_ssl -> "GMN access control" -> GMN;
  }
