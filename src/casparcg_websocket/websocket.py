from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from twisted.internet import reactor
from .amcp import AMCPClientFactory
from .osc import OSCReceiverProtocol

import ujson


class DirDict(object):
    def __init__(self):
        self._dict = {}

    def __setitem__(self, path_string, value):
        path = path_string.split('/')

        container = self._dict
        while len(path) > 1:
            next_elem_name, path = path[0], path[1:]
            container = container.setdefault(next_elem_name, {})
        container[path[0]] = value

    def __getitem__(self, path_string):
        path = path_string.split('/')

        container = self._dict
        while len(path) > 1:
            next_elem_name, path = path[0], path[1:]
            if next_elem_name not in container:
                raise IndexError(next_elem_name)
            container = self._dict[next_elem_name]

        return container[path[0]]

    def __repr__(self):
        return str(self._dict)

    def for_json(self):
        return self._dict


def map_osc_to_dict(osc):
    retval = DirDict()

    for m in osc.messages:
        path = m.message.address[1:]
        retval[path] = m.message.params

    return retval


class ServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        super().__init__()
        self._amcp_factory = AMCPClientFactory(self)

    def connectionMade(self):
        super().connectionMade()
        self._caspar_connection = reactor.connectTCP(
            self.factory.config.casparcg_host,
            self.factory.config.casparcg_port,
            self._amcp_factory
        )

        self._osc_connection = reactor.listenUDP(
            self.factory.config.osc_port,
            OSCReceiverProtocol(self.onOSCMessage)
        )

    def connectionLost(self, reason):
        if hasattr(self, '_caspar_connection'):
            self._caspar_connection.disconnect()
            self._amcp_factory.stopTrying()

        if hasattr(self, '_osc_connection'):
            self._osc_connection.stopListening()

    def onMessage(self, payload, isBinary):
        if hasattr(self, 'amcp'):
            if self.amcp:
                self.amcp.sendMessage(payload)

    def onAMCPMessage(self, message):
        self.sendMessage(
            ujson.dumps({
                'amcp': message.decode('utf-8').strip()
            }).encode('utf-8')
        )

    def onOSCMessage(self, message):
        state = map_osc_to_dict(message)
        self.sendMessage(
            ujson.dumps(
                {'state': state.for_json()}
            ).encode('utf-8')
        )


class ServerFactory(WebSocketServerFactory):

    protocol = ServerProtocol

    def __init__(self, config):
        super().__init__()
        self.config = config
