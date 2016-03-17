__author__ = 'tardis'
# import netifaces
import re
from ootclient.utils import patch_subprocess
import random
from netaddr import IPAddress, IPNetwork


class Server():
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        ifs = self.get_ifaces()
        master_mac = self._get_master_mac(kwargs.get('master_cidr'), ifs)

        def _get_name():
            return master_mac.replace(':', '')

        return {'name': _get_name(), 'interfaces': ifs,
                'master_mac': master_mac}

    def _get_master_mac(self, master_cidr, interfaces):
        ipn = IPNetwork(master_cidr)
        for k, v in interfaces.items():
            ip = v.get('ip')
            if ip:
                if IPAddress(ip) in ipn:
                    return v.get('mac')

    # def get_ifaces_bynetifaces(self):
    # ifaces = {}
    # for i in netifaces.interfaces():
    # addrs = netifaces.ifaddresses(i)
    # iface = {'inet': addrs.get(netifaces.AF_INET)}
    # iface['mac'] = addrs.get(netifaces.AF_LINK)
    # ifaces[i] = iface
    # return json.dumps(ifaces)

    def __str__(self):
        return {'interfaces': self.get_ifaces()}

    def get_ifaces(self):
        subprocess = patch_subprocess()
        output = subprocess.check_output(['bash', '-c', 'ls /sys/class/net'])
        ifnames = set(output.split('\n'))
        ifnames = filter(lambda x: x and x != 'lo', ifnames)
        ifaces = {}
        for i in ifnames:
            ifaces[i] = self._get_iface(i)

        return ifaces

    # TODO need test
    def _get_iface(self, ifname):
        iface = {}
        subprocess = patch_subprocess()
        output = subprocess.check_output(['bash', '-c', 'ip a show %s' % ifname])
        m = re.search(r'(?<=link/ether).*(?=brd)', output)
        if m:
            iface['mac'] = m.group().replace(' ', '')
        m = re.search(r'(?<=inet).*(?=/\d{2} *brd)', output)
        if m:
            iface['ip'] = m.group().replace(' ', '')

        return iface




