"""aenumerate - enumerate for async for"""

import asyncio
from collections import abc


class aenumerate(abc.AsyncIterator):
    """enumerate for async for"""
    def __init__(self, aiterable, start=0):
        self._aiterable = aiterable
        self._i = start - 1

    async def __aiter__(self):
        self._ait = await self._aiterable.__aiter__()
        return self

    async def __anext__(self):
        # self._ait will raise the apropriate AsyncStopIteration
        val = await self._ait.__anext__()
        self._i += 1
        return self._i, val


# Example usage
async def iter_lines(host, port):
    """Iterator over lines from host:port, print them with line number"""
    rdr, wtr = await asyncio.open_connection(host, port)
    async for lnum, line in aenumerate(rdr, 1):
        line = line.decode().rstrip()
        print('[{}:{}] {:02d} {}'.format(host, port, lnum, line))


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description='enumerate lines from TCP server')
    parser.add_argument('host', help='host to connect to')
    parser.add_argument('port', help='port to connect to', type=int)
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(iter_lines(args.host, args.port))
    loop.close()

# Run server: nc -lc -p 7654 < some-file
# (or on osx: nc -l 7654 < some-file)
