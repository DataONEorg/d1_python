# Change Log

## [2.3.5](https://github.com/DataONEorg/d1_python/tree/2.3.5) (2017-08-08)
[Full Changelog](https://github.com/DataONEorg/d1_python/compare/2.3.4...2.3.5)

* Update all dependencies to current versions as of 2017-08-07

* Add general bulk importer management command
    * Allows upgrading from any earlier version of GMN or other MN stack

* Add shared module for handling obsolescence chains / revisions
    * `d1_common/revision.py`

* Rename methods for creating missing directory names
    * `d1_common/util.py`

* Add default page size of 100 records for getLogRecords()
    * `d1_common/const.py`

* Expose a ".total" attribute in iterators
    * Clients can read the value from .total to keep track of progress. Earlier, clients had to perform a separate query using filter parameters matching those used by the iterator. There was also a potential race, in that the total could change between query by the iterator and by the client.

* Change iterator arguments:
    * ObjectListIterator: listObjects_args_dict -> list_objects_args
    * LogRecordIterator: getLogRecords_dict -> get_log_records_arg_dict

* Add get_and_save() wrapper for MNRead.get()
    * This is a convenience method added because correctly saving the result
from get() to a file is a bit tricky, while it is also the most common
use of get().
    * Add option to create missing directories for MNRead.get_and_save()

* Add section in README.md about db fixtures for GMN, how they're used, how to generate them
    * Improve procedure for regenerating db fixture

* Add mock API handlers
    * MNCore.getCapabilities()
    * CNCore.listNodes()

* Fix bug: SID did not resolve correctly
    * Add tests for SID resolve

* Update default User-Agent to DataONE_Python/x.y.z +http://dataone.org/

* Add misc type related utilities to d1_common
    * `d1_common/type_conversions.py`, etc.

* Add support for v2 CNRead.synchronize()

* Add description on how to use stream=True with MNRead.get()

* Add handling of db where migrations are out of sync in fixture generator

* Add cleardb diag management command
    * Remove cleardb from the diags page
    * Start code for other "diag" management commands

* Improve the way that chains are represented in the db
    * Less code and faster SID related queries

* Update revision change related model name
    After earlier modifications in how the chains are represented, the old
names were misleading.

* Add SID filtering support
    * Add support for passing SID as the getLogRecords() idFilter and listObjects() identifier args.
    * Note: We don't resolve SIDs for v1, so the v1 pidFilter argument cannot take a
SID.
    * Add tests for SID filtering

* Fix bug: Unable to run management commands

* Update node registration doc to reflects updated manage.py commands

* Add script that checks scimeta indexing

* Misc refactoring and internal improvements  
