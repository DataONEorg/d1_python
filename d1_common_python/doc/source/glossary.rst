.. glossary::


  DataONE Common Library for Python
    Part of the DataONE :term:`Investigator Toolkit (ITK)`. Provides
    functionality commonly needed by projects that interact with the
    :term:`DataONE` infrastructure via Python. It is a dependency of
    :term:`DataONE Client Library for Python`, :term:`GMN` and all other DataONE
    components written in Python.


  DataONE Client Library for Python
    Part of the DataONE :term:`Investigator Toolkit (ITK)`. Provides
    programmatic access to the DataONE infrastructure and may be used to form
    the basis of larger applications or to extend existing applications
    to utilize the services of DataONE.


  DataONE
    Data Observation Network for Earth

    https://dataone.org


  Investigator Toolkit (ITK)
    The Investigator Toolkit provides a suite of software tools that are useful
    for the various audiences that DataONE serves. The tools fall in a number of
    categories, which are further developed here, with examples of potential
    applications that would fit into each category.

    http://mule1.dataone.org/ArchitectureDocs-current/design/itk-overview.html


  GMN
    DataONE Generic Member Node

    GMN is an implementation of a :term:`MN`. It provides an implementation
    of all MN APIs. GMN can be used as a as a workbone or as a reference for a
    3rd party MN implementation. GMN can also be used as an "adapter", making it
    possible for a 3rd party system to become a MN and expose its objects to
    DataONE with a minimum of effort. In this mode, we refer to GMN as the
    adapter and the 3rd party system as the adaptee.

    When used as an adapter, GMN provides a minimal REST API that the adaptee
    can call into to expose its objects, in a process we refer to as object
    registration. After registration, GMN exposes objects on behalf of the
    :term:`adaptee`.

  MN
    DataONE Member Node.


  Adaptee
    A 3rd party system that uses GMN to expose its data through DataONE.
  

  Subversion
    Version control system
    
    http://subversion.apache.org/


  Bash
    GNU Bourne-Again Shell
    
    http://www.gnu.org/software/bash/


  PyXB
    Python XML Schema Bindings
    
    http://pyxb.sourceforge.net/


  lxml
    A library for processing XML and HTML with Python
  
    http://lxml.de/


  minixsv
    A Lightweight XML schema validator
    
    http://www.familieleuthe.de/MiniXsv.html


  python-dateutil
    Extends the standard datetime module
    
    http://labix.org/python-dateutil


  setuptools
    A package manager for Python
  
    http://pypi.python.org/pypi/setuptools
  

  ISO8601
    International standard covering the exchange of date and time-related data
    
    http://en.wikipedia.org/wiki/ISO_8601
    
  python-iso8601
    Python library implementing basic support for :term:`ISO8601`
    
    http://pypi.python.org/pypi/iso8601/



    