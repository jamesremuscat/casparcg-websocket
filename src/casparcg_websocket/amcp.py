from twisted.internet.protocol import Protocol, ReconnectingClientFactory


class AMCPClientProtocol(Protocol):
    def connectionMade(self):
        print('AMCP connection made')
        self.factory.websocket.amcp = self

    def sendMessage(self, message):
        self.transport.write(
            "{}\r\n".format(
                message.decode('utf-8')
            ).encode('utf-8')
        )

    def dataReceived(self, data):
        self.factory.websocket.onAMCPMessage(data)


class AMCPClientFactory(ReconnectingClientFactory):
    def __init__(self, websocket):
        self.websocket = websocket

    def buildProtocol(self, addr):
        self.resetDelay()
        protocol = AMCPClientProtocol()
        protocol.factory = self
        return protocol
