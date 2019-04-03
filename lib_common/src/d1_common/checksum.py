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
"""Utilities for handling checksums.

Warning:

  The ``MD5`` checksum algorithm is not cryptographically secure. It's possible to
  craft a sequence of bytes that yields a predetermined checksum.

"""

import hashlib

import d1_common.const
import d1_common.types.dataoneTypes

DEFAULT_CHUNK_SIZE = 1024 * 1024

DATAONE_TO_PYTHON_CHECKSUM_ALGORITHM_MAP = {
    'MD5': hashlib.md5,
    'SHA1': hashlib.sha1,
    'SHA-1': hashlib.sha1,
}

# Checksum PyXB object creation


def create_checksum_object_from_stream(
    f, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
):
    """Calculate the checksum of a stream.

    Args:
      f: file-like object
        Only requirement is a ``read()`` method that returns ``bytes``.

      algorithm: str
        Checksum algorithm, ``MD5`` or ``SHA1`` / ``SHA-1``.

    Returns:
      Populated Checksum PyXB object.

    """
    checksum_str = calculate_checksum_on_stream(f, algorithm)
    checksum_pyxb = d1_common.types.dataoneTypes.checksum(checksum_str)
    checksum_pyxb.algorithm = algorithm
    return checksum_pyxb


def create_checksum_object_from_iterator(
    itr, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
):
    """Calculate the checksum of an iterator.

    Args:
      itr: iterable
        Object which supports the iterator protocol.

      algorithm: str
        Checksum algorithm, ``MD5`` or ``SHA1`` / ``SHA-1``.

    Returns:
      Populated Checksum PyXB object.

    """
    checksum_str = calculate_checksum_on_iterator(itr, algorithm)
    checksum_pyxb = d1_common.types.dataoneTypes.checksum(checksum_str)
    checksum_pyxb.algorithm = algorithm
    return checksum_pyxb


def create_checksum_object_from_bytes(
    b, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
):
    """Calculate the checksum of ``bytes``.

    Warning:
      This method requires the entire object to be buffered in (virtual) memory, which
      should normally be avoided in production code.

    Args:
      b: bytes
        Raw bytes

      algorithm: str
        Checksum algorithm, ``MD5`` or ``SHA1`` / ``SHA-1``.

    Returns:
      Populated PyXB Checksum object.

    """
    checksum_str = calculate_checksum_on_bytes(b, algorithm)
    checksum_pyxb = d1_common.types.dataoneTypes.checksum(checksum_str)
    checksum_pyxb.algorithm = algorithm
    return checksum_pyxb


# Calculate checksum


def calculate_checksum_on_stream(
    f,
    algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM,
    chunk_size=DEFAULT_CHUNK_SIZE,
):
    """Calculate the checksum of a stream.

    Args:
      f: file-like object
        Only requirement is a ``read()`` method that returns ``bytes``.

      algorithm: str
        Checksum algorithm, ``MD5`` or ``SHA1`` / ``SHA-1``.

      chunk_size : int
        Number of bytes to read from the file and add to the checksum at a time.

    Returns:
      str : Checksum as a hexadecimal string, with length decided by the algorithm.

    """
    checksum_calc = get_checksum_calculator_by_dataone_designator(algorithm)
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        checksum_calc.update(chunk)
    return checksum_calc.hexdigest()


def calculate_checksum_on_iterator(
    itr, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
):
    """Calculate the checksum of an iterator.

    Args:
      itr: iterable
        Object which supports the iterator protocol.

      algorithm: str
        Checksum algorithm, ``MD5`` or ``SHA1`` / ``SHA-1``.

    Returns:
      str : Checksum as a hexadecimal string, with length decided by the algorithm.

    """
    checksum_calc = get_checksum_calculator_by_dataone_designator(algorithm)
    for chunk in itr:
        checksum_calc.update(chunk)
    return checksum_calc.hexdigest()


