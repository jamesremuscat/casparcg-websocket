from collections import namedtuple
from dotenv import load_dotenv
from twisted.internet import reactor
from twisted.python import log

from .websocket import ServerFactory

import os
import sys


Config = namedtuple('Config', ['casparcg_host', 'casparcg_port', 'osc_port'])


def main():
    log.startLogging(sys.stdout)
    load_dotenv()

    # Connecting to the CasparCG server:
    casparcg_host = os.environ.get('CASPARCG_HOST', None)
    casparcg_port = os.environ.get('CASPARCG_PORT', 5250)
    osc_port = os.environ.get('OSC_PORT', 6250)

    config = Config(casparcg_host, casparcg_port, osc_port)

    # Connections from web apps
    websocket_port = os.environ.get('WEBSOCKET_PORT', 8080)

    if casparcg_host is None:
        raise RuntimeError('No CASPARCG_HOST specified!')

    ws_server_factory = ServerFactory(config)

    reactor.listenTCP(websocket_port, ws_server_factory)

    reactor.run()
