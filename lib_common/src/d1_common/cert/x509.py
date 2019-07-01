# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for processing X.509 v3 certificates."""

import datetime
import ipaddress
import logging
import re
import socket
import ssl
import urllib.parse

import contextlib
import cryptography
import cryptography.hazmat
import cryptography.hazmat.backends
import cryptography.hazmat.primitives
import cryptography.hazmat.primitives.asymmetric
import cryptography.hazmat.primitives.asymmetric.ec
import cryptography.hazmat.primitives.asymmetric.rsa
import cryptography.hazmat.primitives.hashes
import cryptography.hazmat.primitives.serialization
import cryptography.x509
import cryptography.x509.oid
import pyasn1.codec.der
import pyasn1.codec.der.decoder

import d1_common.const

OID_TO_SHORT_NAME_DICT = {
    """Map OID to short names for use when creating DataONE compliant serialization of the
    DN.
    
    This is pulled from LDAPv3 RFCs (RFC 4510 TO RFC 4519).
    
    The set of OIDs that can occur in RDNs seems to be poorly defined. RFC 4514 refers to
    a registry but, if the registry exists, it's probably too large to be useful to us. So
    we pull in OIDs for a small set that can be expected in RDNs in certs from CILogon and
    will just need to expand it if required.
    
    RFC 4514 section 2: Converting DistinguishedName from ASN.1 to a String
    
    If the AttributeType is defined to have a short name (descriptor) [RFC4512] and that
    short name is known to be registered [REGISTRY] [RFC4520] as identifying the
    AttributeType , that short name a <descr>, is used.  Otherwise the AttributeType is
    encoded as the dotted-decimal encoding , a <numericoid> of its OBJECT IDENTIFIER. The
    <descr> and <numericoid> are defined in [RFC4512].
    """
    "0.9.2342.19200300.100.1.1": "UID",  # userId
    "0.9.2342.19200300.100.1.25": "DC",  # domainComponent
    "1.2.840.113549.1.9.1": "email",  # emailAddress
    "2.5.4.3": "CN",  # commonName
    "2.5.4.4": "SN",  # surname
    "2.5.4.6": "C",  # countryName
    "2.5.4.7": "L",  # localityName
    "2.5.4.8": "ST",  # stateOrProvinceName
    "2.5.4.9": "STREET",  # streetAddress
    "2.5.4.10": "O",  # organizationName
    "2.5.4.11": "OU",  # organizationalUnitName
}

DATAONE_SUBJECT_INFO_OID = "1.3.6.1.4.1.34998.2.1"
AUTHORITY_INFO_ACCESS_OID = "1.3.6.1.5.5.7.1.1"  # authorityInfoAccess
CA_ISSUERS_OID = "1.3.6.1.5.5.7.48.2"  # caIssuers
OCSP_OID = "1.3.6.1.5.5.7.48.1"  # OCSP

UBUNTU_CA_BUNDLE_PATH = "/etc/ssl/certs/ca-certificates.crt"


# Subjects


def extract_subjects(cert_pem):
    """Extract primary subject and SubjectInfo from a DataONE PEM (Base64) encoded X.509
    v3 certificate.

    Args:
      cert_pem: str or bytes
        PEM (Base64) encoded X.509 v3 certificate

    Returns:
      2-tuple:
        - Primary subject (str) extracted from the certificate DN.
        - SubjectInfo (XML str) if present (see the subject_info module for parsing)

    """
    cert_obj = deserialize_pem(cert_pem)
    return extract_subject_from_dn(cert_obj), extract_subject_info_extension(cert_obj)


def extract_subject_from_dn(cert_obj):
    """Serialize a DN to a DataONE subject string.

    Args:
      cert_obj: cryptography.Certificate

    Returns:
      str:
        Primary subject extracted from the certificate DN.

    The certificate DN (DistinguishedName) is a sequence of RDNs
    (RelativeDistinguishedName). Each RDN is a set of AVAs (AttributeValueAssertion /
    AttributeTypeAndValue). A DataONE subject is a plain string. As there is no single
    standard specifying how to create a string representation of a DN, DataONE selected
    one of the most common ways, which yield strings such as:

    CN=Some Name A123,O=Some Organization,C=US,DC=Some Domain,DC=org

    In particular, the sequence of RDNs is reversed. Attribute values are escaped,
    attribute type and value pairs are separated by "=", and AVAs are joined together
    with ",". If an RDN contains an unknown OID, the OID is serialized as a dotted
    string.

    As all the information in the DN is preserved, it is not possible to create the
    same subject with two different DNs, and the DN can be recreated from the subject.

    """
    return ",".join(
        "{}={}".format(
            OID_TO_SHORT_NAME_DICT.get(v.oid.dotted_string, v.oid.dotted_string),
            rdn_escape(v.value),
        )
        for v in reversed(list(cert_obj.subject))
    )


