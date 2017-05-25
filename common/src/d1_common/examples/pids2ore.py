#!/usr/bin/env python
"""Version 2 of OAI-ORE support in Python for DataONE."""
import logging

from resource_map import ResourceMap


def createSimpleResourceMap(ore_pid, sci_meta_pid, data_pids):
  """Create a simple resource map with one metadata document and n data
  objects."""
  ore = ResourceMap()
  ore.oreInitialize(ore_pid)
  ore.addMetadataDocument(sci_meta_pid)
  ore.addDataDocuments(data_pids, sci_meta_pid)
  return ore


def pids2ore(in_stream, fmt='xml', base_url=u'https://cn.dataone.org/cn'):
  """read pids from in_stream and generate a resource map.

  first pid is the ore_pid second is the sci meta pid remainder are data
  pids
  """
  pids = []
  for line in in_stream:
    pid = line.strip()
    if len(pid) > 0:
      if not pid.startswith("# "):
        pids.append(pid)
  if (len(pids)) < 2:
    raise ValueError("Insufficient identifiers provided.")

  logging.info(u"Read %d identifiers", len(pids))

  ore = ResourceMap(base_url=base_url)

  logging.info(u"ORE PID = %s", pids[0])
  ore.oreInitialize(pids[0])

  logging.info(u"Metadata PID = %s", pids[1])
  ore.addMetadataDocument(pids[1])

  ore.addDataDocuments(pids[2:], pids[1])
  return ore.serialize(doc_format=fmt)
