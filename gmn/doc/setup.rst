GMN setup overview
==================

Setting up the DataONE Generic Member Node (:term:`GMN`).

Verified setup procedures are provided for Ubuntu 16.04 LTS (Server and Desktop) and CentOS 7.3.

It may be possible to deploy GMN using a different stack, such as one based on `nginx <http://nginx.net/>`_ and `uWSGI <http://projects.unbit.it/uwsgi/wiki/>`_. Such setups are currently untested, but if they are attempted and prove to have benefits, please let us know.

The GMN setup process has been broken down into two sections, each containing a series of steps. The first section describes how to set up an instance of GMN which can be used only locally. The second section describes how to join the GMN instance to DataONE. For testing GMN and learning about Member Nodes, only the first section need be completed. For exposing data to the DataONE federation and providing storage for replicas, both the first and second sections must be completed.

Along with the steps in each section, some background information is provided. The actual steps that need to be performed are indented to separate them from the background information.

Commands that need to be run from the shell are prefixed with "$".

The instructions describe an installation into subfolders of ``/var/local/dataone/``. To install into another location, all related paths must be adjusted accordingly.

The instructions describe how to set GMN up to run in a separate Apache Virtual Host on a fresh install of Ubuntu. General setup and configuration issues, such as issues that may be encountered when adding GMN to an existing server, are not covered.

The GMN software stack is installed into a Python virtual environment to avoid potential conflicts with other Python software on the server.

Use the `Next` link in the sidebar to get to the next page of steps after completing the current page.


.. toctree::
  :maxdepth: 2

  setup_ubuntu/setup
  setup_centos/setup
  setup-env
  setup-extra
  setup-extra-resources
  setup-migrate
