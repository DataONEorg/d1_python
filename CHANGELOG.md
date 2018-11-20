# Change Log

## [3.2.0](https://github.com/DataONEorg/d1_python/tree/3.2.0) (2018-10-15)
[Full Changelog](https://github.com/DataONEorg/d1_python/compare/2.4.2...3.2.0)

* DataONE Generic Member Node (GMN)

  * Added web interface for GMN
    * MN organization highlighted with logo and description 
    * Opening any link at or below the BaseURL of GMN provides a way to reach all publicly available information on the MN. This includes links that do not go to valid endpoints, or are in other ways invalid
    * Functionality includes
      * Links to profile pages on Search for subjects and other MNs
      * Resolve objects on CN, download object from MN, view System Metadata
      * Browse object list and log records, paging forwards and backwards
      * Static links to areas of interest for DataONE

  * Added Apache, Postgres and Python version numbers to GMN status page
  * Reading from the GMN status page with without a browser now returns an XML doc. No need to scrape the page for version numbers and other status information
  * Added multiprocessing to GMN bulk importer
    * 10x speedup seems likely in latency bound systems

  * Added more validation of GMN settings
  * Added migrations to generate Postgres indexes for default sorting  
    * Surprisingly, Django does not generate indexes for default sort ordering specified when using the ORM

  * Reconfigured logging to take advantage of Django's support for rotating logs, much like logrotate does. Maximum space to use for logging is now a config setting.
  * Other usability improvements (see log)

* GMN deployment 

  * Improved and streamline GMN install procedures, including
    * Refactored install so that it can be accomplished in two stages, where only the first stage needs to be performed by account with sudo access

  * Improved and cleaned up Apache conf file
    * Move from Rewrite to Redirect / Alias
    * All redirects are in the same configuration file
      * http -> https, / -> GMN "home", /mn -> v2/node
      
    * Factored repeated paths out 

* Documentation

  * Fixed documentation build warnings and formatting
  * Added SSL/TLS troubleshooting doc, misc other background information
  * Restructured doc layout
  * Refactored shell commands into larger blocks to reduce copy/paste
  * Added more checking and related logic to the blocks to automatically handle more filesystem / OS variations
  * Added Copy buttons for all shell blocks
  * Added docs for
    * How to set up GMN using APT instead of PyPI dependencies
    * How to set up multiple MNs on a single GMN instance
    * How to perform automatic upgrades within GMN 3.x
    * How to cluster tables by index in Postgres to improve GMN perf

  * Added missing glossary entries
  * Upgraded to Sphinx Better theme 0.1.5
 
* DataONE Client and Common Libraries

  * Refactored to improve functionality and take advantage of new functionality in the underlying dependencies
  * Standardized logging in d1_python
  * Consistently use timezone aware datetime objects
  * Removed automatic caching (cachecontrol) in d1_client
  * Disabled retries by default in d1_client
    * Retries are still available, but they're opt-in instead of opt-out.

  * Changed default mimetype for XML from application/xml to text/xml
  * Changed default slice size from 1000 to 100
  * Upgrades of all dependencies

* Tests and test framework

  * Improved support for debugging in PyCharm and factored it out to the test framework
  * Moved to using the PyCharm Diff & Merge tool for viewing sample mismatches
  * Fixed inconsistent normalization of sysmeta replica section

* Developer, working on the DataONE code base

  * Improved documentation on how to work on our code base, such as  
    * Building of GMN DB fixture
    * Using the Responses based DataONE client for debugging GMN    
    * Types of test failures
    * Work with the pre-commit Git hooks
    * Authenticating on Postgres from PyCharm

  * Fixture generator updates, new fixture for Django 2.x
  * Better consistency in logging formats, more information logged

* Developer, using the DataONE libraries

  * Add timezone aware current time functions based on the timezone support that was added in Python 3
  * Cleaner and more consistent interfaces in classes and methods  
  * Documentation describing more corner cases, e.g.,for date-time objects

* Ongoing:
  * Fixing and clean up the Solr client  
  * Reworking the examples / utilities
    * Standardize code layout
    * Add standard set of command line arguments
    * Update to use currently available features in Python 3 and the D1 libs

  * Adding tests for GMN multithreaded bulk importer
  * Adding tests for GMN's XSLT based web UI


## [2.4.2](https://github.com/DataONEorg/d1_python/tree/2.4.2) (2018-02-15)
[Full Changelog](https://github.com/DataONEorg/d1_python/compare/2.4.1...2.4.2)

* DataONE Generic Member Node (GMN)
  * Add SysMeta XML doc to each object returned in BagIt from getPackage()
  * Fix configuration checks performed at startup and improve messages
  * Add option to limit number of objects to import in bulk importer
  * Add tests for settings check performed at GMN startup

* DataONE Client Library
  * Move updateSystemMetadata() to baseclient to make it availble for CN calls

* DataONE Common Library
  * Improve StringIterator to allow for more general usage

* Tests and test framework
  * Add memory_limit context manager and associated test
    * Provides ability to fail unit tests that exceed a given memory usage target
    * Based on psutil, which is added as a new dependency
  * Add workaround for MultipartEncoder bug in Django test client
  * Improve performance in instance generator
    * Skip generating PyXB objects that will not be used in the final SysMeta object
  * Ensure unique media types in test objects
  * Check that dateSysMetadataModified of object obsoleted by update() is set to the GMN server's current datetime

* Misc
  * Update dependencies to current as of 2018-02-15


## [2.4.1](https://github.com/DataONEorg/d1_python/tree/2.4.1) (2017-12-14)
[Full Changelog](https://github.com/DataONEorg/d1_python/compare/2.4.0...2.4.1)

* DataONE Generic Member Node (GMN)
  * Add XML Schema (XSD) validation of incoming Science Metadata documents
    * Applies to calls to MNStorage.create() and MNStorage.update()
    * Controlled by new SCIMETA_VALIDATION_* settings
  * Update jQuery UI to latest and switch from static to hotlinked
  * Fix mistake in cron setup instructions
  * Fix bug that prevented process_refresh_queue from running
  * Improve error handling and logging in bulk importer

* DataONE Common Library
  * Add new package for validating Science Metadata
    * The required schemas are included in the package
  * Improve error handling in multiprocessed iterators
  * Misc refactoring

* Tests and test framework
  * Misc smaller test framework improvements
  * Add basic test for GMN home/status page

* Misc  
  * Update dependencies to current as of 2017-12-06
  * Remove accidentally added duplicates

## [2.4.0](https://github.com/DataONEorg/d1_python/tree/2.4.0) (2017-11-16)
[Full Changelog](https://github.com/DataONEorg/d1_python/compare/2.3.8...2.4.0)

* DataONE Generic Member Node (GMN)
  * Fix ServiceFailure caused by some `listObjects()` and `getLogRecords()` slice requests
  * Fix datetimes in DataONE types sometimes returned as naive instead of in the UTC timezone
  * Add support for returning BagIt zip archives from `getPackage()`
    * BagIt objects are generated directly as streams, so arbitrarily sized BagIt archives can be requested and latency is the same as for regular `get()`  
  * Reverse the ordering of `ObjectList` (`listObjects()`) and `Log` (`getLogRecords()`)
    * Now ordered by modified timestamp, ascending, then identifier, ascending
  * Add limit to the maximum number of items that can be returned in a single slice
    * Adjustable via new `MAX_SLICE_ITEMS` setting, 5000 by default
  * Add fallback to default settings
    * Allows new settings to be added without requiring admins to add the new settings into their local settings.py after GMN upgrade
  * Add support for API calls without HTTP User Agent header in GMN
    * Such calls may be generated by custom, "one-off" clients
  * Fixes related to `create()` and `update()` of resource maps and their aggregated objects
    * "block" and "open" modes implemented as described in `RESOURCE_MAP_CREATE` in `settings_template.py`
    * Allow multiple Resource Maps to aggregate the same PID and each other
    * Allow Resource Maps to aggregate non-local and possibly non-existing objects
  * Rework internal representation and handling of revision chains
  * Update bulk importer for handling of out-of-order revisions
  * Refactoring
    * Split up input validation related functionality
    * identifier related functionality
    * Misc

* DataONE Common Library
  * Add AccessPolicyWrapper, a wrapper for the AccessPolicy DataONE type adds type specific and intuitive methods directly on the object
    * Add SimpleXMLWrapper, similar functionality for XML
    * These abstract away the details of the types and provide for concise and intuitive code
    * We plan on implementing such wrappers for all relevant types
  * Add new subpackage for generators
    * string generator
    * file contents generator
  * Add module for generating and validating BagIt streams
  * Add utilities for basic XML parsing
  * Improve utilities for comparing and normalizing XML
  * New date-time functions to better handle timezones

* DataONE Client Library
  * Improve error handling in multiprocessed iterators

* Tests and test framework
  * Add around 300 tests since 2.3.8.
  * Add support for running tests in parallel with `pytest.xdist`
    * Run of test set, currently around 1100 tests, reduced from 7 to 2 min on dev machine
    * Each worker runs against a separate copy of the GMN database, instantiated from shared template
  * Add context managers for setting the CRUD whitelist
  * Add module that calls DataONE APIs in GMN without using PyXB
    * Gives the ability to generate and check response to invalid requests, such as requests with incorrectly formatted URLs, multipart documents, and DataONE types  
  * Add ability to skip recently passed tests
    * Controlled with `--skip` and related test args
    * Default is to not skip
  * Speed up slice tests
  * Better support for timezones in date_time instance generator
  * Add misc functions for working with random lists in instance generator
  * Fix "flaky" test
    * Failed on some combinations of values in the underlying randomly generated type
  * Misc other smaller test framework improvements

* Misc
  * Update dependencies to current as of 2017-11-16
  * Better timezone support throughout d1_python

## [2.3.8](https://github.com/DataONEorg/d1_python/tree/2.3.8) (2017-10-20)
[Full Changelog](https://github.com/DataONEorg/d1_python/compare/2.3.6...2.3.8)

* DataONE Generic Member Node (GMN)
  * Add support for storing partial and out-of-order revision chains
    * Automatically combine chain fragments that are found to be part of the
    same chain
    * Tests for various revision and SID related corner cases
  * Add migrations to latest db  
  * Improve progress information in management commands
  * Add diagnostics management command to migrate and repair revision chains
  * Add support for general migrations to bulk importer
  * Remove old migrate_v1_to_v2 command
  * Update database test fixtures and sample docs

* DataONE Client Library
  * Add multiprocessed log record iterator
  * Refactor multiprocessed iterators to improve reliability
  * Add API v1.2 MN method wrappers (view and package methods)

* DataONE Common Library
  * Add misc methods, docstrings and tests to access_policy module
  * Update PyXB bindings to PyXB 1.2.6 and update generator script

* Misc
  * Update dependencies to current as of 2017-10-20


## [2.3.6](https://github.com/DataONEorg/d1_python/tree/2.3.6) (2017-08-24)
[Full Changelog](https://github.com/DataONEorg/d1_python/compare/2.3.5...2.3.6)

* DataONE Generic Member Node (GMN)
  * Add extended listObjects() API
      * Fast method for retrieving large number of selected sysmeta values
      * Returns JSON
      * Quickly generated and parsed
      * No schema
      * Minimal document size
      * Part of a new API class, "ext", which will holds GMN specific APIs
  * Optimize slicing / paging of multi-page result sets
  * Add support for proxied objects in bulk importer
  * Add support for rejecting replication requests for non-public objects
  * Add Proxy, Obsoletes, ObsoletedBy and SeriesId to the custom headers returned by most D1 API methods
    * Proxy header allows clients to determine if an object is proxied and, if so, where the original object resides
    * Obsoletes, ObsoletedBy headers allow clients to determine if object is part of a revision chain
  * Keep track of ownership and versioning of sciobj filesystem store
  * Check every minute instead of every hour for new replication and sysmeta refresh tasks
  * Ongoing refactoring of diagnostics

* DataONE Client Library
  * Add support for disabling timeout by passing timeout=None, 0 or 0.0

* Tests and test framework
  * Add various small unit test improvements
  * Add automatic migration of test database
  * Update samples
  * Ensure that files deleted after previous build are not included in later releases

* Misc
  * Update dependencies to current as of 2017-08-24

## [2.3.5](https://github.com/DataONEorg/d1_python/tree/2.3.5) (2017-08-08)
[Full Changelog](https://github.com/DataONEorg/d1_python/compare/2.3.4...2.3.5)

* DataONE Generic Member Node (GMN)
  * Add general bulk importer management command
    * Allows upgrading from any earlier version of GMN or other MN stack
  * Add cleardb diag management command
    * Remove cleardb from the diags page
    * Start code for other "diag" management commands
  * Improve the way that chains are represented in the db
    * Less code and faster SID related queries
  * Update revision change related model name
    * After earlier modifications in how the chains are represented, the old names were misleading
  * Add SID filtering support
      * Add support for passing SID as the getLogRecords() idFilter and listObjects() identifier args
      * Note: We don't resolve SIDs for v1, so the v1 pidFilter argument cannot take a SID.
      * Add tests for SID filtering
  * Fix bug: Unable to run management commands
  * Update node registration doc to reflects updated manage.py commands

* DataONE Client Library
  * Add support for v2 CNRead.synchronize()
  * Expose a ".total" attribute in iterators
    * Clients can read the value from .total to keep track of progress. Earlier, clients had to perform a separate query using filter parameters matching those used by the iterator. There was also a potential race, in that the total could change between query by the iterator and by the client.
  * Change iterator arguments:
    * ObjectListIterator: listObjects_args_dict -> list_objects_args
    * LogRecordIterator: getLogRecords_dict -> get_log_records_arg_dict
  * Add get_and_save() wrapper for MNRead.get()
    * This is a convenience method added because correctly saving the result from get() to a file is a bit tricky, while it is also the most common use of get().
  * Add option to create missing directories for MNRead.get_and_save()
  * Add description on how to use stream=True with MNRead.get()

* DataONE Common Library
  * Add module for handling obsolescence chains / revisions
    * `d1_common/revision.py`
  * Rename methods for creating missing directory names
    * `d1_common/util.py`
  * Add default page size of 100 records for getLogRecords()
    * `d1_common/const.py`
  * Update default User-Agent to DataONE_Python/x.y.z +http://dataone.org/
  * Add misc type related utilities to d1_common
    * `d1_common/type_conversions.py`, etc.

* Tests and test framework
  * Add section in README.md about db fixtures for GMN, how they're used, how to generate them
    * Improve procedure for regenerating db fixture
  * Add mock API handlers
    * MNCore.getCapabilities()
    * CNCore.listNodes()
  * Fix bug: SID did not resolve correctly
    * Add tests for SID resolve
  * Add handling of db where migrations are out of sync in fixture generator
  * Add script that checks scimeta indexing

* Misc
  * Update dependencies to current as of 2017-08-07
