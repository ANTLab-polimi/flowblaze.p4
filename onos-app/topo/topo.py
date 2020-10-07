#!/usr/bin/python

# Copyright 2020 Daniele Moro <daniele.moro@polimi.it>
#                Davide Sanvito <davide.sanvito@neclab.eu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from bmv2 import ONOSBmv2Switch, P4Host
setLogLevel('info')

net = Mininet(switch=ONOSBmv2Switch)

# HOSTS
info('*** Adding hosts\n')
h1 = net.addHost('h1', cls=P4Host, ip='10.0.0.1/24', mac="00:00:00:00:00:01")
h2 = net.addHost('h2', cls=P4Host, ip='10.0.1.1/24', mac="00:00:00:00:00:02")
h10 = net.addHost('h10', cls=P4Host, ip='10.10.10.1/24', mac="00:00:00:00:00:10")

# SWITCHES
info('*** Adding switches\n')
s1 = net.addSwitch(name='s1', loglevel='debug', pktdump=False)

# LINKS
info('*** Creating links\n')
net.addLink(h1, s1)
net.addLink(h2, s1)
net.addLink(h10, s1)

info('*** Starting network\n')

net.start()
h1.cmd("ip route add default via 10.0.0.254")
h2.cmd("ip route add default via 10.0.1.254")
h10.cmd("ip route add default via 10.10.10.254")
# ARP managed via ARP Proxy in ONOS

info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()