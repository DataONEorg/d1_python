Installing GMN Software & Supporting Packages
=============================================

Install Packages & Pip
~~~~~~~~~~~~~~~~~~~~~~

Install development tools and other needed packages::

    $ sudo yum groupinstall -y 'development tools'
    $ sudo yum -y install python-devel openssl-devel libxml2-devel
    $ sudo yum -y install libxslt-devel libffi-devel curl mod_ssl
    $ sudo yum -y install openssl-perl gcc mod_wsgi

Install pip::

    $ sudo easy_install pip



Install GMN Software in Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the virtualenv command. We can get this using pip::

    $ sudo pip install virtualenv

Setup directories::


    $ sudo mkdir -p /var/local/dataone/{gmn_venv_py3,gmn_object_store}
    $ cd /var/local/dataone
    $ sudo chown gmn:apache gmn_venv_py3

Create and activate a virtual environment in the gmn_venv_py3 directory::

    sudo -Hu gmn bash -c '
      virtualenv gmn_venv_py3
      source gmn_venv_py3/bin/activate
      pip install --upgrade setuptools==33.1.1
      pip install dataone.gmn
    '


Configure the GMN Python virtual environment to be the default for the gmn user.::

    $ su MySudoUser
    $ sudo vi /home/gmn/.bashrc

This will take you into a text editor. Use the “i” key to enter insert mode. You will see the word ‘INSERT’ at the bottom when this is active, which means you can edit the contents. Add the following lines to the end of the file.::

    # This next line added as part of GMN installation setup:
    PATH="$PATH":/var/local/dataone/gmn_venv_py3/bin/


Then use Escape key and “:wq” to write the changes to the file and exit the editor.
