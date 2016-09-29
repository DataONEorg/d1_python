import datetime
import os
import sys

import django.test

import mn.sysmeta_db

import d1_common.types.dataoneTypes_v2_0 as v2
# import myapp.models



class GMNUnitTests(django.test.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def _make_absolute(self, p):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)

  def _read_test_file(self, filename, mode_str ='r'):
    return open(os.path.join(self._make_absolute('test_files'), filename), mode_str).read()

  def _read_test_xml(self, filename, mode_str ='r'):
    xml_str = self._read_test_file(filename, mode_str)
    xml_obj = v2.CreateFromDocument(xml_str)
    return xml_obj

  def _create_sci_obj_base(self):
    sci_row = mn.models.ScienceObject()
    sci_row.checksum_algorithm = mn.sysmeta_db._get_or_create_checksum_algorithm_row('SHA-1')
    sci_row.format = mn.sysmeta_db._get_or_create_format_row('test')
    sci_row.is_archived = False
    sci_row.is_replica = False
    sci_row.mtime = datetime.datetime.now()
    sci_row.pid = mn.sysmeta_db.create_id_row('test')
    sci_row.serial_version = 1
    sci_row.size = 1
    sci_row.save()
    return sci_row

  def test_0(self):
    sci_row = self._create_sci_obj_base()
    sysmeta_obj = self._read_test_xml('sysmeta_v2_0_sample.xml')
    mn.sysmeta_db._update_access_policy(sci_row, sysmeta_obj)
    print sysmeta_obj.accessPolicy.toxml()
