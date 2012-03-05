PID level locking
=================

The PID level locking is thread based.

Disadvantages:

- Apache must be configured to use a single process with multiple threads. This
  configuration is server wide.
- If multiple processes are used, the PID locking will fail silently. The errors
  caused by this would not be easily reproducible and would include random
  corruption of system metadata, crashes and incorrect data returned.

Advantages:

- As the locks are held in memory, this locking method is fast.
- There is no need to remove potential residual locks at startup.

Notes:

- The method uses a dictionary of locking objects. At the beginning and end of
  each view, the view briefly holds an exclusive lock on the dictionary itself.
  While the main section of the view is running, it holds a read or write lock
  on the PID it operates on. These locks are stored in the dictionary. The
  locking objects serialize the views in such a way that all methods that read
  information from a given PID can run concurrently while writing blocks access
  to all other readers and writers.

- This locking method serializes calls instead of returning "Retry" exceptions.

The potential issues are:

- Performance issues in Apache related to running a single process with multiple
  threads. 

- Inability to change Apache configuration because Apache is running other web
  apps.

Note: Under Windows, Apache uses a multi-process manager (MPM) called "winnt".
This MPM always uses a single process with multiple threads.

If another type of locking must be implemented, some issues to consider are:

When storing locks in the database:

- Does not implicitly support serialization of calls; it becomes more natural to
  raise "Retry" exceptions.

- Becomes harder to support multiple concurrent readers.

- The transaction management middleware layer in Django wraps updates performed
  by a view in a transaction. When storing locks in the database, updates to the
  locks must become visible to other views before they start their own
  processing, which makes it incompatible with the transaction middleware.


Optimistic locking
------------------

It may be that an optimistic locking scheme is best for GMN, as there will be
low contention during regular operation.

Potential issues:

- Optimistic locking is mainly used where the result of processing is store in
  an atomic operation. When operating on data both on the file system and in the
  database, updates can not be atomic, so each view must be aware that it may be
  processing information that is concurrently being updated and must fail
  gracefully if the data is not what is expected.

- Optimistic locking causes "Retry" exceptions instead of serialization.


Django and multi-threading
--------------------------

Django was not initially written to support multi-threading. The only supported
mode when running Django under Apache was the "prefork" MPM, which runs each
Django instance in a separate process. There is much discussion online about
issues related to Django and multi-threading. However, almost all of these
relate to versions of Django prior to version 1.0. Support for multi-threading
was constantly being worked on and was mostly resolved as of version 1.0. As of
version 1.3, there are two known multi-threading issues in Django itself but
these refer to corner cases in poorly written apps.


Resources
---------

https://github.com/stdbrouw/django-locking

Python native: multiprocessing.managers.SyncManager

http://stackoverflow.com/questions/320096/django-how-can-i-protect-against-concurrent-modification-of-data-base-entries

https://groups.google.com/group/django-developers/browse_frm/thread/905f79e350525c95/dfed56f8ed65aed2

http://groups.google.com/group/django-users/browse_thread/thread/e882e25271e667d9/95d52fc57b82e189

http://en.wikipedia.org/wiki/Django_%28web_framework%29#Server_arrangements
