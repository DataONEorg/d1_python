Setup on CentOS
===============

This section describes the initial steps in setting up :term:`GMN`. It has been verified CentOS 7.3. Instructions for Ubuntu are :doc:`also available <../ubuntu/setup>`.

If only this section is completed, the resulting installation is a stand-alone test instance of GMN. The stand-alone instance can be used for performance testing, developing scripts for populating the MN and for learning about MNs in general.

By completing :doc:`../d1env/env`, the stand-alone test instance can then be joined to DataONE as an official Member Node.

Contents:

.. toctree::
  :maxdepth: 2

  01-firewall
  02-apache
  03-postgresql
  04-d1-stack
  05-vhost
  06-ssl
  07-authn-ca
  08-authn-client
  09-async
  10-basic-config
  11-final
  12-testing
