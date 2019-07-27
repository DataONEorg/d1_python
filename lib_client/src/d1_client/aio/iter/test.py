#!/usr/bin/env python
import asyncio
import logging
import sys
import time

import d1_common.utils.ulog

import d1_client.aio.async_client
import d1_client.aio.iter.objectlist_async

log = logging.getLogger(__name__)
d1_common.utils.ulog.setup(is_debug=True)


async def main():
    # async for x in d1_client.aio.iter.objectlist_async.OO():
    #     print(x)

    c = d1_client.aio.async_client.AsyncDataONEClient(
        "https://gmn.edirepository.org/mn"
    )

    time.sleep(3)

    # o = d1_client.aio.iter.objectlist_async.ObjectListIteratorAsync(c)
    #
    # async for object_info_pyxb in o:
    #     pid = object_info_pyxb.identifier.value()
    #     print('async for: {}'.format(pid))

    # async for x in o:
    #     print( x)

    # async for x in o.qq():
    #     print(x)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