def create_mn_dn(node_urn):
    """Create a certificate DN suitable for use in Member Node client side certificates
    issued by DataONE, and thus in Certificate Signing Requests (CSR). The DN will be on
    the form:

        DC=org, DC=dataone, CN=urn:node:<ID>

    where <ID> typically is a short acronym for the name of the organization responsible
    for the Member Node.

    The DN is formatted into a DataONE subject, which is used in authentication,
    authorization and event tracking.

    Args:
        node_urn: str
            Node URN. E.g.,
                Production certificate: ``urn:node:XYZ``.
                Test certificate ``urn:node:mnTestXYZ``.

    Returns:
        cryptography.x509.Name
    """
    return create_simple_dn(node_urn, domain_componet_list=["org", "dataone"])


def create_simple_dn(common_name_str, domain_componet_list=None):
    """Create a simple certificate DN suitable for use in testing and for generating self signed CA and other certificate.

        DC=local, DC=dataone, CN=<common name>

    Args:
        common_name_str: The Common Name to use for the certificate.
            DataONE uses simple DNs without physical location information, so only the
            ``common_name_str`` (``CommonName``) needs to be specified.

            For Member Node Client Side certificates or CSRs, ``common_name_str`` is the
            ``node_id``, e.g., ``urn:node:ABCD`` for production, or
            ``urn:node:mnTestABCD`` for the test environments.

            For a local CA, something like ``localCA`` may be used.

            For a locally trusted client side certificate, something like
            ``localClient`` may be used.

        domain_componet_list: list
            Optionally set custom domain components.

        fqdn_list: list of str
            List of Fully Qualified Domain Names (FQDN) and/or IP addresses for which
            this certificate will provide authentication.

            E.g.: ['my.membernode.org', '1.2.3.4']

            This is mainly useful for creating a self signed server side certificate or
            a CSR that will be submitted to a trusted CA, such as Verisign, for signing.

    Returns:
        cryptography.x509.Name
    """
    domain_componet_list = domain_componet_list or ["local", "dataone"]
    attr_list = []
    for dc_str in domain_componet_list:
        attr_list.append(
            cryptography.x509.NameAttribute(
                cryptography.x509.oid.NameOID.DOMAIN_COMPONENT, dc_str
            )
        )
    attr_list.append(
        cryptography.x509.NameAttribute(
            cryptography.x509.oid.NameOID.COMMON_NAME, common_name_str
        )
    )
    return cryptography.x509.Name(attr_list)


# CSR


def generate_csr(private_key_bytes, dn, fqdn_list=None):
    """Generate a Certificate Signing Request (CSR).

    Args:
        private_key_bytes: bytes
            Private key with which the CSR will be signed.

        dn: cryptography.x509.Name
            The dn can be built by passing a list of cryptography.x509.NameAttribute to
            cryptography.x509.Name.

            Simple DNs can be created with the ``create_dn*`` functions in this module.

        fqdn_list: list of str
            List of Fully Qualified Domain Names (FQDN) and/or IP addresses for which
            this certificate will provide authentication.

            E.g.: ['my.membernode.org', '1.2.3.4']

            This is mainly useful for creating a self signed server side certificate or
            a CSR that will be submitted to a trusted CA, such as Verisign, for signing.

    Returns:
        cryptography.x509.CertificateSigningRequest
    """
    csr = cryptography.x509.CertificateSigningRequestBuilder(subject_name=dn)
    if fqdn_list:
        csr.add_extension(
            extension=cryptography.x509.SubjectAlternativeName(
                [cryptography.x509.DNSName(v) for v in fqdn_list]
            ),
            critical=False,
        )
    return csr.sign(
        private_key=private_key_bytes,
        algorithm=cryptography.hazmat.primitives.hashes.SHA256(),
        backend=cryptography.hazmat.backends.default_backend(),
    )


# PEM


