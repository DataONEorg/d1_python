Installing d1_libclient_python
==============================

Note that ``d1_libclient_python`` is in the early stages of development and will
likely change significantly over time. 

Use it at your own risk of frustration.

The simplest way to utilize the library is to check out the source from 
subversion and work from there.  This makes it easy to keep up to date with
changes.

A package will be released at some point in the future once things stabilize 
a bit.

To set things up in ``$HOME/dataone-python``::

  mkdir $HOME/dataone-python
  cd $HOME/dataone-python
  svn co https://repository.dataone.org/software/cicore/trunk/api-common-python
  svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python
  export PYTHONPATH="$PWD/api-common-python/src:$PWD/d1-python/src:$PYTHONPATH"
  cd d1-python/src
  python d1cli.py --help


Use the usual ``svn update`` operations to update your copy.
