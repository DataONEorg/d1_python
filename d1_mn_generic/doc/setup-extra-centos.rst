Installing on CentOS 5.5
========================

The following instructions for setting GMN up on CentOS should be considered in
the context of the setup documentation that is provided for Ubuntu. Study the
setup instructions for Ubuntu first and use the information below to adapt that
information for a CentOS install.

Platform
--------

Install required packages (some of these may already be installed)::

  $ sudo yum install python26 sqlite mod_wsgi openssh-server libxml2-devel libxslt-devel python26-devel Django python-iso8601

(Verify if these are needed)::

  $ sudo yum install python26-tools (may not be necessary, but gives you tk/tcl)
  $ sudo yum install python-sqlite2 (may be incorrect....)


Python
------

CentOS requires Python 2.4 while Django and GMN requires Python 2.7. These
requirements are met by installing the two versions of Python side by side and
making sure that Python 2.7 is used by Django and the GMN scripts.

  Install :term:`python-setuptools`::

    $ sudo yum install python26-setuptools python26-setuptools-devel

  Verify easy_install installed correctly::

    $ easy_install

  Create staging area::

    $ mkdir ~/building

  Install :term:`lxml`::

    $ cd ~/building
    $ wget http://dl.iuscommunity.org/pub/ius/stable/Redhat/5/i386/python26-lxml-2.0.11-1.ius.el5.i386.rpm
    $ rpm -i python26-lxml-2.0.11-1.ius.el5.i386.rpm

  Install :term:`PyXB`::

    $ cd ~/building
    $ wget http://surfnet.dl.sourceforge.net/project/pyxb/pyxb/1.1.2%20%28Beta%29/PyXB-base-1.1.2.tar.gz
    $ tar xzf PyXB-base-1.1.2.tar.gz
    $ cd PyXB-1.1.2/
    $ sudo python setup.py install

  Install :term:`minixsv`::

    $ cd ~/building/
    $ wget http://www.familieleuthe.de/minixsv/minixsv-0.9.0.tar.gz
    $ tar xzf minixsv-0.9.0.tar.gz
    $ cd minixsv-0.9.0
    $ sudo python26 setup.py install


GMN
---

Install GMN as described in the instructions for Ubuntu. Then modify GMN to
explicitly use Python 2.7. This is needed because CentOS includes Python 2.4
and used that version by default.

Files that must be modified::

  ./install/config.py:       63 res = os.system('/usr/bin/python26 ./manage.py syncdb')
  ./service/mk_fixtures.py:  23 print os.system('/usr/bin/python26 ./manage.py syncdb')
  ./service/mk_fixtures.py:  24 print os.system('/usr/bin/python26 ./manage.py update_db')
  ./service/mk_fixtures.py:  25 print os.system('/usr/bin/python26 ./manage.py insert_test_log')
  ./service/mk_fixtures.py:  39   cmd = '/usr/bin/python26 ./manage.py dumpdata {0} > \'{1}\''.format(app, os.path.join(fixture_dir, 'base.fixture.json'))
  ./install/config_util.py:  60 run(['/usr/bin/python26','./manage.py', 'set_node_val', key, val])

CentOS stores mod_wsgi.so in a different location than Ubuntu. Modify configuration script accordingly::

  ./install/config.py:       88 parser.add_option('-w', '--mod-wsgi-path', dest='mod_wsgi_path', action='store', type='string', default='/etc/httpd/modules/mod_wsgi.so')

Modified other \*.py files that execute other scripts to call python26.

Run the GMN install script under Python 2.7::

  $ sudo python26 ../install/config.py
