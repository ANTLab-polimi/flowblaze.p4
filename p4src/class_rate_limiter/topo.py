#!/usr/bin/python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from bmv2 import ONOSBmv2Switch, P4Host
setLogLevel('info')

net = Mininet(switch=ONOSBmv2Switch)

# HOSTS
info('*** Adding hosts\n')
h1 = net.addHost('h1', cls=P4Host, ip='10.0.0.1/8', mac="00:00:00:00:00:01")
h2 = net.addHost('h2', cls=P4Host, ip='10.0.1.1/8', mac="00:00:00:00:00:02")
h10 = net.addHost('h10', cls=P4Host, ip='10.10.10.1/8', mac="00:00:00:00:00:10")

# SWITCHES
info('*** Adding switches\n')
s1 = net.addSwitch(name='s1', loglevel='debug', json="/class_rate_limiter/p4build/bmv2.json", pktdump=False)

# LINKS
info('*** Creating links\n')
net.addLink(h1, s1)
net.addLink(h2, s1)
net.addLink(h10, s1)

info('*** Starting network\n')

net.start()
info('*** Static ARP\n')
net.staticArp()

info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()