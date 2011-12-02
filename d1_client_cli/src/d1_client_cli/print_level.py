def print_level(level, msg):
  for l in str(msg).split('\n'):
    print('{0: <8s}{1}'.format(level, l))


def print_debug(msg):
  print_level('DEBUG', msg)


def print_error(msg):
  print_level('ERROR', msg)


def print_info(msg):
  print_level('', msg)
