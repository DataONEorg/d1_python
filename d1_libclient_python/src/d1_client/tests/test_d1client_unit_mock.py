'''
Created on Feb 20, 2015

@author: mark
'''
import unittest
from mock import Mock, call
import src.d1_client.d1client as d1client
import src.d1_client.d1baseclient as d1baseclient
import cnclient
import testing_utilities
import testing_context

MEMBER_NODES = {
  'dryad': 'http://dev-dryad-mn.dataone.org/mn',
  'daac': 'http://daacmn.dataone.utk.edu/mn',
  'metacat': 'http://knb-mn.ecoinformatics.org/knb/d1',
}

COORDINATING_NODES = {'cn-dev': 'http://cn-dev.dataone.org/cn', }


class OrderTest(unittest.TestCase):
  # declare the test resource
  fooSource = None

  # preparing to test
  def setUp(self):
    """ Setting up for the test """
    self.d1_object = d1client.DataONEObject(
      '_bogus_pid_845434598734598374534958',
      forcenew=True
    )
    self.target = MEMBER_NODES['dryad']

    # identify the test routine
    testName = self.id().split(".")
    testName = testName[2]
    print testName

    self.fooSource = Mock(
      spec=d1client.DataONEObject(
        '_bogus_pid_845434598734598374534958',
        forcenew=True
      )
    )
    self.fooSource._cnBaseUrl.return_value = True
    self.fooSource.getInventory.return_value = 5

  def test_resolve_return(self):
    self.mock_cn = Mock(
      spec=cnclient_2_0.CoordinatingNodeClient_2_0(
        base_url='www.example.com'
      )
    )

    # ending the test
  def tearDown(self):
    """Cleaning up after the test"""
    print "OrderTest:tearDown_:begin"
    print ""
