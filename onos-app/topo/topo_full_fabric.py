#!/usr/bin/python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from bmv2 import ONOSBmv2Switch, P4Host
setLogLevel('info')

net = Mininet(switch=ONOSBmv2Switch)

# HOSTS
info('*** Adding hosts\n')
h1 = net.addHost('h1', cls=P4Host, ip='10.0.0.1/24', mac="00:00:00:00:00:01",
                 gateway='10.0.0.254')
h2 = net.addHost('h2', cls=P4Host, ip='10.0.0.2/24', mac="00:00:00:00:00:02",
                 gateway='10.0.0.254')
h10 = net.addHost('h10', cls=P4Host, ip='10.10.10.1/24', mac="00:00:00:00:00:10",
                  gateway='10.10.10.254')

# SWITCHES
info('*** Adding switches\n')
# Leaf
s11 = net.addSwitch(name='s11', loglevel='info', pktdump=False)
s12 = net.addSwitch(name='s12', loglevel='debug', pktdump=False)

# Spine
s21 = net.addSwitch(name='s21', loglevel='debug', pktdump=False)
s22 = net.addSwitch(name='s22', loglevel='debug', pktdump=False)

# LINKS
info('*** Creating links\n')
net.addLink(h1, s11)
net.addLink(h2, s11)
net.addLink(h10, s12)

net.addLink(s11,s21)
net.addLink(s11,s22)

net.addLink(s12,s21)
net.addLink(s12,s22)



info('*** Starting network\n')

net.start()
h1.cmd("ip route add default via 10.0.0.254")
h2.cmd("ip route add default via 10.0.0.254")
h10.cmd("ip route add default via 10.10.10.254")
# ARP managed via ARP Proxy in ONOS
#info('*** Static ARP\n')
#net.staticArp()

info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()