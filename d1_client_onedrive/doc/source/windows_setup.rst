Creating the installer for Windows
==================================

ONEDrive supports Microsoft Windows. The Windows distribution installs ONEDrive
as a regular application, independent of any existing Python environment on the
computer. These instructions detail how to create the installer and is intended
as a reference for DataONE and 3rd party developers.

The regular distribution channel for DataONE's Python products is PyPI, but the
PyPI distribution does not include various files needed for building the
installer.

To create the ONEDrive installer for Windows, ONEDrive is first installed from
the DataONE Subversion repository into a regular Python environment.

Then, a stand-alone, executable version of ONEDrive is created with py2exe.

Finally, an installer is built for the executable and all dependencies.

1. If you do not already have a working 32-bit Python 2.7 environment, download
   the latest 32-bit Python 2.7 Windows installer from
   http://www.python.org/download/ and install it.

#. In ``Control Panel | Classic View | System | Advanced | Environment Variables``,
   add ``;C:\Python27;C:\Python27\Scripts`` to the end of the Path.

#. Install pip::

   > python -c "import urllib2; exec(urllib2.urlopen('https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py').read())"
   > easy_install pip




Download the latest Python 2.7 installer:
https://www.python.org/download/releases/2.7.6/
Windows x86 MSI Installer (2.7.6)

Run the installer and leave all settings at their defaults.

Download get-pip.py:
https://pip.pypa.io/en/latest/installing.html

Open a command prompt:

> setx path "%path%;C:\Python27;C:\Python27\Scripts"

Close then reopen the command prompt.

Go to the download location of get-pip.py.

E.g., cd \Users\Myself\Downloads

Install and update pip::

> python get-pip.py
> python -m pip install -U pip




#. Download and install the 32-bit Python 2.7 lxml Windows installer from
   http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml.

#. Open a Command Prompt.

#. Install the DataONE Client Library for Python and dependencies::

   > pip install dataone.libclient

#. Download and install Subversion for Windows from http://sourceforge.net/projects/win32svn/

#. Download and install the 32-bit Python 2.7 py2exe from http://sourceforge.net/projects/py2exe/files/py2exe/

#. Open a new Command Prompt (to pick up new path to the ``svn`` command).

#. Create a work area on disk. Below, ``C:\onedrive`` is used for this. To use
   another folder replace all the references to the folder below.

   ::

   > mkdir c:\onedrive
   > c:
   > cd \onedrive
   > svn co https://repository.dataone.org/software/cicore/trunk/itk/d1_client_onedrive/src/ .

#. Start ONEDrive and verify that it works::

   > src\d1_client_onedrive\onedrive.py

Access the ONEDrive filesystem and check that the folder hierarchy can be
traversed and that the DataONE objects can be accessed.

Exit with ctrl-break.

#. Build a stand-alone version of ONEDrive::

   > cd src
   > setup.py py2exe

A list of missing modules will be printed. These are not used by ONEDrive.

#. Verify that the exe version of ONEDrive works::

   > cd dist
   > onedrive.exe

Access the ONEDrive filesystem and check that the folder hierarchy can be
traversed and that the DataONE objects can be accessed.

Exit with ctrl-break.

#. Download and install the stable release of Inno Setup from: http://www.jrsoftware.org/isdl.php#stable

Open the Inno Setup script::

  > cd \onedrive
  > onedrive-setup.iss

In the script, update the version number so that it matches the version number
displayed when ONEDrive was started in a previous step.

Build the installer by selecting ``Compile`` and ``Build`` in the main menu.

The finished installer will be in ``C:\onedrive\src\Output``.
