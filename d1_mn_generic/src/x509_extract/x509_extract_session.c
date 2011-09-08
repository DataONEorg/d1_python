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

// :platform:
//   Linux
// :Synopsis:
//   Extract the DataONE Session object from a PEM formatted X.509 v3
//   certificate.
// :Author:
//   DataONE (dahl)

#include <python2.6/Python.h>

#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/bio.h>
#include <openssl/x509v3.h>
#include <openssl/asn1.h>

#include <stdio.h>
#include <string.h>

int extract_session(unsigned char** session_buf, char *x509_cert_pem) {
  // Parse the PEM formatted X.509 cert.
  BIO* bio_in = NULL;
  X509* x509 = NULL;
  bio_in = BIO_new_mem_buf(x509_cert_pem, -1);
  if (!bio_in) {
    PyErr_SetString(PyExc_Exception, "Unable to create OpenSSL BIO");
    goto err;    
  }
  x509 = PEM_read_bio_X509_AUX(bio_in, NULL, NULL, NULL);
  if (!x509) {
    PyErr_SetString(PyExc_Exception,
                    "Unable to parse PEM formatted X.509 v3 certificate");
    goto err;
  }
  
  // Get the DataONE Session extension.
  int session_nid = OBJ_create("1.3.6.1.4.1.37951.10.1", "DataONESession",
                             "DataONE Session XML Object");
  int session_idx = X509_get_ext_by_NID(x509, session_nid, -1);
  X509_EXTENSION* ex = X509_get_ext(x509, session_idx);
  if (!ex) {
    PyErr_SetString(PyExc_Exception, "Unable to find DataONE Session");
    goto err;
  }

  // DER decode the extension value to get the UTF-8 XML.
  ASN1_OCTET_STRING* session = X509_EXTENSION_get_data(ex);
  const unsigned char* session_data = session->data;
  long len;
  int tag, xclass;
  int ret = ASN1_get_object(&session_data, &len, &tag, &xclass, session->length);
  if (ret) {
    PyErr_SetString(PyExc_Exception, "Unable to DER decode DataONE Session");
    goto err;
  }
  
  // Create buffer for Session string.
  *session_buf = (unsigned char*)malloc(len + 1 /* zero terminator */);
  if (!*session_buf) {
    PyErr_SetString(PyExc_Exception,
                    "Unable to allocate memory for DataONE Session");
    goto err;
  }

  // Copy string to buffer.
  strncpy((char*)*session_buf, (const char*)session_data, len + 1);

  return 1;

err:
  if (x509) {
    X509_free(x509);    
  }
  if (bio_in) {
    BIO_free_all(bio_in);
  }
  return 0;
}

static PyObject* x509_extract_session_extract(PyObject *self, PyObject *args) {
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
  unsigned char* session_buf;
  int ret = extract_session(&session_buf, x509_cert_pem);
  if (!ret) {
    // extract_session() sets an error string if unsuccessful. Returning NULL
    // raises a Python exception with that string.
    return NULL;
  }

  // Build Python string containing the session.
  PyObject* session_str = Py_BuildValue("s", session_buf);
  
  free(session_buf);
  
  return session_str;
}

static PyMethodDef x509_extract_session_methods[] = {
  {"extract",  x509_extract_session_extract, METH_VARARGS,
  "Extract DataONE Session from X.509 certificate"},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

PyMODINIT_FUNC initx509_extract_session(void) {
  // Initialize OpenSSL.
  SSL_load_error_strings();
  ERR_load_BIO_strings();
  OpenSSL_add_all_algorithms();
  // Initialize Python module.
  (void) Py_InitModule("x509_extract_session", x509_extract_session_methods);
}

//int main(int argc, char *argv[]) {
//  /* Pass argv[0] to the Python interpreter */
//  Py_SetProgramName(argv[0]);
//
//  /* Initialize the Python interpreter.  Required. */
//  Py_Initialize();
//
//  /* Add a static module */
//  initx509_extract_session();
//  
//  return 0;
//}
