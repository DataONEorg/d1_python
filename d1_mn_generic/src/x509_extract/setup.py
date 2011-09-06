from distutils.core import setup, Extension

module1 = Extension('x509_extract_session', sources=['x509_extract_session.cpp'])

setup(
  name='Extract',
  version='1.0',
  description='Extract arbitrarty extension from X.509 certificate',
  ext_modules=[module1]
)
