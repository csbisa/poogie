#!/usr/bin/python

# Uses MHPacketProcessor to dump info in real time to aid in debugging and
# parsing.
#
#  ./watch-live.py
# Dumps top-level block info
#
#  ./watch-live.py <id>
# Dumps the payload for the provided ID (i.e. 0x101)
#
#  ./watch-live.py <id> <name>
# Dumps the parsed payload for the provided ID and class name (i.e. player_movement)
#
# You will need to edit the parameters to sniff at the end of this file to
# capture what you're looking for.

import binascii
import importlib
from mh_types.generated.mh4u_remote_packet import Mh4uRemotePacket
from mh_types.generated.mh4u_data import Mh4uData
from poogie.process import MHPacketProcessor
from scapy.layers.inet import IP
from scapy.sendrecv import sniff
import sys

# Set this to False if you don't want the screen to be cleared for every
# update.
clearscreen = True

def get_vars(obj):
    return { k:v for k,v in vars(obj).items() if not k.startswith('_') }

# typepkg is e.g. monster_status
# which would return the MonsterStatus class
def get_type(typepkg):
    modulename = "mh_types.generated." + typepkg
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

    if clearscreen:
        print("\x1b[2J")
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

if len(sys.argv) > 1:
    typeid = int(sys.argv[1], 16)
else:
    typeid = None
if len(sys.argv) > 2:
    typeclass = get_type(sys.argv[2])
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

# TODO Make these arguments.
sniff(iface="enp2s0", prn=callback, filter="udp and host 10.0.0.147")
