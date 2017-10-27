import d1_gmn.app
import d1_gmn.app.models
import d1_gmn.app.sciobj_store
import d1_gmn.app.util

import d1_common.checksum
import d1_common.types
import d1_common.types.exceptions
import d1_common.xml


def sanity(request, sysmeta_pyxb, new_pid=None):
  _does_not_contain_replica_sections(sysmeta_pyxb)
  _is_not_archived(sysmeta_pyxb)
  if new_pid:
    _matches_url_pid(sysmeta_pyxb, new_pid)
  obsoleted_by_not_specified(sysmeta_pyxb)
  _matches_uploaded(request, sysmeta_pyxb)


def has_matching_modified_timestamp(new_sysmeta_pyxb):
  pid = d1_common.xml.get_req_val(new_sysmeta_pyxb.identifier)
  old_sysmeta_model = d1_gmn.app.util.get_sci_model(pid)
  old_ts = old_sysmeta_model.modified_timestamp
  new_ts = new_sysmeta_pyxb.dateSysMetadataModified
  if old_ts != new_ts:
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'dateSysMetadataModified of updated System Metadata must match existing. '
      u'pid="{}" old_ts="{}" new_ts="{}"'.format(pid, old_ts,
                                                 new_ts), identifier=pid
    )


def obsoleted_by_not_specified(sysmeta_pyxb):
  if sysmeta_pyxb.obsoletedBy is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, u'obsoletedBy cannot be specified in System Metadata for this method'
    )


def obsoletes_not_specified(sysmeta_pyxb):
  if sysmeta_pyxb.obsoletes is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, u'obsoletes cannot be specified in System Metadata for this method'
    )


def obsoletes_matches_pid_if_specified(sysmeta_pyxb, old_pid):
  if sysmeta_pyxb.obsoletes is not None:
    if d1_common.xml.get_req_val(sysmeta_pyxb.obsoletes) != old_pid:
      raise d1_common.types.exceptions.InvalidSystemMetadata(
        0, u'Persistent ID (PID) specified in System Metadata "obsoletes" '
        u'field does not match PID specified in URL. '
        u'sysmeta_pyxb="{}", url="{}"'.format(
          d1_common.xml.get_req_val(sysmeta_pyxb.obsoletes), old_pid
        )
      )


#
# Private
#

# def revision_references_existing_objects_if_specified(sysmeta_pyxb):
#   _pid_exists_if_specified(sysmeta_pyxb, 'obsoletes')
#   _pid_exists_if_specified(sysmeta_pyxb, 'obsoletedBy')


def _does_not_contain_replica_sections(sysmeta_pyxb):
  """Assert that {sysmeta_pyxb} does not contain any replica information.
  """
  if len(getattr(sysmeta_pyxb, 'replica', [])):
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, u'A replica section was included. A new object object created via '
      u'create() or update() cannot already have replicas. pid="{}"'.
      format(d1_common.xml.get_req_val(sysmeta_pyxb.identifier)),
      identifier=d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
    )


def _is_not_archived(sysmeta_pyxb):
  """Assert that {sysmeta_pyxb} does not have have the archived flag set.
  """
  if _is_archived(sysmeta_pyxb):
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'Archived flag was set. A new object created via create() or update() '
      u'cannot already be archived. pid="{}"'.format(
        d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
      ), identifier=d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
    )


def _matches_url_pid(sysmeta_pyxb, pid):
  sysmeta_pid = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
  if sysmeta_pid != pid:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'PID specified in the URL parameter of the API call does not match the '
      u'PID specified in the included System Metadata. '
      u'url_pid="{}", sysmeta_pid="{}"'.format(pid, sysmeta_pid)
    )


def _matches_uploaded(request, sysmeta_pyxb):
  if 'HTTP_VENDOR_GMN_REMOTE_URL' not in request.META:
    _correct_file_size(request, sysmeta_pyxb)
    _supported_checksum_algorithm(sysmeta_pyxb)
    _correct_checksum(request, sysmeta_pyxb)


def _correct_file_size(request, sysmeta_pyxb):
  if sysmeta_pyxb.size != request.FILES['object'].size:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, u'Object size in System Metadata does not match that of the '
      u'uploaded object. sysmeta_pyxb={} bytes, uploaded={} bytes'.format(
        sysmeta_pyxb.size, request.FILES['object'].size
      )
    )


def _correct_checksum(request, sysmeta_pyxb):
  checksum_calculator = (
    d1_common.checksum.get_checksum_calculator_by_dataone_designator(
      sysmeta_pyxb.checksum.algorithm
    )
  )
  checksum_str = d1_gmn.app.sciobj_store.calculate_checksum(
    request, checksum_calculator
  )
  if sysmeta_pyxb.checksum.value().lower() != checksum_str.lower():
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'Checksum in System Metadata does not match that of the uploaded object. '
      u'sysmeta_pyxb="{}", uploaded="{}"'.format(
        sysmeta_pyxb.checksum.value().lower(), checksum_str.lower()
      )
    )


def _is_archived(sysmeta_pyxb):
  return getattr(sysmeta_pyxb, 'archived', False)


def _supported_checksum_algorithm(sysmeta_pyxb):
  if not (
      d1_common.checksum.
      is_supported_algorithm(sysmeta_pyxb.checksum.algorithm)
  ):
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'Checksum algorithm is unsupported. algorithm="{}" supported="{}"'.format(
        sysmeta_pyxb.checksum.algorithm,
        ', '.join(d1_common.checksum.get_supported_algorithms())
      )
    )


def _pid_exists_if_specified(sysmeta_pyxb, sysmeta_attr):
  pid = d1_common.xml.get_opt_val(sysmeta_pyxb, sysmeta_attr)
  if pid is None:
    return
  if not d1_gmn.app.models.ScienceObject.objects.filter(pid__did=pid).exists():
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, u'System Metadata field references non-existing object. '
      u'field="{}", pid="{}"'.format(sysmeta_attr, pid)
    )
