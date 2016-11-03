Optimizing GMN performance
==========================

Database
~~~~~~~~

The MNRead.listObjects() call does ordered, sliced and filtered selects from the
object table. The object table should be clustered on mtime. With PostgreSQL,
this can be done with the CLUSTER command::

  > cluster mn_object using mtime;

MNCore.getLogRecords() can be optimized in the same ways as MNRead.listObjects().

The mn_event_log should be clustered on date_logged::

  > cluster mn_event_log using date_logged

* PostgreSQL will not automatically keep the table clustered. Instead, the
  table must be clustered whenever sufficient changes have been accumulated.

* To keep the table clustered for longer, adjust the fill factor.

* Use cron to schedule automatic clustering. Note that the tables are locked
  while the clustering operation runs.

* Search the web for PostgreSQL "analyze" and "vacuum" for more information.


Profiling
~~~~~~~~~

When GMN is in debug mode (DEBUG is set to True in the GMN settings.py file),
the following profiling functionality is available.

SQL query profiling
-------------------

All REST calls accept a :term:`vendor specific extensions` called
``VENDOR_PROFILE_SQL``. When this parameter is provided, the normal output from
the call is suppressed and a text document containing SQL query profiling
information is returned instead. The document lists all the SQL queries that
were used for filling the request together with execution times.

..note:: If a REST call returns an exception, the exception is also supressed.


Python profiling
----------------

All REST calls accept a :term:`vendor specific extensions` called
VENDOR_PROFILE_PYTHON. When this parameter is provided, the normal output from
the call is suppressed and a text document containing Python script profiling
information is returned instead. The document includes information such as the
name and location, number of calls and cumulative execution times for the
longest running functions.

..note:: Only the view functions are covered. In particular, response_handler,
where the SQL queries are executed, is not covered.
