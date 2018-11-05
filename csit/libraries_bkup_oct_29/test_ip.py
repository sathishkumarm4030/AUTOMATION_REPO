import ipaddress

class BetterIPv4Network(ipaddress.IPv4Network):

    def __add__(self, offset):
        """Add numeric offset to the IP."""
        new_base_addr = int(self.network_address) + offset
        return self.__class__((new_base_addr, str(self.netmask)))

    def size(self):
        """Return network size."""
        start = int(self.network_address)
        return int(self.broadcast_address) + 1 - start


import itertools as it

network = BetterIPv4Network(u'10.1.0.0/16')
network_addrs = (network + (i + 1) * network.size() for i in it.count())

print network_addrs
print next(network_addrs)