#!/usr/bin/python

import argparse
import binascii
import importlib
from poogie.process import MHPacketProcessor
from scapy.layers.inet import IP
from scapy.utils import PcapReader
import struct
import sys

def get_vars(obj):
    return { k:v for k,v in vars(obj).items() if not k.startswith('_') }

# typepkg is e.g. monster_status
# which would return the MonsterStatus class
def get_type(game, typepkg):
    modulename = "mh_types.generated." + game + "." + typepkg
    module = importlib.import_module(modulename)
    classname = ''.join([n[0].upper() + n[1:] for n in typepkg.split('_')])
    return getattr(module, classname)

idx = 0
prev_data = None
def display(data, typeclass, time, rawpkt):
    global idx
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

    print("Block", idx, time, rawpkt[IP].src, "->", rawpkt[IP].dst, len(data))

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

def process_packet(data, flags, time, rawpkt=None, typeid=None, typeclass=None):
    if len(data) < 4:
        return
    (unknown2, datatype) = struct.unpack('HH', data[0:4])
    if datatype == typeid:
        display(data[4:], typeclass, time, rawpkt)

def dump_packet(data, flags, time, rawpkt=None):
    if len(data) >= 4:
        (unknown2, datatype) = struct.unpack('HH', data[0:4])
    else:
        print('Skipping short block of length', len(data), 'with flags', hex(flags))
        return
    print('\t'.join(["%.3f" % time, rawpkt[IP].src + "->" + rawpkt[IP].dst,
                     hex(datatype), hex(unknown2),
                     hex(flags), str(len(data))]))

parser = argparse.ArgumentParser(description="Uses MHPacketProcessor to dump info from a pcap file to aid in debugging and parsing.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="""
Examples:

 watch.py <pcap_file>
Dumps top-level block info

 watch.py --id <id> <pcap_file>
Dumps the payload for the provided ID (i.e. 0x101)

 watch.py --id <id> --type <type> <pcap_file>
Dumps the parsed payload for the provided ID and class name (i.e. player_movement)
""")
parser.add_argument("pcap_file", help="pcap file to parse")
parser.add_argument("--id",
                    help="ID to watch. See doc/types.md for more information",
                    required=False,
                    type=lambda x: int(x, 0))
parser.add_argument("--type",
                    help="Name for the type to parse the data into",
                    required=False)
parser.add_argument("--game",
                    help="Game to use for types (mh4u, mhg, etc.)",
                    default='mh4u')
args = parser.parse_args()

if args.type and not args.id:
    print("--id must be provided with --type")
    sys.exit(1)

typeclass = None
if args.type is not None:
    typeclass = get_type(args.game, args.type)

if args.id is not None:
    mhp = MHPacketProcessor(process_packet)
    callback = lambda x: mhp.process(x, verbose=False, rawpkt=x, typeid=args.id, typeclass=typeclass)
else:
    mhp = MHPacketProcessor(dump_packet)
    callback = lambda x: mhp.process(x, verbose=False, rawpkt=x)

for pkt in PcapReader(args.pcap_file):
    callback(pkt)

print(mhp.get_stats())
