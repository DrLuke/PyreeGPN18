import socket
import threading


__author__ = 'adrian'



class ArtNetReceiver(threading.Thread):
    def __init__(self, universe):
        threading.Thread.__init__(self)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", 6454))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock = sock
        self.clb = None
        self.universe = universe
        self.inp = [0] * 512
        self.start()


    def new_data(self, data):
        for n in range(0, min(len(data), 512)):
            if data[n] != self.inp[n]:
                if self.clb is not None:
                    self.clb(n, data[n])
                self.inp[n] = data[n]
    def run(self):
        self.artnetReceiver()

    def artnetReceiver(self):
        while 1:
            data, addr = self.sock.recvfrom(1024)
            if data.startswith("Art-Net\x00\x00\x50\x00\x0e".encode()) and len(data) > 20:
                universe =data[14] + (data[15] << 8)
                if universe != self.universe:
                    continue
                length = (data[16] << 8) +data[17]
                dmx = data[18:18 + length]
                dmx = [n / 255.0 for n in dmx]
                self.new_data(dmx)


#def my_clb(channel, value):
#    print(channel, value)

#a = ArtNetReceiver(8)
#a.clb = my_clb

