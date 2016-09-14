import logging
import unittest
import sys
from django.http.response import HttpResponse
from mock import patch, PropertyMock, MagicMock
import httplib
import datetime
sys.path.append('/home/mark/d1/d1_python/d1_mn_generic/src/service')
from service.mn.mn import models
import service.mn.views
from mock_django.query import QuerySetMock


class response(object):
  def __init__(self):
    self['Content-Length'] = 0

  def read(self):
    return 'http://ns.dataone.org/service/types/v1'


class science_object():
  def __init__(
    self,
    pid,
    obsoletedBy,
    obsoletes,
    sid,
    date_mod=datetime.datetime(2015, 4, 1),
    archived=False
  ):
    self.obsoletedBy = obsoletedBy
    self.obsoletes = obsoletes
    self.pid = pid
    self.sid = sid
    self.mtime = date_mod
    self.archived = archived
    self.size = 1024
    self.format = create_format()
    self.checksum_algorithm = create_checksum_algorithm()
    self.checksum = 'xyzpdq'
    self.serial_version = 'v1.1'


class create_format(object):
  def __init__(self, *args, **kwargs):
    self.format_id = 2


class create_checksum_algorithm(object):
  def __init__(self):
    self.checksum_algorithm = 'Sha-2'


class mocked_request():
  def __init__(self):
    self.method = 'GET'
    pass


class NewDate(datetime.datetime):
  @classmethod
  def utcnow(cls):
    return cls(2010, 1, 1, 0, 0, 0)


class method(mocked_request):
  def __init__(self):
    self.method = 'GET'


