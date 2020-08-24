import matplotlib.pyplot as plt
import numpy as np
from scapy.all import *
from math import ceil,floor

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

IPsrc = ['10.0.0.1', '10.0.1.200']

timeseries = {}
ts_min = float('inf')
ts_max = 0
scapy_cap = rdpcap('h10_dump.pcap')
for packet in scapy_cap:
	if packet[IP].src in IPsrc:
		if packet[IP].src not in timeseries:
			timeseries[packet[IP].src] = []
		timeseries[packet[IP].src].append([float(packet.time), packet[UDP].len])
		if float(packet.time) > ts_max:
			ts_max = float(packet.time)
		if float(packet.time) < ts_min:
			ts_min = float(packet.time)

# move time horizon 5 seconds back wrt timestamp of the 1st packet
ts_min -= 5
ts_max += 5

def plot(SLOT_SIZE):
	SLOTS_NUM = int(ceil((ts_max-ts_min)/SLOT_SIZE))
	plt.figure(figsize=(3,3))
	for IPsrc in sorted(timeseries.keys()):
		data = [0]*SLOTS_NUM
		for ts, size in timeseries[IPsrc]:
			data[int(floor((ts-ts_min)/SLOT_SIZE))] += (size*8/1e6)/SLOT_SIZE
		plt.plot(data, label='h2' if IPsrc == '10.0.1.200' else 'h1', linestyle='-' if IPsrc == '10.0.1.200' else '-.')
	plt.xlabel('Time [s]')
	plt.ylabel('Rate [Mbps]')
	plt.xlim([0, plt.xlim()[1]])
	plt.ylim([0, plt.ylim()[1]])
	plt.grid(linestyle=':')
	plt.legend(loc='lower center')
	plt.tight_layout()
	plt.show()

plot(1)
#plot(2)
