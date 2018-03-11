#!/usr/bin/python

# This script is an example of logging player attacks in realtime.
#
# Only valid for hammer attacks.
#
# You will need to edit the parameters to sniff at the end of this file to
# capture what you're looking for.

from mh_types.generated.player_movement import PlayerMovement
from poogie.process import MHPacketProcessor
from scapy.all import sniff
import sys

hammerattacks = [
    'does a side swing',
    'does a pound',
    'does a pound',
    'does a pound',
    'does a golfswing',
    'unknown',
    'does a unsheathe attack',
    'starts charging',
    'unknown',
    'unknown',
    'unknown',
    'does a level 1 charge',
    'does a uppercut',
    'does a moving level 1 charge',
    'does a uppercut',
    'unknown',
    'does a superpound',
    'unknown',
    'starts a spinning attack',
    'does a spinning finisher',
    'does a spinning early finisher',
    'does an upswing',
    'starts charging',
    'starts charging',
    'unknown',
    'does a pound',
    'does a sideswing',
    'does a pound',
]

prev_data = None
def display(data):
    global prev_data
    if prev_data is None:
        prev_data = data
    else:
        if prev_data == data:
            return
        prev_data = data

    decoded = PlayerMovement.from_bytes(data)
    if decoded.activity == 4:
        action = 'unknown'
        if decoded.action < len(hammerattacks):
            action = hammerattacks[decoded.action]
        if action == 'unknown':
            return
        # TODO Name isn't tracked so we just use 'test.'
        print('test', action)

def process_packet(block, time):
    # 101 is only for the first player, 102/103/104 would be for other players
    if block.type == 0x101 and block.length != 0xff:
        display(block.data)

mhp = MHPacketProcessor(process_packet)

# TODO Make these arguments.
sniff(iface="enp2s0", prn=mhp.process, filter="udp and host 10.0.0.147")
