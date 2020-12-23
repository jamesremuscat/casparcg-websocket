from dotenv import load_dotenv

import os


def main():
    load_dotenv()

    # Connecting to the CasparCG server:
    casparcg_host = os.environ.get('CASPARCG_HOST', None)
    casparcg_port = os.environ.get('CASPARCG_PORT', 5250)
    osc_port = os.environ.get('OSC_PORT', 6250)

    # Connections from web apps
    websocket_port = os.environ.get('WEBSOCKET_PORT', 8080)

    if casparcg_host is None:
        raise RuntimeError('No CASPARCG_HOST specified!')

    print('Hello world')
