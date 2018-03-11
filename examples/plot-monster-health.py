#!/usr/bin/python

# Generates monster health graph given a pcap file.
# This script doesn't detect quest boundaries, so you'll get funny results if
# you feed a pcap file that contains multiple quests.
#
#  ./plot-monster-health.py <pcap file>

import matplotlib.pyplot as plt
from mh_types.generated.mh4u.monster_status import MonsterStatus
from poogie.process import MHPacketProcessor
from scapy.utils import PcapReader
import sys

pcap_file = sys.argv[1]
health = []

def process_packet(block, time):
    if block.type == 0x105 and block.length != 0xff:
        status = MonsterStatus.from_bytes(block.data)
        health.append([status.id, status.health, time])

mhp = MHPacketProcessor(process_packet)
for pkt in PcapReader(pcap_file):
    mhp.process(pkt)

ids = set([d[0] for d in health])
for i in ids:
    datapoints = list(zip(*[d[1:] for d in health if d[0] == i]))
    plt.plot(list(datapoints[1]), list(datapoints[0]))

plt.title('Monster Health')
plt.xlabel('Quest Time')
plt.xlim(0)
plt.ylabel('HP')
plt.ylim(0)
# TODO Find the actual monster name
plt.legend(['Monster '+chr(ord('A')+i) for i in ids])

plt.show()
