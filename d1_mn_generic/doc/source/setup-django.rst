Step 7: Django
===============

==================== ==============================================
Component            Minimum Version
==================== ==============================================
Django               1.3
==================== ==============================================


Because the packaged version of Django for Ubuntu is often behind the latest
release, we install Django from source.

Set up staging area::

  $ mkdir ~/djangoinstall
  $ cd ~/djangoinstall

Download the latest version of Django from
https://www.djangoproject.com/download/

::

  $ wget http://media.djangoproject.com/releases/1.3/Django-1.3.tar.gz  

Uncompress and install::  

  $ tar xzvf Django-1.3.tar.gz
  $ cd Django-1.3
  $ sudo python setup.py install

:doc:`setup-d1-gmn`
