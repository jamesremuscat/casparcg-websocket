from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from twisted.internet import reactor
from .amcp import AMCPClientFactory

import json


class ServerProtocol(WebSocketServerProtocol):

    def connectionMade(self):
        super().connectionMade()
        reactor.connectTCP(
            self.factory.config.casparcg_host,
            self.factory.config.casparcg_port,
            AMCPClientFactory(self)
        )

    def onMessage(self, payload, isBinary):
        if hasattr(self, 'amcp'):
            if self.amcp:
                self.amcp.sendMessage(payload)

    def onAMCPMessage(self, message):
        self.sendMessage(
            json.dumps({
                'amcp': message.decode('utf-8').strip()
            }).encode('utf-8')
        )


class ServerFactory(WebSocketServerFactory):

    protocol = ServerProtocol

    def __init__(self, config):
        super().__init__()
        self.config = config
