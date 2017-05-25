Installing PostgreSQL
=====================

Install PostgreSQL::

    $ sudo yum -y install postgresql postgresql-devel postgresql-libs postgresql-plpython postgresql-server


Initialize the Database & Configure to start on boot::

    $ sudo postgresql-setup initdb
    $ sudo service postgresql start
    $ sudo chkconfig postgresql on

    $ sudo passwd -d postgres
    $ sudo su postgres -c passwd

    $ sudo -u postgres createuser gmn
    $ sudo -u postgres createdb -E UTF8 gmn2