def deserialize_pem(cert_pem):
    """Deserialize PEM (Base64) encoded X.509 v3 certificate.

    Args:
      cert_pem: str or bytes
        PEM (Base64) encoded X.509 v3 certificate

    Returns:
      cert_obj: cryptography.Certificate

    """
    if isinstance(cert_pem, str):
        cert_pem = cert_pem.encode("utf-8")
    return cryptography.x509.load_pem_x509_certificate(
        data=cert_pem, backend=cryptography.hazmat.backends.default_backend()
    )


def deserialize_pem_file(cert_path):
    """Deserialize PEM (Base64) encoded X.509 v3 certificate in file.

    Args:
      cert_path: str or bytes
        Path to PEM (Base64) encoded X.509 v3 certificate file

    Returns:
      cert_obj: cryptography.Certificate

    """
    with open(cert_path, "rb") as f:
        return deserialize_pem(f.read())


def serialize_cert_to_pem(cert_obj):
    """Serialize certificate to PEM.

    The certificate can be also be a Certificate Signing Request (CSR).

    Args:
      cert_obj: cryptography.Certificate

    Returns:
      bytes: PEM encoded certificate

    """
    return cert_obj.public_bytes(
        encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM
    )


# DataONE SubjectInfo Extension


def extract_subject_info_extension(cert_obj):
    """Extract DataONE SubjectInfo XML doc from certificate.

    Certificates issued by DataONE may include an embedded XML doc containing
    additional information about the subject specified in the certificate DN. If
    present, the doc is stored as an extension with an OID specified by DataONE and
    formatted as specified in the DataONE SubjectInfo schema definition.

    Args:
      cert_obj: cryptography.Certificate

    Returns:
      str : SubjectInfo XML doc if present, else None

    """
    try:
        subject_info_der = cert_obj.extensions.get_extension_for_oid(
            cryptography.x509.oid.ObjectIdentifier(DATAONE_SUBJECT_INFO_OID)
        ).value.value
        return str(pyasn1.codec.der.decoder.decode(subject_info_der)[0])
    except Exception as e:
        logging.debug('SubjectInfo not extracted. reason="{}"'.format(e))


# Download Certificate


def download_as_der(
    base_url=d1_common.const.URL_DATAONE_ROOT,
    timeout_sec=d1_common.const.DEFAULT_HTTP_TIMEOUT,
):
    """Download public certificate from a TLS/SSL web server as DER encoded ``bytes``.

    If the certificate is being downloaded in order to troubleshoot validation issues,
    the download itself may fail due to the validation issue that is being investigated.
    To work around such chicken-and-egg problems, temporarily wrap calls to the
    download_* functions with the ``disable_cert_validation()`` context manager (also in
    this module).

    Args:
        base_url : str
          A full URL to a DataONE service endpoint or a server hostname
        timeout_sec : int or float
          Timeout for the SSL socket operations
    Returns:
      bytes: The server's public certificate as DER encoded bytes.

    """
    # TODO: It is unclear which SSL and TLS protocols are supported by the method
    # currently being used. The current method and the two commented out below
    # should be compared to determine which has the best compatibility with current
    # versions of Python and current best practices for protocol selection.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_sec)
    ssl_socket = ssl.wrap_socket(sock)
    url_obj = urllib.parse.urlparse(base_url)
    ssl_socket.connect((url_obj.netloc, 443))
    return ssl_socket.getpeercert(binary_form=True)

    # (1)
    # ssl_context = ssl.create_default_context()
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    # ssl_socket = ssl_context.wrap_socket(
    #   socket.socket(),
    #   server_hostname=django.conf.settings.DATAONE_ROOT
    # )
    #
    # (2)
    # ssl_protocol_list: PROTOCOL_SSLv2, PROTOCOL_SSLv3, PROTOCOL_SSLv23,
    # PROTOCOL_TLSv1, PROTOCOL_TLSv1_1,  PROTOCOL_TLSv1_2
    #
    # Check if protocols should be checked in order of preference or if the
    # function will do that.
    #
    # for ssl_protocol_str in ssl_protocol_list:
    #   print ssl_protocol_str
    #   try:
    #     return ssl.get_server_certificate(
    #       addr=(hostname_str, int(port_str)),
    #       ssl_version=getattr(ssl, ssl_protocol_str),
    #       ca_certs=UBUNTU_CA_BUNDLE_PATH,
    #     )
    #   except ssl.SSLError as e:
    #     logging.info('SSL: {}'.format(str(e)))
    #     if ssl_protocol_str is ssl_protoc`ol_list[-1]:
    #       raise


