Basic Configuration
===================

Configure the GMN settings that are required for running a local instance of GMN.

For a basic local standalone install, all the settings can be left at their
defaults.

Run the commands below to:

  * Create default settings based on settings template

  .. _clip1:

  ::

    [ `whoami` != gmn ] && sudo -Hsu gmn

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip1">Copy</button>
  ..

  .. _clip2:

  ::

    . /var/local/dataone/gmn_venv/bin/activate
    export GMN_PKG_DIR=`python -c "import site; print(site.getsitepackages()[0])"`
    cp ${GMN_PKG_DIR}/d1_gmn/settings_template.py ${GMN_PKG_DIR}/d1_gmn/settings.py

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip2">Copy</button>
  ..
