from twisted.internet import defer, protocol
from pythonosc.osc_packet import OscPacket, ParseError


class OSCReceiverProtocol(protocol.DatagramProtocol):

    def __init__(self, handler):
        """
        @param receiver: L{Receiver} instance.
        """
        self.handler = handler

    def datagramReceived(self, data, sender):
        try:
            packet = OscPacket(data)
            self.handler(packet)
        except ParseError:
            print('Cannot parse: {}'.format(data))
