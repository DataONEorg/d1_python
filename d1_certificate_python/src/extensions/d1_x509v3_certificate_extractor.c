// This work was created by participants in the DataONE project, and is
// jointly copyrighted by participating institutions in DataONE. For
// more information on DataONE, see our web site at http://dataone.org.
//
//   Copyright ${year}
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// :Synopsis:
//   Python extension that extracts the DataONE Session from a PEM formatted
//   X.509 v3 certificate.
//
//   The Session includes information such as the signature and the valid
//   not before and valid not after date-times. But those items are validated
//   by Apache and so are not of interest at this point. So, in the context
//   of this function, the Session is the Subject DN and the SubjectInfo XML
//   document.
//
// :Author:
//   DataONE (dahl)

#include <Python.h>

#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/bio.h>
#include <openssl/x509v3.h>
#include <openssl/asn1.h>

#include <stdio.h>
#include <string.h>


// DataONE OID: 1.3.6.1.4.1.37951.10.1
// CILogon OID for DataONE SubjectInfo: 1.3.6.1.4.1.34998.2.1:
#define SUBJECT_INFO_OID "1.3.6.1.4.1.34998.2.1"
#define SUBJECT_FORMAT_FLAGS \
  XN_FLAG_RFC2253

//  ASN1_STRFLGS_ESC_QUOTE | \
//  ASN1_STRFLGS_RFC2253 | \
//  XN_FLAG_DN_REV | \
//  XN_FLAG_DUMP_UNKNOWN_FIELDS \
//  XN_FLAG_FN_SN | \
//  XN_FLAG_SEP_COMMA_PLUS | \

enum status_enum {
  ERROR,
  SUCCESS
};


enum status_enum extract(
  unsigned char** subject_buf,
  unsigned char** subject_info_buf,
  char *x509_cert_pem)
{
  enum status_enum status = ERROR;
  BIO* bio_cert = NULL;
  BIO* bio_subject = NULL;
  X509* x509 = NULL;
  X509_NAME* subject = NULL;
  int result;
  long len;

  // Parse the PEM formatted X.509 cert.
  bio_cert = BIO_new_mem_buf(x509_cert_pem, -1);
  if (!bio_cert) {
    PyErr_SetString(PyExc_Exception, "Error creating OpenSSL BIO");
    goto end;
  }
  x509 = PEM_read_bio_X509_AUX(bio_cert, NULL, NULL, NULL);
  if (!x509) {
    PyErr_SetString(PyExc_Exception,
                    "Error parsing PEM formatted X.509 v3 certificate");
    goto end;
  }

  // Get the Subject DN.
  subject = X509_get_subject_name(x509);
  if (!subject) {
    PyErr_SetString(PyExc_Exception, "Error reading certificate subject");
    goto end;
  }
  // Create BIO for Subject.
  bio_subject = BIO_new(BIO_s_mem());
  if (!bio_subject) {
    PyErr_SetString(PyExc_Exception, "Error creating Subject BIO");
    goto end;
  }
  // Write formatted DN to BIO.
  result = X509_NAME_print_ex(bio_subject, subject, 0, SUBJECT_FORMAT_FLAGS);
  if (!result) {
    PyErr_SetString(PyExc_Exception, "Error formatting Subject");
    goto end;
  }
  // Copy BIO to C buffer.
  char *start = NULL;
  len = BIO_get_mem_data(bio_subject, &start);
  *subject_buf = (unsigned char*)malloc(len + 1 /* zero terminator */);
  if (!*subject_buf) {
    PyErr_SetString(PyExc_Exception,
                    "Unable to allocate memory for Subject buffer");
    goto end;
  }
  strncpy((char*)*subject_buf, (const char*)start, len);
  (*subject_buf)[len] = 0; // zero terminator

  // Get the DataONE SubjectInfo extension.
  int session_nid = OBJ_create(SUBJECT_INFO_OID, "SubjectInfo",
                               "DataONE SubjectInfo XML Object");
  int session_idx = X509_get_ext_by_NID(x509, session_nid, -1);
  X509_EXTENSION* extension = X509_get_ext(x509, session_idx);
  if (extension) {
    // DER decode the extension value to get the UTF-8 XML.
    // Not sure if this has been properly tested with UTF-8 strings. May
    // need ASN1_STRING_to_UTF8().
    ASN1_OCTET_STRING* subject_info = X509_EXTENSION_get_data(extension);
    const unsigned char* subject_info_data = subject_info->data;
    int tag, xclass;
    result = ASN1_get_object(&subject_info_data, &len, &tag, &xclass,
                             subject_info->length);
    if (result) {
      PyErr_SetString(PyExc_Exception, "Unable to DER decode SubjectInfo");
      goto end;
    }
    // Create buffer for SubjectInfo.
    *subject_info_buf = (unsigned char*)malloc(len + 1 /* zero terminator */);
    if (!*subject_info_buf) {
      PyErr_SetString(PyExc_Exception,
                      "Unable to allocate memory for SubjectInfo buffer");
      goto end;
    }
    // Copy string to buffer.
    strncpy((char*)*subject_info_buf, (const char*)subject_info_data, len);
    (*subject_info_buf)[len] = 0; // zero terminator
  }
  else {
    // The SubjectInfo extension was not present in the certificate. Return
    // an empty string for it.
    *subject_info_buf = (unsigned char*)malloc(1);
    (*subject_info_buf)[0] = 0; // zero terminator
  }

  status = SUCCESS;

end:
  if (x509) {
    X509_free(x509);
  }
  if (bio_cert) {
    BIO_free_all(bio_cert);
  }
  if (bio_subject) {
    BIO_free_all(bio_subject);
  }
  OBJ_cleanup();
  return status;
}


static PyObject* d1_x509v3_certificate_extractor_extract(PyObject *self, PyObject *args) {
  // Convert the Python string containing the x509 certificate in PEM format to
  // a C terminated string.
  char *x509_cert_pem;
  if (!PyArg_ParseTuple(args, "s", &x509_cert_pem)) {
    PyErr_SetString(PyExc_Exception,
                    "Invalid argument. Expected a string containing a PEM "
                    "formatted X.509 v3 certificate");
    return NULL;
  }

  // Extract the session.
  unsigned char* subject_info_buf = NULL;
  unsigned char* subject_buf = NULL;
  enum status_enum status = extract(&subject_buf, &subject_info_buf,
                                            x509_cert_pem);
  if (status == ERROR) {
    // extract() sets an error string if unsuccessful. Returning NULL
    // raises a Python exception with that string.
    return NULL;
  }

  PyObject* py_session = Py_BuildValue("(ss)", subject_buf, subject_info_buf);
  free(subject_buf);
  free(subject_info_buf);
  return py_session;
}


static PyMethodDef d1_x509v3_certificate_extractor_methods[] = {
  {"extract",  d1_x509v3_certificate_extractor_extract, METH_VARARGS,
  "Extract DataONE Session from X.509 v3 certificate"},
  {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC initd1_x509v3_certificate_extractor(void) {
  // Initialize OpenSSL.
  SSL_load_error_strings();
  ERR_load_BIO_strings();
  OpenSSL_add_all_algorithms();
  // Initialize Python module.
  (void) Py_InitModule("d1_x509v3_certificate_extractor", d1_x509v3_certificate_extractor_methods);
}


//int main(int argc, char *argv[]) {
//  /* Pass argv[0] to the Python interpreter */
//  Py_SetProgramName(argv[0]);
//
//  /* Initialize the Python interpreter.  Required. */
//  Py_Initialize();
//
//  /* Add a static module */
//  initd1_x509v3_certificate_extractor();
//
//  return 0;
//}