# Download


def download_as_pem(
    base_url=d1_common.const.URL_DATAONE_ROOT,
    timeout_sec=d1_common.const.DEFAULT_HTTP_TIMEOUT,
):
    """Download public certificate from a TLS/SSL web server as PEM encoded string.

    Also see download_as_der().

    Args:
        base_url : str
          A full URL to a DataONE service endpoint or a server hostname
        timeout_sec : int or float
          Timeout for the SSL socket operations

    Returns:
      str: The certificate as a PEM encoded string.

    """
    return ssl.DER_cert_to_PEM_cert(download_as_der(base_url, timeout_sec))


def download_as_obj(
    base_url=d1_common.const.URL_DATAONE_ROOT,
    timeout_sec=d1_common.const.DEFAULT_HTTP_TIMEOUT,
):
    """Download public certificate from a TLS/SSL web server as Certificate object.

    Also see download_as_der().

    Args:
        base_url : str
          A full URL to a DataONE service endpoint or a server hostname
        timeout_sec : int or float
          Timeout for the SSL socket operations

    Returns:
      cryptography.Certificate

    """
    return decode_der(download_as_der(base_url, timeout_sec))


def decode_der(cert_der):
    """Decode cert DER string to Certificate object.

    Args:
      cert_der : Certificate as a DER encoded string

    Returns:
      cryptography.Certificate()

    """
    return cryptography.x509.load_der_x509_certificate(
        data=cert_der, backend=cryptography.hazmat.backends.default_backend()
    )


# noinspection PyProtectedMember
@contextlib.contextmanager
def disable_cert_validation():
    """Context manager to temporarily disable certificate validation in the standard SSL
    library.

    Note: This should not be used in production code but is sometimes useful for
    troubleshooting certificate validation issues.

    By design, the standard SSL library does not provide a way to disable verification
    of the server side certificate. However, a patch to disable validation is described
    by the library developers. This context manager allows applying the patch for
    specific sections of code.

    """
    current_context = ssl._create_default_https_context
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        yield
    finally:
        ssl._create_default_https_context = current_context


def extract_issuer_ca_cert_url(cert_obj):
    """Extract issuer CA certificate URL from certificate.

    Certificates may include a URL where the root certificate for the CA which was used
    for signing the certificate can be downloaded. This function returns the URL if
    present.

    The primary use for this is to fix validation failure due to non-trusted issuer by
    downloading the root CA certificate from the URL and installing it in the local
    trust store.

    Args:
      cert_obj: cryptography.Certificate

    Returns:
      str: Issuer certificate URL if present, else None

    """
    for extension in cert_obj.extensions:
        if extension.oid.dotted_string == AUTHORITY_INFO_ACCESS_OID:
            authority_info_access = extension.value
            for access_description in authority_info_access:
                if access_description.access_method.dotted_string == CA_ISSUERS_OID:
                    return access_description.access_location.value


# Private key


def serialize_private_key_to_pem(private_key, passphrase_bytes=None):
    """Serialize private key to PEM.

    Args:
      private_key:
      passphrase_bytes:

    Returns:
      bytes: PEM encoded private key

    """
    return private_key.private_bytes(
        encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM,
        format=cryptography.hazmat.primitives.serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=cryptography.hazmat.primitives.serialization.BestAvailableEncryption(
            passphrase_bytes
        )
        if passphrase_bytes is not None
        else cryptography.hazmat.primitives.serialization.NoEncryption(),
    )


def generate_private_key(key_size=2048):
    """Generate a private key."""
    return cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=cryptography.hazmat.backends.default_backend(),
    )


# Public Key


def get_public_key_pem(cert_obj):
    """Extract public key from certificate as PEM encoded PKCS#1.

    Args:
      cert_obj: cryptography.Certificate

    Returns:
      bytes: PEM encoded PKCS#1 public key.

    """
    return cert_obj.public_key().public_bytes(
        encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM,
        format=cryptography.hazmat.primitives.serialization.PublicFormat.PKCS1,
    )


# File


def save_pem(pem_path, pem_bytes):
    """Save PEM encoded bytes to file."""
    with open(pem_path, "wb") as f:
        f.write(pem_bytes)


