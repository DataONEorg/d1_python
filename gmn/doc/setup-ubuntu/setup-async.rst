Configure the GMN asynchronous processes
========================================

Run the commands below to:

  * Set up cron jobs for GMN's asynchronous processes

  .. _clip1:

  ::

      [ `whoami` != root ] && sudo -Hs

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip1">Copy</button>
  ..

  .. _clip2:

  ::

    . /var/local/dataone/gmn_venv/bin/activate
    export GMN_PKG_DIR=`python -c "import site; print(site.getsitepackages()[0])"`
    crontab -u gmn ${GMN_PKG_DIR}/d1_gmn/deployment/crontab

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip2">Copy</button>
  ..


Altering the schedule
~~~~~~~~~~~~~~~~~~~~~

By default, the processes are set to run once every hour, with a random delay that distributes network traffic and CN load over time. To alter the schedule, consult the crontab manual:

  .. _clip3:

  ::

    man 5 crontab

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip3">Copy</button>
  ..

