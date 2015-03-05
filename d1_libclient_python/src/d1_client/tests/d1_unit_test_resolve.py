'''
Created on Feb 23, 2015

@author: mark
'''
import unittest


class Test(unittest.TestCase):
  def test_resolve_return_value(self):
    with patch.object(
      d1client.cnclient.CoordinatingNodeClient,
      'resolve',
      new_callable=PropertyMock
    ) as mocked_d1:
      #         mock_resolve.return_value = 'test2'
      mocked_d1.objectLocation.return_value = 'test'
      self.client.resolve('_bogus_pid_845434598734598374534958')
      self.assertEqual('test', self.client._mn)


if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()
