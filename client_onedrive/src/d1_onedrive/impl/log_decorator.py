from __future__ import absolute_import

import functools
import logging


class log_func(object):
  def __call__(self, func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
      logging.info('---> {0}'.format(func.__name__))
      f_result = func(*args, **kwds)
      logging.info('<--- {0}'.format(func.__name__))
      return f_result

    return wrapper
