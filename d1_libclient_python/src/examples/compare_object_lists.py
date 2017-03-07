#!/usr/bin/env python
import logging

import d1_client.objectlistiterator
import d1_client.mnclient_2_0
import d1_client.cnclient_2_0

# Check for discrepancies between MN and CN by comparing object lists

#CN_BASE_URL = d1_common.const.URL_CN_BASE_URL
CN_BASE_URL = 'https://cn-stage.test.dataone.org/cn'
#CN_BASE_URL = 'https://cn-sandbox.test.dataone.org/cn'
#CN_BASE_URL = 'https://cn-dev.test.dataone.org/cn'

NODE_ID = 'urn:node:mnTestR2R'


def main():
  logging.basicConfig(level=logging.INFO)

  node_pyxb = find_node(NODE_ID)

  if node_pyxb is None:
    print 'Node not found: {}'.format(NODE_ID)
    return

  if node_pyxb.type != 'mn':
    print 'Expected NodeID be for an MN. Found a {}'.format(
      node_pyxb.type.upper()
    )
    return

  print 'BaseURL: {}'.format(node_pyxb.baseURL)

  mn_base_url = node_pyxb.baseURL

  mn_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(mn_base_url)
  pid_a_dict = get_object_dict(mn_client)

  cn_client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(CN_BASE_URL)
  pid_b_dict = get_object_dict(cn_client, node_id=NODE_ID)

  dump_unique(pid_a_dict, pid_b_dict, CN_BASE_URL)
  dump_unique(pid_b_dict, pid_a_dict, mn_base_url)


def dump_unique(from_dict, not_in_dict, base_url):
  only_pid_set = set(from_dict.keys()).difference(set(not_in_dict.keys()))
  print '{} only in {}:'.format(len(only_pid_set), base_url)
  for pid_str in sorted(
      only_pid_set, key=lambda x: from_dict[x].dateSysMetadataModified
  ):
    print '  {} {}'.format(pid_str, from_dict[pid_str].dateSysMetadataModified)


def get_object_dict(client, node_id=None):
  pid_dict = {}
  for object_info in d1_client.objectlistiterator.ObjectListIterator(
      client, nodeId=node_id
  ):
    pid_dict[object_info.identifier.value()] = object_info
  return pid_dict


def find_node(node_id):
  cn_client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(CN_BASE_URL)
  for node_pyxb in cn_client.listNodes().node:
    if node_pyxb.identifier.value() == node_id:
      return node_pyxb


if __name__ == '__main__':
  main()
