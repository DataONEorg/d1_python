Setup on CentOS
===============

This section describes the initial steps in setting up :term:`GMN`. It has been verified CentOS 7.3. Instructions for Ubuntu are :doc:`also available <../setup-ubuntu/setup>`.

If only this section is completed, the resulting installation is a stand-alone test instance of GMN. The stand-alone instance can be used for performance testing, developing scripts for populating the MN and for learning about MNs in general.

By completing :doc:`../setup-no-arch/setup-env`, the stand-alone test instance can then be joined to DataONE as an official Member Node.

.. toctree::
  :maxdepth: 2

  1-setup-firewall
  2-setup-apache
  3-setup-postgresql
  4-setup-d1-stack
  5-setup-vhost
  6-setup-ssl
  7-setup-authn-ca
  8-setup-authn-client
  9-setup-async
  10-setup-basic-config
  11-setup-final
  12-setup-testing
