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
//   Generate a PEM formatted X.509 v3 certificate that contains a DataONE
//   SubjectInfo object as a custom extension and is signed by the DataONE Test
//   CA.
// :Author:
//   DataONE (Dahl)

#include <Python.h>

#include <openssl/x509.h>
#include <openssl/x509v3.h>
#include <openssl/err.h>
#include <openssl/pem.h>

// CILogon OID 1.3.6.1.4.1.34998.2.1: DataONE subjectInfo
#define SUBJECT_INFO_OID "1.3.6.1.4.1.34998.2.1"
#define CERTIFICATE_VALID_HOURS 18
#define CERTIFICATE_VALID_HOURS_LONG_TERM (24 * 365 * 10)
#define EXPIRE_SECS (60 * 60 * CERTIFICATE_VALID_HOURS)
#define EXPIRE_SECS_LONG_TERM (60 * 60 * CERTIFICATE_VALID_HOURS_LONG_TERM)
#define EXT_COUNT 5


enum status_enum {
  ERROR,
  NO_SESSION,
  SUCCESS
};


struct entry {
  char *key;
  char *value;
};


struct entry ext_ent[EXT_COUNT] = {
  {"basicConstraints", "CA:FALSE"},
  {"nsComment", "\"DataONE Test Certificate\""},
  {"subjectKeyIdentifier", "hash"},
  {"authorityKeyIdentifier", "keyid,issuer:always"},
  {"keyUsage", "nonRepudiation,digitalSignature,keyEncipherment"}
};


struct rdn {
  char* type;
  unsigned char* value;
};


