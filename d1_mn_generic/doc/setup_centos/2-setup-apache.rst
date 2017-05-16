Install Web Server & Create GMN User
====================================

Apache
~~~~~~

Install Apache::

    $ sudo yum -y install httpd

Start Apache and configure to start on boot::

  $ sudo systemctl start httpd
  $ sudo systemctl enable httpd
  $ sudo systemctl enable httpd.service

To confirm apache is running, check the status::

    $ sudo systemctl status httpd

Now is a good time to check if Apache is listening on port 80 by default as it should be::

    $ netstat -ln | grep -E :'80'

Which will return output similar to::

    tcp6       0      0 :::80                   :::*                    LISTEN

If the command returns nothing, then something isn’t right. You should go back and review the previous steps.


Create GMN User
~~~~~~~~~~~~~~~

Change ownership of document root so it and its contents are in the same group as the web server::

    $ sudo chgrp -R apache /var/www/html

Now that apache is installed you can create a user and add it to the apache group::

    $ sudo useradd -G apache gmn
    $ sudo passwd gmn

