Optimizing GMN performance
==========================

Postgres database
~~~~~~~~~~~~~~~~~

Increasing the memory available to Postgres for such things as sorting can dramatically include performance, as Postgres will use the disk as temporary storage if there is not enough memory. In Ubuntu 18.04 with Postgres 10, the default is 4MB. To increase the value, edit work ``work_mem`` in ``postgresql.conf``. E.g.,:

::

  sudo editor /etc/postgresql/10/main/postgresql.conf

- Increase ``work_mem`` from 4MB to 32MB.

The MNRead.listObjects() and MNCore.getLogRecords() API issue ordered, sliced and filtered select statements. The base tables for these operations should be clustered (physically ordered) by the default sort order. Unfortunately, Django does not do this automatically. To cluster the base table for ``MNRead.listObjects()``:

Find the names of the indexes, by running the GMN ``manage.py`` as the ``gmn`` user:

::

  $ sudo -Hu gmn
  $ ./manage.py dbshell
  > \d app_scienceobject

Search for the combined index name ``(modified_timestamp, id)``

Specify clustering on the index:

::

  > cluster app_scienceobject using <index name, e.g., app_science_modifie_76ef91_idx>;

To cluster the base table for ``MNCore.getLogRecords()``, repeat the procedure with ``app_eventlog`` and ``(timestamp, id``).

When successfully completed, ``\d app_scienceobject / app_eventlog`` will display the ``CLUSTERED`` keyword next to the clustered indexes.

Notes:

- Clustering on a large database can take a long time, and queries are not accepted during the process.
- Postgres will not automatically keep the table clustered. Instead, the table must be clustered whenever sufficient changes have been accumulated.
- To keep the table clustered for longer, adjust the fill factor.
- Use cron to schedule automatic clustering. Note that the tables are locked while the clustering operation runs.
- Search the web for Postgres "analyze" and "vacuum" for more information.


Profiling
~~~~~~~~~

When GMN is in debug mode (DEBUG is set to True in the GMN settings.py file), the following profiling functionality is available.


SQL query profiling
-------------------

All REST calls accept a :term:`vendor specific extensions` called
``VENDOR_PROFILE_SQL``. When this parameter is provided, the normal output from the call is suppressed and a text document containing SQL query profiling information is returned instead. The document lists all the SQL queries that were used for filling the request together with execution times.

.. note:: If a REST call returns an exception, the exception is also suppressed.


Python profiling
----------------

All REST calls accept a :term:`vendor specific extensions` called VENDOR_PROFILE_PYTHON. When this parameter is provided, the normal output from the call is suppressed and a text document containing Python script profiling information is returned instead. The document includes information such as the name and location, number of calls and cumulative execution times for the longest running functions.

.. note:: Only the view functions are covered. In particular, response_handler, where the SQL queries are executed, is not covered.
