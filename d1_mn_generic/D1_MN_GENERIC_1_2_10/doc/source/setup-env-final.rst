

Turn off stand-alone mode
~~~~~~~~~~~~~~~~~~~~~~~~~

When setting up a :doc:`stand-alone node <setup-local>`, set ``STAND_ALONE`` to
``True`` in the ``settings_site.py`` file::

  # Only perform this step on a stand-alone instance of GMN.
  $ sudo nano /var/local/dataone/gmn/lib/python2.7/site-packages/service/settings_site.py

* Set ``STAND_ALONE`` to ``True``.
