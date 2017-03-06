def entrypoint0():

  import sys
  print(sys.argv)
  del sys.modules['__main__']

  entrypoint1()


def entrypoint1():

  from onedrive import onedrive
  onedrive.main()
