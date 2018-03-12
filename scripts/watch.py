#!/usr/bin/python

# Uses MHPacketProcessor to dump info from a pcap file to aid in debugging and
# parsing.
#
#  ./watch.py
# Dumps top-level block info
#
#  ./watch.py <id>
# Dumps the payload for the provided ID (i.e. 0x101)
#
#  ./watch.py <id> <name>
# Dumps the parsed payload for the provided ID and class name (i.e. player_movement)

import binascii
import importlib
from mh_types.generated.mh4u_remote_packet import Mh4uRemotePacket
from mh_types.generated.mh4u_data import Mh4uData
from poogie.process import MHPacketProcessor
from scapy.layers.inet import IP
from scapy.utils import PcapReader
import sys

def get_vars(obj):
    return { k:v for k,v in vars(obj).items() if not k.startswith('_') }

# typepkg is e.g. monster_status
# which would return the MonsterStatus class
def get_type(typepkg):
    modulename = "mh_types.generated.mh4u." + typepkg
    module = importlib.import_module(modulename)
    classname = ''.join([n[0].upper() + n[1:] for n in typepkg.split('_')])
    return getattr(module, classname)

idx = 1
prev_data = None
def display(data, typeclass):
    global idx
    global gs
    idx += 1
    # Lower layer currently doesn't deal with duplicate blocks, so this
    # works around it by ignoring duplicate sequential blocks.
    global prev_data
    if prev_data is None:
        prev_data = data
    else:
        if prev_data == data:
            return
        prev_data = data

    print("Block", idx)

    if typeclass is None:
        d = {'unknown': data}
    else:
        func = getattr(typeclass, 'from_bytes')
        d = get_vars(func(data))

    for k, v in d.items():
        if isinstance(v, bytes):
            for row in [v[i:i+32] for i in range(0, len(v), 32)]:
                print(k, str(binascii.hexlify(row)))
        elif isinstance(v, list):
            fmt = " {:3d}" * len(v)
            print(k + fmt.format(*v))
        else:
            print(k, v)

pcap_file = sys.argv[1]
if len(sys.argv) > 2:
    typeid = int(sys.argv[2], 16)
else:
    typeid = None
if len(sys.argv) > 3:
    typeclass = get_type(sys.argv[3])
else:
    typeclass = None

def process_packet(block, time):
    if block.type == typeid and block.length != 0xff:
        display(block.data, typeclass)

def dump_packet(block, time, rawpkt=None):
    print('\t'.join([rawpkt[IP].src, hex(block.type), hex(block.unknown2),
                     hex(block.unknown1), str(block.length)]))

if typeid is not None:
    mhp = MHPacketProcessor(process_packet)
    callback = mhp.process
else:
    mhp = MHPacketProcessor(dump_packet)
    callback = lambda x: mhp.process(x, verbose=True, rawpkt=x)

for pkt in PcapReader(pcap_file):
    callback(pkt)