def load_csr(pem_path):
    """Load CSR from PEM encoded file."""
    with open(pem_path, "rb") as f:
        return cryptography.x509.load_pem_x509_csr(
            data=f.read(), backend=cryptography.hazmat.backends.default_backend()
        )


def load_private_key(pem_path, passphrase_bytes=None):
    """Load private key from PEM encoded file."""
    with open(pem_path, "rb") as f:
        return cryptography.hazmat.primitives.serialization.load_pem_private_key(
            data=f.read(),
            password=passphrase_bytes,
            backend=cryptography.hazmat.backends.default_backend(),
        )


# Client Side Certificate


def generate_cert(ca_issuer, ca_key, csr_subject, csr_pub_key):
    # Various details about who we are. For a self-signed certificate the
    # subject and issuer are always the same.
    # Sign our certificate with our private key
    return (
        cryptography.x509.CertificateBuilder()
        .subject_name(csr_subject)
        .issuer_name(ca_issuer)
        .public_key(csr_pub_key)
        .serial_number(cryptography.x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(
            # Our certificate will be valid for 10 days
            datetime.datetime.utcnow()
            + datetime.timedelta(days=10)
        )
        .add_extension(
            extension=cryptography.x509.SubjectAlternativeName(
                [cryptography.x509.DNSName("localhost")]
            ),
            critical=False,
        )
        .sign(
            private_key=ca_key,
            algorithm=cryptography.hazmat.primitives.hashes.SHA256(),
            backend=cryptography.hazmat.backends.default_backend(),
        )
    )


def serialize_cert_to_der(cert_obj):
    """Serialize certificate to DER.

    Args:
      cert_obj: cryptography.Certificate

    Returns:
      bytes: DER encoded certificate

    """
    return cert_obj.public_bytes(
        cryptography.hazmat.primitives.serialization.Encoding.DER
    )


# CA


def generate_ca_cert(
    dn, private_key, fqdn_str=None, public_ip=None, private_ip=None, valid_days=10 * 365
):
    """Args:

        dn: cryptography.x509.Name
            A cryptography.x509.Name holding a sequence of cryptography.x509.NameAttribute objects.

            See the create_dn* functions.

        private_key: RSAPrivateKey, etc

        fqdn_str:
        public_ip:
        private_ip:

        valid_days: int
            Number of days from now until the certificate expires.

    Returns:

    """
    # best practice seem to be to include the hostname in the SAN, which *SHOULD*
    # mean COMMON_NAME is ignored.
    # allow addressing by IP, for when you don't have real DNS (common in most
    # testing scenarios)
    # openssl wants DNSnames for ips
    # cryptography.x509.DNSName(private_ip),

    alt_name_list = [cryptography.x509.DNSName("localhost")]

    if fqdn_str:
        alt_name_list.append(cryptography.x509.DNSName(fqdn_str))

    if public_ip:
        alt_name_list.append(cryptography.x509.DNSName(public_ip))
        alt_name_list.append(
            cryptography.x509.IPAddress(ipaddress.IPv4Address(public_ip))
        )

    if private_ip:
        alt_name_list.append(cryptography.x509.DNSName(private_ip))
        alt_name_list.append(
            cryptography.x509.IPAddress(ipaddress.IPv4Address(private_ip))
        )

    alt_names = cryptography.x509.SubjectAlternativeName(alt_name_list)

    # path_len=0: This cert can only sign itself, not other certs.
    basic_contraints = cryptography.x509.BasicConstraints(ca=True, path_length=0)
    now = datetime.datetime.utcnow()
    return (
        cryptography.x509.CertificateBuilder()
        .subject_name(dn)
        .issuer_name(dn)
        .public_key(private_key.public_key())
        .serial_number(cryptography.x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=valid_days))
        .add_extension(basic_contraints, critical=False)
        .add_extension(alt_names, critical=False)
        .sign(
            private_key=private_key,
            algorithm=cryptography.hazmat.primitives.hashes.SHA256(),
            backend=cryptography.hazmat.backends.default_backend(),
        )
    )


# Misc


def input_key_passphrase(applicable_str="private key"):
    passphrase_str = input(
        "Passphrase for {} (Press Enter for no passphrase): ".format(applicable_str)
    )
    if passphrase_str == "":
        return None
    return passphrase_str.encode("utf-8")


def check_cert_type(cert):
    public_key = cert.public_key()
    if isinstance(
        public_key, cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey
    ):
        print("IS RSA")
    elif isinstance(
        public_key, cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey
    ):
        print("IS EllipticCurvePublicKey")
    else:
        print("UNKNOWN")


