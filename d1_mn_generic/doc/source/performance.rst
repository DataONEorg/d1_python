Performance
===========

<scratch>


The listObjects call does ordered, sliced and filtered selects from the object
table. The object table should be clustered on mtime. With PostgreSQL, this
can be done with the CLUSTER command::

  cluster object using mtime;
  
PostgreSQL will not automatically keep the table clustered. Instead, the
table must be clustered whenever sufficient changes have been accumulated.

To keep the table clustered for longer, adjust the fill factor.

--

cluster mn_object using mn_object_mtime;

--

analyze

vacuum

~~

The bad is that since there is no additional overhead aside from the usual index
key creation during table inserts and updates, you need to schedule reclustering
to maintain your fine order and the clustering causes a table lock. The annoying
locking hopefully will be improved in later versions. Scheduling a cluster can
be done with a Cron Job or the more OS agnostic PgAgent approach. In another
issue, we'll cover how to use PgAgent for backup and other scheduling
maintenance tasks such as this.
