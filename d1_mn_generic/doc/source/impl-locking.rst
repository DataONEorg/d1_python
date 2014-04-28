Locking and concurrency
=======================

Locking and concurrency in GMN is based on Django's implementation of implicit
database transactions, enabled by setting ``ATOMIC_REQUESTS`` to True in the
database connection setup.

Django wraps each HTTP request in an implicit transaction. The transaction is
rolled back if the request does not complete successfully. Upon a successfully
completed request, the transaction is committed, thus making all modifications
that the request made to the database visible simultaneously, bringing the
database directly from one valid state to the next.

Transactions are also used in read-only requests as they hide any transitions
between valid states that may happen during the processing of multiple database
transactions during a single request.