def calculate_checksum_on_bytes(
    b, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
):
    """Calculate the checksum of ``bytes``.

    Warning: This method requires the entire object to be buffered in (virtual) memory,
    which should normally be avoided in production code.

    Args:
      b: bytes
        Raw bytes

      algorithm: str
        Checksum algorithm, ``MD5`` or ``SHA1`` / ``SHA-1``.

    Returns:
      str : Checksum as a hexadecimal string, with length decided by the algorithm.

    """
    checksum_calc = get_checksum_calculator_by_dataone_designator(algorithm)
    checksum_calc.update(b)
    return checksum_calc.hexdigest()


# Checksum validation


def are_checksums_equal(checksum_a_pyxb, checksum_b_pyxb):
    """Determine if checksums are equal.

    Args:
       checksum_a_pyxb, checksum_b_pyxb: PyXB Checksum objects to compare.

    Returns:
      bool
        - **True**: The checksums contain the same hexadecimal values calculated with
          the same algorithm. Identical checksums guarantee (for all practical
          purposes) that the checksums were calculated from the same sequence of bytes.
        - **False**: The checksums were calculated with the same algorithm but the
          hexadecimal values are different.

    Raises:
      ValueError
        The checksums were calculated with different algorithms, hence cannot be
        compared.

    """
    if checksum_a_pyxb.algorithm != checksum_b_pyxb.algorithm:
        raise ValueError(
            'Cannot compare checksums calculated with different algorithms. '
            'a="{}" b="{}"'.format(checksum_a_pyxb.algorithm, checksum_b_pyxb.algorithm)
        )
    return checksum_a_pyxb.value().lower() == checksum_b_pyxb.value().lower()


# Algorithm


def get_checksum_calculator_by_dataone_designator(dataone_algorithm_name):
    """Get a checksum calculator.

    Args:
      dataone_algorithm_name : str
        Checksum algorithm, ``MD5`` or ``SHA1`` / ``SHA-1``.

    Returns:
      Checksum calculator from the ``hashlib`` library

      Object that supports ``update(arg)``, ``digest()``, ``hexdigest()`` and
      ``copy()``.

    """
    return DATAONE_TO_PYTHON_CHECKSUM_ALGORITHM_MAP[dataone_algorithm_name]()


def get_default_checksum_algorithm():
    """Get the default checksum algorithm.

    Returns:
      str : Checksum algorithm that is supported by DataONE, the DataONE Python stack
      and is in common use within the DataONE federation. Currently, ``SHA-1``.

      The returned string can be passed as the ``algorithm_str`` to the functions in
      this module.

    """
    return d1_common.const.DEFAULT_CHECKSUM_ALGORITHM


def is_supported_algorithm(algorithm_str):
    """Determine if string is the name of a supported checksum algorithm.

    Args:
      algorithm_str: str
        String that may or may not contain the name of a supported algorithm.

    Returns:
      bool
        - **True**: The string contains the name of a supported algorithm and can be
          passed as the ``algorithm_str`` to the functions in this module.
        - **False**: The string is not a supported algorithm.

    """
    return algorithm_str in DATAONE_TO_PYTHON_CHECKSUM_ALGORITHM_MAP


def get_supported_algorithms():
    """Get a list of the checksum algorithms that are supported by the DataONE Python
    stack.

    Returns:
      list : List of algorithms that are supported by the DataONE Python stack and can
      be passed to as the ``algorithm_str`` to the functions in this module.

    """
    return list(DATAONE_TO_PYTHON_CHECKSUM_ALGORITHM_MAP.keys())


# Format


def format_checksum(checksum_pyxb):
    """Create string representation of a PyXB Checksum object.

    Args:
      PyXB Checksum object

    Returns:
      str : Combined hexadecimal value and algorithm name.

    """
    return '{}/{}'.format(
        checksum_pyxb.algorithm.upper().replace('-', ''), checksum_pyxb.value().lower()
    )
