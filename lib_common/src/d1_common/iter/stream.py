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
import os

import d1_common.const


class StreamIterator(object):
    """Generator that returns a stream in chunks.

    In this context, a stream is anything with a ``read()`` method and, if the client
    requires it, a way to determine the total number of elements that will be returned
    by the ``read()`` method at any point during iteration.

    Typical sources for streams are files and HTML responses.

    """

    def __init__(self, stream, chunk_size=d1_common.const.DEFAULT_CHUNK_SIZE):
        """Args: stream: Object with ``read()`` method, such as an open file.

        chunk_size: int     Max number of elements to return in each chunk. The last
        chunk will     normally be smaller. Other chunks may be smaller as well, but
        never     empty.

        """
        self._stream = stream
        self._chunk_size = chunk_size

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if hasattr(self._stream, "close"):
            self._stream.close()

    def __iter__(self):
        """Returns: Chunks of ``read()`` on stream.

        E.g., ``bytes`` for a file opened in binary mode and ``str`` for a UTF-8 file
        opened with ``encoding='UTF-8'``.

        """
        while True:
            chunk_str = self._stream.read(self._chunk_size)
            if not chunk_str:
                break
            yield chunk_str

    @property
    def size(self):
        """Returns:

        int : The total number of bytes that will be returned by the iterator.

        """
        if hasattr(self._stream, "len"):
            return len(self._stream)
        elif hasattr(self._stream, "fileno"):
            return os.fstat(self._stream.fileno()).st_size
        else:
            cur_pos = self._stream.tell()
            size = self._stream.seek(0, os.SEEK_END)
            self._stream.seek(cur_pos)
            return size
