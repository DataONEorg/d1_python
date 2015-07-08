#!/bin/python2.7
__author__ = 'mark'
import service.mn.management.commands.process_replication_queue as rep_queue


def get_file_lock(fname):

  lock = rep_queue.Lock(fname)
  file_opened = True
  lock.acquire()
  lock.release()


if __name__ == '__main__':
  fname = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/tmp/test1.txt'
  get_file_lock(fname)
