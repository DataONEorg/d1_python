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
"""JSON Web Token (JWT) parsing and validation.

- http://self-issued.info/docs/draft-jones-json-web-token-01.html

JWT representations:

- bu64: A URL safe flavor of Base64 used by JWTs
- jwt_bu64: A complete JWT consisting of three dot separated bu64 encoded parts:
  (header_bu64, payload_bu64, signature_bu64)
- jwt_tup: A complete JWT consisting of a tuple of 3 decoded (raw) parts: (header_str,
  payload_str, signature_str)

"""

import base64
import datetime
import hashlib
import json
import logging

import jwt

import d1_common.cert
import d1_common.cert.x509
import d1_common.date_time

CLAIM_LIST = [
    # JSON key, title, is_date
    ('iss', 'Issuer', False),
    ('iat', 'Issued At', True),
    ('exp', 'Expiration Time', True),
    ('nbf', 'Not Before Time', True),
    ('aud', 'Audience', False),
]


def get_subject_with_local_validation(jwt_bu64, cert_obj):
    """Validate the JWT and return the subject it contains.

    - The JWT is validated by checking that it was signed with a CN certificate.
    - The returned subject can be trusted for authz and authn operations.

    - Possible validation errors include:

        - A trusted (TLS/SSL) connection could not be made to the CN holding the
          signing certificate.
        - The JWT could not be decoded.
        - The JWT signature signature was invalid.
        - The JWT claim set contains invalid "Not Before" or "Expiration Time" claims.

    Args:
      jwt_bu64: bytes
        The JWT encoded using a a URL safe flavor of Base64.

      cert_obj: cryptography.Certificate
        Public certificate used for signing the JWT (typically the CN cert).

    Returns:
      - On successful validation, the subject contained in the JWT is returned.

      - If validation fails for any reason, errors are logged and None is returned.

    """
    try:
        jwt_dict = validate_and_decode(jwt_bu64, cert_obj)
    except JwtException as e:
        return log_jwt_bu64_info(logging.error, str(e), jwt_bu64)
    try:
        return jwt_dict['sub']
    except LookupError:
        log_jwt_dict_info(logging.error, 'Missing "sub" key', jwt_dict)


def get_subject_with_remote_validation(jwt_bu64, base_url):
    """Same as get_subject_with_local_validation() except that the signing certificate
    is automatically downloaded from the CN.

    - Additional possible validations errors:

      - The certificate could not be retrieved from the root CN.

    """
    cert_obj = d1_common.cert.x509.download_as_obj(base_url)
    return get_subject_with_local_validation(jwt_bu64, cert_obj)


def get_subject_with_file_validation(jwt_bu64, cert_path):
    """Same as get_subject_with_local_validation() except that the signing certificate
    is read from a local PEM file."""
    cert_obj = d1_common.cert.x509.deserialize_pem_file(cert_path)
    return get_subject_with_local_validation(jwt_bu64, cert_obj)


def get_subject_without_validation(jwt_bu64):
    """Extract subject from the JWT without validating the JWT.

    - The extracted subject cannot be trusted for authn or authz.

    Args:
      jwt_bu64: bytes
        JWT, encoded using a a URL safe flavor of Base64.

    Returns:
      str: The subject contained in the JWT.

    """
    try:
        jwt_dict = get_jwt_dict(jwt_bu64)
    except JwtException as e:
        return log_jwt_bu64_info(logging.error, str(e), jwt_bu64)
    try:
        return jwt_dict['sub']
    except LookupError:
        log_jwt_dict_info(logging.error, 'Missing "sub" key', jwt_dict)


def get_bu64_tup(jwt_bu64):
    """Split the Base64 encoded JWT to its 3 component sections.

    Args:
      jwt_bu64: bytes
        JWT, encoded using a a URL safe flavor of Base64.

    Returns:
      3-tup of Base64: Component sections of the JWT.

    """
    return jwt_bu64.strip().split(b'.')


def get_jwt_tup(jwt_bu64):
    """Split and decode the Base64 encoded JWT to its 3 component sections.

    - Reverse of get_jwt_bu64().

    Args:
      jwt_bu64: bytes
        JWT, encoded using a a URL safe flavor of Base64.

    Returns:
      3-tup of bytes: Raw component sections of the JWT.

    """
    return [decode_bu64(v) for v in get_bu64_tup(jwt_bu64)]


def get_jwt_bu64(jwt_tup):
    """Join and Base64 encode raw JWT component sections.

    - Reverse of get_jwt_tup().

    Args:
      jwt_tup: 3-tup of bytes
        Raw component sections of the JWT.

    Returns:
      jwt_bu64: bytes
        JWT, encoded using a a URL safe flavor of Base64.

    """
    return b'.'.join([encode_bu64(v) for v in jwt_tup])


