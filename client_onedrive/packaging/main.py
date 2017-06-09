from __future__ import print_function


def entrypoint0():

  import sys
  print(sys.argv)
  del sys.modules['__main__']

  entrypoint1()


def entrypoint1():

  from d1_onedrive import onedrive
  onedrive.main()
