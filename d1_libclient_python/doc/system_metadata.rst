.. _system_metadata:

SystemMetadata
==============

This class simplifies access to the individual values in a SystemMetadata
object.

Reference: :ref:`d1_client_systemmetadata`

Example
~~~~~~~

::

  >>> target = "http://localhost:8000/mn"
  >>> from d1_client import client
  >>> cli = client.DataOneClient()
  >>> objects = cli.listObjects(target=target,count=3)
  >>> objects['data'][0]['pid']
  u'02c3f67e-b2e1-4550-8fae-f6d90e9f15f6'
  >>> sysm = cli.getSystemMetadata(objects['data'][0]['pid'], target=target)
  >>> sysm.Checksum
  '2e01e17467891f7c933dbaa00e1459d23db3fe4f'