def get_jwt_dict(jwt_bu64):
    """Parse Base64 encoded JWT and return as a dict.

    - JWTs contain a set of values serialized to a JSON dict. This decodes the JWT and
      returns it as a dict containing Unicode strings.
    - In addition, a SHA1 hash is added to the dict for convenience.

    Args:
      jwt_bu64: bytes
        JWT, encoded using a a URL safe flavor of Base64.

    Returns:
      dict: Values embedded in and derived from the JWT.

    """
    jwt_tup = get_jwt_tup(jwt_bu64)
    try:
        jwt_dict = json.loads(jwt_tup[0].decode('utf-8'))
        jwt_dict.update(json.loads(jwt_tup[1].decode('utf-8')))
        jwt_dict['_sig_sha1'] = hashlib.sha1(jwt_tup[2]).hexdigest()
    except TypeError as e:
        raise JwtException('Decode failed. error="{}"'.format(e))
    return jwt_dict


def validate_and_decode(jwt_bu64, cert_obj):
    """Validate the JWT and return as a dict.

    - JWTs contain a set of values serialized to a JSON dict. This decodes the JWT and
      returns it as a dict.

    Args:
      jwt_bu64: bytes
        The JWT encoded using a a URL safe flavor of Base64.

      cert_obj: cryptography.Certificate
        Public certificate used for signing the JWT (typically the CN cert).

    Raises:
      JwtException: If validation fails.

    Returns:
      dict: Values embedded in the JWT.

    """
    try:
        return jwt.decode(
            jwt_bu64.strip(), cert_obj.public_key(), algorithms=['RS256'], verify=True
        )
    except jwt.InvalidTokenError as e:
        raise JwtException('Signature is invalid. error="{}"'.format(str(e)))


def log_jwt_dict_info(log, msg_str, jwt_dict):
    """Dump JWT to log.

    Args:
      log: Logger
        Logger to which to write the message.

      msg_str: str
        A message to write to the log before the JWT values.

      jwt_dict: dict
        JWT containing values to log.

    Returns:
      None

    """
    d = ts_to_str(jwt_dict)
    # Log known items in specific order, then the rest just sorted
    log_list = [(b, d.pop(a)) for a, b, c in CLAIM_LIST if a in d] + [
        (k, d[k]) for k in sorted(d)
    ]
    list(
        map(
            log,
            ['{}:'.format(msg_str)] + ['  {}: {}'.format(k, v) for k, v in log_list],
        )
    )


def log_jwt_bu64_info(log, msg_str, jwt_bu64):
    """Dump JWT to log.

    Args:
      log: Logger
        Logger to which to write the message.

      msg_str: str
        A message to write to the log before the JWT values.

      jwt_bu64: bytes
        JWT, encoded using a a URL safe flavor of Base64.

    Returns:
      None

    """
    return log_jwt_dict_info(log, msg_str, get_jwt_dict(jwt_bu64))


def ts_to_str(jwt_dict):
    """Convert timestamps in JWT to human readable dates.

    Args:
      jwt_dict: dict
        JWT with some keys containing timestamps.

    Returns:
      dict: Copy of input dict where timestamps have been replaced with human readable
      dates.

    """
    d = ts_to_dt(jwt_dict)
    for k, v in list(d.items()):
        if isinstance(v, datetime.datetime):
            d[k] = v.isoformat().replace('T', ' ')
    return d


def ts_to_dt(jwt_dict):
    """Convert timestamps in JWT to datetime objects.

    Args:
      jwt_dict: dict
        JWT with some keys containing timestamps.

    Returns:
      dict: Copy of input dict where timestamps have been replaced with
      datetime.datetime() objects.

    """
    d = jwt_dict.copy()
    for k, v in [v[:2] for v in CLAIM_LIST if v[2]]:
        if k in jwt_dict:
            d[k] = d1_common.date_time.dt_from_ts(jwt_dict[k])
    return d


def encode_bu64(b):
    """Encode bytes to a URL safe flavor of Base64 used by JWTs.

    - Reverse of decode_bu64().

    Args:
      b: bytes
        Bytes to Base64 encode.

    Returns:
      bytes: URL safe Base64 encoded version of input.

    """
    s = base64.standard_b64encode(b)
    s = s.rstrip('=')
    s = s.replace('+', '-')
    s = s.replace('/', '_')
    return s


def decode_bu64(b):
    """Encode bytes to a URL safe flavor of Base64 used by JWTs.

    - Reverse of encode_bu64().

    Args:
      b: bytes
        URL safe Base64 encoded bytes to encode.

    Returns:
      bytes: Decoded bytes.

    """
    s = b
    s = s.replace(b'-', b'+')
    s = s.replace(b'_', b'/')
    p = len(s) % 4
    if p == 0:
        pass
    elif p == 2:
        s += b'=='
    elif p == 3:
        s += b'='
    else:
        raise ValueError('Illegal Base64url string')
    return base64.standard_b64decode(s)


class JwtException(Exception):
    """Exceptions raised directly by this module."""

    pass