enum status_enum generate(
                         char* cert_out_path, char* ca_cert_path,
                         char* ca_key_path, char* ca_key_pw,
                         char* public_key_path, char* subject_info,
                         char* subject_alt_name, struct rdn* rdns, int n_rdns,
                         int long_term)
{
  enum status_enum status = ERROR;

  int i;
  X509_NAME *name;
  X509V3_CTX ctx;
  FILE* fp = NULL;
  X509* ca_cert = NULL;
  X509* cert = NULL;
  EVP_PKEY* ca_private_key = NULL;
  EVP_PKEY* public_key = NULL;
  X509_EXTENSION* subject_alt_name_extension;

  // Read the CA certificate.
  if(!(fp = fopen(ca_cert_path, "r"))) {
    PyErr_SetString(PyExc_Exception, "Error opening CA certificate file");
    goto end;
  }
  if(!(ca_cert = PEM_read_X509(fp, NULL, NULL, NULL))) {
    PyErr_SetString(PyExc_Exception, "Error while reading CA certificate file");
    goto end;
  }
  fclose(fp);
  fp = NULL;

  // Read the CA private key.
  if(!(fp = fopen(ca_key_path, "r"))) {
    PyErr_SetString(PyExc_Exception, "Error opening CA private key file");
    goto end;
  }
  if(!(ca_private_key = PEM_read_PrivateKey(fp, NULL, NULL, ca_key_pw))) {
    PyErr_SetString(PyExc_Exception, "Error while reading CA private key");
    goto end;
  }
  fclose(fp);
  fp = NULL;

  // Create new certificate.
  if(!(cert = X509_new())) {
    PyErr_SetString(PyExc_Exception, "Error creating X509 object");
    goto end;
  }

  // Set version number.
  if(X509_set_version(cert, 2L) != 1) {
    PyErr_SetString(PyExc_Exception, "Error setting certificate version");
    goto end;
  }
  // Set serial number.
  ASN1_INTEGER_set(X509_get_serialNumber(cert), 1);

  // Add subject to certificate (DN represented as multiple RDNs).
  if (!(name = X509_NAME_new())) {
    PyErr_SetString(PyExc_Exception, "Error creating name object");
    goto end;
  }
  for (i = 0; i < n_rdns; ++i) {
    if (!(X509_NAME_add_entry_by_txt(name, rdns[i].type, MBSTRING_UTF8,
                                     rdns[i].value, -1, -1, 0))) {
      PyErr_SetString(PyExc_Exception, "Error adding RDN");
      goto end;
    }
  }
  if(X509_set_subject_name(cert, name) != 1) {
    PyErr_SetString(PyExc_Exception, "Error setting subject (DN)");
    goto end;
  }

  // Copy subject on CA certificate to issuer on certificate.
  if(!(name = X509_get_subject_name(ca_cert))) {
    PyErr_SetString(PyExc_Exception, "Error getting subject from CA certificate");
    goto end;
  }
  if(X509_set_issuer_name(cert, name) != 1) {
    PyErr_SetString(PyExc_Exception, "Error setting issuer");
    goto end;
  }

  // Code for reading public key from memory. This will be used if we later
  // want to optimize for speed by keeping PEMs in memory.
  //BIO* keyBio = BIO_new_mem_buf(TESTING_public_key_path, sizeof(TESTING_public_key_path));
  //EVP_PKEY* public_key = PEM_read_bio_PUBKEY(keyBio,NULL,NULL,NULL);
  //BIO_free_all(keyBio);

  // Read public key from file and add to cert.
  if(!(fp = fopen(public_key_path, "r"))) {
    PyErr_SetString(PyExc_Exception, "Error opening public key file");
    goto end;
  }
  if(!(public_key = PEM_read_PUBKEY(fp, NULL, NULL, NULL))) {
    PyErr_SetString(PyExc_Exception, "Error while reading public key file (must be PEM)");
    goto end;
  }
  fclose(fp);
  fp = NULL;
  if(X509_set_pubkey(cert, public_key) != 1) {
    PyErr_SetString(PyExc_Exception, "Error adding public key");
    goto end;
  }

  // Set the expiration time for the certificate.
  if(!(X509_gmtime_adj(X509_get_notBefore(cert), 0))) {
    PyErr_SetString(PyExc_Exception, "Error setting notBefore date");
    goto end;
  }
  int expire_seconds = long_term ? EXPIRE_SECS_LONG_TERM : EXPIRE_SECS;
  if(!(X509_gmtime_adj(X509_get_notAfter(cert), expire_seconds))) {
    PyErr_SetString(PyExc_Exception, "Error setting notAfter");
    goto end;
  }

  // Add X.509 v3 extensions.
  X509V3_set_ctx(&ctx, ca_cert, cert, NULL, NULL, 0);
  for(i = 0; i < EXT_COUNT; i++) {
    X509_EXTENSION* ext = X509V3_EXT_conf(NULL, &ctx, ext_ent[i].key, ext_ent[i].value);
    if(!ext) {
  	  //fprintf(stderr, "Error on \"%s = %s\"\n", ext_ent[i].key, ext_ent[i].value);
      PyErr_SetString(PyExc_Exception, "Error creating X.509 v3 extension object");
      goto end;
    }
    if(!X509_add_ext(cert, ext, -1)) {
  	  //fprintf(stderr, "Error on \"%s = %s\"\n", ext_ent[i].key, ext_ent[i].value);
      PyErr_SetString(PyExc_Exception, "Error adding X.509 v3 extension object");
      goto end;
  	}
    X509_EXTENSION_free(ext);
  }

  // Add the DataONE SubjectInfo custom extension.
  int session_nid = OBJ_create(SUBJECT_INFO_OID, "SubjectInfo",
                               "DataONE SubjectInfo XML Object");
  X509V3_EXT_add_alias(session_nid, NID_netscape_comment);
  X509_EXTENSION* ex = X509V3_EXT_conf_nid(NULL, NULL, session_nid,
                                           subject_info);
  X509_add_ext(cert, ex, -1);

  // Add subjectAltName.
  if(!(subject_alt_name_extension = X509V3_EXT_conf(NULL, NULL, "subjectAltName",
                                     subject_alt_name))) {
    PyErr_SetString(PyExc_Exception, "Error creating subjectAltName extension");
    goto end;
  }
  if(!X509_add_ext(cert, subject_alt_name_extension, -1)) {
    PyErr_SetString(PyExc_Exception, "Error adding subjectAltName to "
                    "certificate");
    goto end;
  }

  // Sign the certificate with the CA private key.
  const EVP_MD *digest = NULL;
  if(EVP_PKEY_type(ca_private_key->type) == EVP_PKEY_DSA) {
    digest = EVP_dss1();
  }
  else if(EVP_PKEY_type(ca_private_key->type) == EVP_PKEY_RSA) {
    digest = EVP_sha1();
  }
  else {
    PyErr_SetString(PyExc_Exception, "Error checking CA private key for a valid digest");
    goto end;
  }
  if(!(X509_sign(cert, ca_private_key, digest))) {
    PyErr_SetString(PyExc_Exception, "Error signing certificate");
    goto end;
  }

  // Write the completed certificate.
  if(!(fp = fopen(cert_out_path, "w"))) {
    PyErr_SetString(PyExc_Exception, "Error opening certificate file for write");
    goto end;
  }
  if(PEM_write_X509(fp, cert) != 1) {
    PyErr_SetString(PyExc_Exception, "Error while writing certificate");
    goto end;
  }
  fclose(fp);
  fp = NULL;

  status = SUCCESS;

end:
  if (fp) {
    fclose(fp);
  }
  if(ca_cert) {
    X509_free(ca_cert);
  }
  if(cert) {
    X509_free(cert);
  }
  OBJ_cleanup();
  return status;
}