def rdn_escape(rdn_str):
    """Escape string for use as an RDN (RelativeDistinguishedName)

    The following chars must be escaped in RDNs: , = + < > # ; \ "

    Args:
      rdn_str : str

    Returns:
      str: Escaped string ready for use in an RDN (.)

    """
    return re.sub(r"([,=+<>#;\\])", r"\\\1", rdn_str)


# noinspection PyProtectedMember
def log_cert_info(logger, msg_str, cert_obj):
    """Dump basic certificate values to the log.

    Args:
      logger: Logger
        Logger to which to write the certificate values.

      msg_str: str
        A message to write to the log before the certificate values.

      cert_obj: cryptography.Certificate
        Certificate containing values to log.

    Returns:
      None

    """
    list(
        map(
            logger,
            ["{}:".format(msg_str)]
            + ["  {}: {}".format(k, v) for k, v in get_cert_info_list(cert_obj)],
        )
    )


# noinspection PyProtectedMember
def get_cert_info_list(cert_obj):
    """Get a list of certificate values.

    Args:
      cert_obj: cryptography.Certificate
        Certificate containing values to retrieve.

    Returns:
      list of tup: Certificate value name, value

    """
    return [
        ("Subject", _get_val_str(cert_obj, ["subject", "value"], reverse=True)),
        ("Issuer", _get_val_str(cert_obj, ["issuer", "value"], reverse=True)),
        ("Not Valid Before", cert_obj.not_valid_before.isoformat()),
        ("Not Valid After", cert_obj.not_valid_after.isoformat()),
        (
            "Subject Alt Names",
            _get_ext_val_str(cert_obj, "SUBJECT_ALTERNATIVE_NAME", ["value", "value"]),
        ),
        (
            "CRL Distribution Points",
            _get_ext_val_str(
                cert_obj,
                "CRL_DISTRIBUTION_POINTS",
                ["value", "full_name", "value", "value"],
            ),
        ),
        (
            "Authority Access Location",
            extract_issuer_ca_cert_url(cert_obj) or "<not found>",
        ),
    ]


def get_extension_by_name(cert_obj, extension_name):
    """Get a standard certificate extension by attribute name.

    Args:
      cert_obj: cryptography.Certificate
        Certificate containing a standard extension.

      extension_name : str
        Extension name. E.g., 'SUBJECT_DIRECTORY_ATTRIBUTES'.

    Returns:
      Cryptography.Extension

    """
    try:
        return cert_obj.extensions.get_extension_for_oid(
            getattr(cryptography.x509.oid.ExtensionOID, extension_name)
        )
    except cryptography.x509.ExtensionNotFound:
        pass


# Private


def _get_val_list(obj, path_list, reverse=False):
    """Extract values from nested objects by attribute names.

    Objects contain attributes which are named references to objects. This will descend
    down a tree of nested objects, starting at the given object, following the given
    path.

    Args:
      obj: object
        Any type of object

      path_list: list
        Attribute names

      reverse: bool
        Reverse the list of values before concatenation.

    Returns:
      list of objects

    """
    try:
        y = getattr(obj, path_list[0])
    except AttributeError:
        return []
    if len(path_list) == 1:
        return [y]
    else:
        val_list = [x for a in y for x in _get_val_list(a, path_list[1:], reverse)]
        if reverse:
            val_list.reverse()
        return val_list


def _get_val_str(obj, path_list=None, reverse=False):
    """Extract values from nested objects by attribute names and concatenate their
    string representations.

    Args:
      obj: object
        Any type of object

      path_list: list
        Attribute names

      reverse: bool
        Reverse the list of values before concatenation.

    Returns:
      str: Concatenated extracted values.

    """
    val_list = _get_val_list(obj, path_list or [], reverse)
    return "<not found>" if obj is None else " / ".join(map(str, val_list))


def _get_ext_val_str(cert_obj, extension_name, path_list=None):
    """Get value from certificate extension.

    Args:
      cert_obj: cryptography.Certificate
        Certificate containing a standard extension.

      extension_name : str
        Extension name. E.g., 'SUBJECT_DIRECTORY_ATTRIBUTES'.

      path_list: list
        Attribute names

    Returns:
      str : String value of extension

    """
    return _get_val_str(
        get_extension_by_name(cert_obj, extension_name), path_list or []
    )