class Test(unittest.TestCase):
  def setUp(self):
    self.pid = 'test123'

  def tearDown(self):
    pass

  @patch('mn.views.external.get_object_pid')
  @patch.object(httplib.HTTPConnection, 'request')
  def test_dispatch_object_pid(self, mock_request, mock_get):
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      mock_request.method = 'GET'
      mock_get.return_value = 'test123'
      response = v1.dispatch_object_pid(mock_request, self.pid)
      self.assertEqual('test123', response)

  @patch('mn.views.external.put_object_pid')
  @patch.object(httplib.HTTPConnection, 'request')
  def test_dispatch_object_pid_PUT(self, mock_request, mock_put):
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      mock_request.method = 'PUT'
      mock_put.return_value = 'test123'
      response = v1.dispatch_object_pid(mock_request, self.pid)
      self.assertEqual('test123', response)

  @patch('mn.views.external.put_object_pid')
  @patch.object(httplib.HTTPConnection, 'request')
  def test_dispatch_object_pid_HEAD(self, mock_request, mock_head):
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      mock_request.method = 'PUT'
      mock_head.return_value = 'test123'
      response = v1.dispatch_object_pid(mock_request, self.pid)
      self.assertEqual('test123', response)

  @patch('mn.views.external.delete_object_pid')
  @patch.object(httplib.HTTPConnection, 'request')
  def test_dispatch_object_pid_DELETE(self, mock_request, mock_delete):
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      mock_request.method = 'DELETE'
      mock_delete.return_value = 'test123'
      response = v1.dispatch_object_pid(mock_request, self.pid)
      self.assertEqual('test123', response)

  @patch('mn.views.external.get_object_pid')
  @patch.object(httplib.HTTPConnection, 'request')
  def test_dispatch_object_pid_assert_called_HttpResponseNotAllowed(
    self, mock_request, mock_get
  ):
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      with patch('mn.views.external.HttpResponseNotAllowed') as mocked_method:
        mock_request.method = 'POST'
        mock_get.return_value = 'test123'
        v1.dispatch_object_pid(mock_request, self.pid)
        mocked_method.assert_called_once_with(['GET', 'HEAD', 'POST', 'PUT', 'DELETE'])

  @patch('mn.views.external.get_object')
  @patch.object(httplib.HTTPConnection, 'request')
  def test_dispatch_object(self, mock_request, mock_get):
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      mock_request.method = 'GET'
      mock_get.return_value = 'test123'
      response = v1.dispatch_object(mock_request)
      self.assertEqual('test123', response)

  @patch('mn.views.external.object_post')
  @patch.object(httplib.HTTPConnection, 'request')
  def test_object_post(self, mock_request, mock_post):
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      mock_request.method = 'GET'
      mock_post.return_value = 'test123'
      response = v1.object_post(mock_request)
      self.assertEqual('test123', response)

  @patch('mn.views.external.get_object_pid')
  @patch.object(httplib.HTTPConnection, 'request')
  def test_dispatch_object_assert_called_HttpResponseNotAllowed(
    self, mock_request, mock_get
  ):
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      with patch('mn.views.external.HttpResponseNotAllowed') as mocked_method:
        mock_request.method = 'PUT'
        mock_get.return_value = 'test123'
        v1.dispatch_object(mock_request)
        mocked_method.assert_called_once_with(['GET', 'POST'])

  @patch('mn.view_util.add_http_date_to_response_header')
  @patch('mn.view_util.http_response_with_boolean_true_type')
  @patch.object(httplib.HTTPConnection, 'request')
  def test_get_monitor_ping(self, mock_request, mock_response, mock_add):
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      # output = service.mn.views.external.dispatch_object_pid()
      mock_response.return_value = 'OK'
      mock_request.method = 'GET'
      response = v1.get_monitor_ping(mock_request)
      self.assertIn('OK', response)

  @patch('mn.db_filter.add_slice_filter')
  @patch('mn.db_filter.add_string_begins_with_filter')
  @patch('mn.db_filter.add_string_filter')
  @patch('mn.db_filter.add_datetime_filter')
  @patch('mn.db_filter.add_access_policy_filter')
  @patch('mn.auth.is_trusted_subject')
  @patch('mn.models.EventLog.objects.order_by')
  def DO_NOT_test_get_log(
    self, mock_order, mock_is_trusted, mock_add, mock_add_datetime, mock_add_string,
    mock_add_string_begins, mock_addslice
  ):
    #can't mock the query_unsliced.count
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      with patch.object(
        models.EventLog.objects,
        'count', new_callable=PropertyMock
      ) as mock_count:
        mock_request.method = 'GET'
        mock_add_string_begins.return_value = ['test']
        mock_addslice.return_value = [[], 0, 1]
        mock_count.side_effect = 1
        response = v1.get_log(mock_request)
        self.assertEqual(response, {'count': 1, 'query': [], 'total': 1, 'type': 'log', 'start': 1})

  @patch('mn.node.Node')
  @patch('mn.views.external.HttpResponse')
  def test_get_node(self, mock_response, mock_node):
    with patch(
      'httplib.HTTPConnection.request',
      new_callable=PropertyMock
    ) as mock_request:
      mock_request.method = 'GET'
      mock_response.return_value = 'test'
      node = v1.get_node(mock_request)
      self.assertEqual(node, 'test')

  @patch(
    'mn.views.external.d1_client.object_format_info.ObjectFormatInfo.content_type_from_format_id'
  )
  def test_content_type_from_format_id(self, mock_id):
    mock_id.return_value = 'v1'
    response = v1._content_type_from_format_id('test')
    self.assertEqual('v1', response)

    # @patch('mn.view_util.add_http_date_to_response_header')
    # def test_add_object_properties_to_response_header(self, mock_add):
    #     with patch('mn.views.external.datetime.datetime') as mock_datetime:
    #         mock_datetime.utcnow.return_value = '2015-03-06 12:56:54.323738'
    #         mock_datetime.isoformat.return_value = '2015-03-06 12:56:54.323738'
    #         response = {}
    #         sci_obj = science_object('p3','p4','p2','s1')
    #         v1._add_object_properties_to_response_header(response,sci_obj)
    #         self.assertEqual(response, {'Content-Length': 1024, 'DataONE-SerialVersion': 'v1.1', 'DataONE-Checksum': 'Sha-2,xyzpdq',
    #  'DataONE-formatId': 2, 'Last-Modified': '2015-03-06 12:56:54.323738','Content-Type': 'application/octet-stream'})

  @patch('mn.views.external.datetime.datetime')
  @patch('mn.view_util.add_http_date_to_response_header')
  def test_add_object_properties_to_response_header(self, mock_add, mock_datetime):
    mock_datetime = NewDate
    # mock_datetime.utcnow.return_value = '2015-03-06 12:56:54.323738'
    # mock_datetime.isoformat.return_value = '2015-03-06 12:56:54.323738'
    response = {}
    sci_obj = science_object('p3', 'p4', 'p2', 's1')
    v1._add_object_properties_to_response_header(response, sci_obj)
    self.assertEqual(response, {'Content-Length': 1024, 'DataONE-SerialVersion': 'v1.1', 'DataONE-Checksum': 'Sha-2,xyzpdq',
                                'DataONE-formatId': 2, 'Last-Modified': '2015-03-06 12:56:54.323738','Content-Type': 'application/octet-stream'})

  @patch('mn.views.external._content_type_from_format_id')
  @patch('mn.views.external._get_object_byte_stream')
  @patch('mn.auth.assert_allowed')
  @patch('mn.event_log.read')
  @patch('mn.views.external._add_object_properties_to_response_header')
  @patch('mn.views.external.django.http.response.StreamingHttpResponse')
  @patch('mn.view_asserts.object_exists')
  def DO_NOT_test_get_object_pid(
    self, mock_object, mock_stream, mock_add, mock_read, mock_auth, mock_bytes,
    mock_content
  ):
    with patch(
      'mn.models.ScienceObject.objects.get',
      new_callable=PropertyMock
    ) as mock_get:
      #             mock_stream.return_value = 'test123'
      mock_auth.return_value = True
      mock_get.return_value = [
        science_object(
          'p1', None, None, 's1', date_mod=date(2015, 4, 1)), science_object(
            'p2', None, None, 's1', date_mod=date(2015, 4, 2)
          )
      ]
      response = v1.get_object_pid('test', self.pid)
      self.assertEqual('test123', response)


if __name__ == "__main__":

  def log_setup():
    formatter = logging.Formatter(
      '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
    )
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