static PyObject* d1_x509v3_certificate_generator_generate(PyObject *self,
                                                      PyObject *args) {
  // Convert the Python arguments to C terminated strings.
  // Args:
  // CA file path
  // CA private key path
  // Public key path
  // Certificate output path
  // SubjectInfo xml
  char* cert_out_path;
  char* ca_cert_path;
  char* ca_key_path;
  char* ca_key_pw;
  char* public_key_path;
  char* subject_info;
  char* subject_alt_name;
  PyObject* py_rdns;
  int long_term;

  if(!PyArg_ParseTuple(args, "sssssssOi",
                       &cert_out_path, &ca_cert_path,
                       &ca_key_path, &ca_key_pw, &public_key_path,
                       &subject_info, &subject_alt_name, &py_rdns,
                       &long_term)) {
    return NULL;
  }

  // Parse out the DN, provided as a tuple of type-value tuples.
  PyErr_SetString(PyExc_Exception, "DN must be a tuple of type-value tuples");
  if (!PyTuple_Check(py_rdns)) {
    return NULL;
  }
  int n_rdns = PyTuple_Size(py_rdns);
  struct rdn* rdns = (struct rdn*)malloc(sizeof(struct rdn) * n_rdns);
  int i;
  for(i = 0; i < n_rdns; ++i) {
    PyObject* type_value = PyTuple_GetItem(py_rdns, i);
    if (!PyTuple_Check(type_value)) {
      return NULL;
    }
    if (!PyArg_ParseTuple(type_value, "ss", &rdns[i].type, &rdns[i].value)) {
      return NULL;
    }
  }
  PyErr_Clear();

  // Generate the certificate.
  int ret = generate(cert_out_path, ca_cert_path, ca_key_path,
                                 ca_key_pw, public_key_path, subject_info,
                                 subject_alt_name, rdns, n_rdns, long_term);
  if(!ret) {
    // generate() sets an error string if unsuccessful. Returning
    // NULL raises a Python exception with that string.
    return NULL;
  }

  // Return NoneType.
  return Py_BuildValue("", 0);
}


static PyMethodDef d1_x509v3_certificate_generator_methods[] = {
  {"generate",  d1_x509v3_certificate_generator_generate, METH_VARARGS,
  "Generate X.509 v3 certificate that contains DataONE Session (SubjectInfo)"},
  {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC initd1_x509v3_certificate_generator(void) {
  // Initialize OpenSSL.
  //seed_prng();
  ERR_load_crypto_strings();
  //SSL_load_error_strings();
  ERR_load_BIO_strings();
  OpenSSL_add_all_algorithms();
  // Initialize Python module.
 (void) Py_InitModule("d1_x509v3_certificate_generator",
                      d1_x509v3_certificate_generator_methods);
}

//int main(int argc, char *argv[]) {
//  /* Pass argv[0] to the Python interpreter */
//  Py_SetProgramName(argv[0]);
//
//  /* Initialize the Python interpreter.  Required. */
//  Py_Initialize();
//
//  /* Add a static module */
//  initd1_x509v3_certificate_generator();
//
//  return 0;
//}
