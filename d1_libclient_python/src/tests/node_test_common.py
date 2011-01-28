import logging
'''TEST_INFO is a list of dictionaries, with each dictionary containing
entries for baseurl, existingpid, and boguspid.
'''
TEST_INFO = {'schema_version': 'http://dataone.org/service/types/0.5.1',
             'MN': [{'baseurl': 'http://dev-dryad-mn.dataone.org/mn',
                    'existingpid': 'hdl:10255/dryad.105/mets.xml',
                    'existingpid_ck': 'e494ca7b15404f41006356a5a87dbf44b9a415e7',
                    'boguspid': 'some bogus id'},
                   {'baseurl': 'http://daacmn.dataone.utk.edu/mn',
                    'existingpid': 'MD_ORNLDAAC_787_03032010095920',
                    'existingpid_ck': '49fd46daad283f0cbd411e0297e0d68d56d001a4',
                    'boguspid': 'some bogus id'},
                   {'baseurl': 'http://knb-mn.ecoinformatics.org/knb/d1',
                    'existingpid': 'knb-lter-sev.4892.1',
                    'existingpid_ck': '08B1F55E0C214E15621B5334D84A1D2B',
                    'boguspid': 'some bogus id'},
                   {'baseurl': 'http://sandbox08.uwrl.usu.edu/gmn_cuahsi/mn.svc',
                    'existingpid': '56e2c6c3-03ff-46a4-9f08-96a5beb66183',
                    'existingpid_ck': '???',
                    'boguspid': 'some bogus pid'}],
             'CN': [{'baseurl': 'http://cn-dev.dataone.org',
                    'existingpid': '',
                    'existingpid_ck': '',
                    'boguspid': 'some bogus pid'
                    }]
            }


def loadTestInfo(
  baseurl=None,
  pid=None,
  checksum=None,
  schemaversion=TEST_INFO['schema_version'],
  boguspid='some bogus pid'
):
  '''Populate TEST_INFO dynamically
  '''
  if baseurl is None:
    return TEST_INFO
  test = {'schema_version': schemaversion,
          'MN': [{'baseurl': baseurl,
                 'existingpid': pid,
                 'existingpid_ck': checksum,
                 'boguspid': boguspid}],
          'CN': []}
  return test
