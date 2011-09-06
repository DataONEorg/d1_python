#include <python2.6/Python.h>

#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/bio.h>
#include <openssl/x509v3.h>

#include <iostream>

int extract_session(unsigned char* session_buf, int session_buf_size, char *x509_cert_pem) {
  // A BIO is an I/O abstraction, it hides many of the underlying I/O details
  // from an application. If an application uses a BIO for its I/O it can
  // transparently handle SSL connections, unencrypted network connections and
  // file I/O. 
  BIO* bio;
  
  // Initializing OpenSSL
  SSL_load_error_strings();
  ERR_load_BIO_strings();
  OpenSSL_add_all_algorithms();

  //
  X509 *x509;
  BIO *i = BIO_new(BIO_s_file());
  //BIO *bio = BIO_new(BIO_s_mem());
  //BIO *o = BIO_new_fp(stdout, BIO_NOCLOSE);

  BIO_read_filename(i, "./cert_with_custom_ext.pem");
  x509 = PEM_read_bio_X509_AUX(i, NULL, NULL, NULL);
  
  // Get the DataONE Session extension.
  // TODO: Haven't found out how to loop over the extensions and find the
  // correct one, assume it's the last extension in the cert.
  int n_extensions = X509_get_ext_count(x509);
  if (!n_extensions) {
    return 0;
  }
  X509_EXTENSION* ex = X509_get_ext(x509, n_extensions - 1);
  
  // BIO_s_mem(): Return the memory BIO method function. A memory BIO is a
  // source/sink BIO which uses memory for its I/O. Data written to a memory BIO
  // is stored in a BUF_MEM structure which is extended as appropriate to
  // accommodate the stored data. 
  bio = BIO_new(BIO_s_mem());

  // Copy the octet string in ex->value to buffer.
  M_ASN1_OCTET_STRING_print(bio, ex->value);
  int len = BIO_read(bio, session_buf, session_buf_size);
  if (len == session_buf_size) {
    // Overflow.
    return 0;
  }
  session_buf[len] = '\0';
  
  BIO_free_all(bio);

  return 1;
}

static PyObject* x509_extract_session_extract(PyObject *self, PyObject *args) {
  char *x509_cert_pem;

  if (!PyArg_ParseTuple(args, "s", &x509_cert_pem)) {
    return NULL;
  }

  const int session_buf_size(1024 * 1024);
  unsigned char* session_buf((unsigned char*)malloc(session_buf_size));

  int ret = extract_session(session_buf, session_buf_size, x509_cert_pem);
  if (!ret) {
    
  }
  // TODO: Raise exception if error.

  return Py_BuildValue("s", session_buf);
}

static PyMethodDef x509_extract_session_methods[] = {
  {"extract",  x509_extract_session_extract, METH_VARARGS, "Extract DataONE Session from X.509 certificate"},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

PyMODINIT_FUNC initx509_extract_session(void) {
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
