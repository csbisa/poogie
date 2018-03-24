from collections import namedtuple
from poogie.process import MHPacketProcessor
from poogie.quest import QuestProcessor
from scapy.layers.inet import IP
from scapy.utils import PcapReader

# TODO Gonna need a better way to do this...
from mh_types.generated.mhg.faint_event import FaintEvent
from mh_types.generated.mhg.monster_status import MonsterStatus
from mh_types.generated.mhg.player_equipment import PlayerEquipment
from mh_types.generated.mhg.player_status import PlayerStatus

quest_headers = [ 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xd, 0xe, 0xf,
                  0x12, 0x13, 0x15, 0x16, 0x17, 0x19, 0x1d ]

class Poogie():
    """Monster Hunter packet processor

    Collect events from a capture (processed via process_pcap_file) which can
    then be analyzed

    This class should not be used directly, use one of the game-based subclasses
    such as MHGenPoogie instead.
    """
    Event = namedtuple('Event', ['time', 'type', 'instance', 'ip'])

    def __init__(self):
        self.mhp = MHPacketProcessor(self.process_block)
        self.qp = QuestProcessor()
        self.events = []
        self.skipped = {}
        self.failed_parses = {}

    def process_block(self, data, flags, time, rawpkt=None):
        # Check flags first
        if flags & 0x2:
            # Health check packet, nothing interesting
            return

        # Now dispatch based on the first byte in the data
        if data[0] == 0 and len(data) >= 4:
            t = int.from_bytes(data[2:4], byteorder='little')
            c = self.types.get(t)
            if c is None:
                self.skipped[t] = self.skipped.get(t, 0) + 1
                return
            else:
                parser = getattr(c, 'from_bytes')
                try:
                    parsed = parser(data[4:])
                except:
                    self.failed_parses[t] = self.failed_parses.get(t, 0) + 1
                    return
                self.events.append(self.Event(time, c.__name__, parsed, rawpkt[IP].src))
        elif data[0] in quest_headers:
            self.qp.process_packet(data, flags, time, rawpkt)

    def get_events(self):
        """Get events collected by this poogie instance.

        Returns an array of named tuples of the format:
          (time, type, instance, ip)
        where:
          time - Absolute time of event
          type - Name of the mh_type for the event
          instance - An instance of type for the event
          ip - IP address of the sender for the event
        """
        return self.events

    def process_pcap_file(self, filename):
        """Processes a pcap file
        """
        for pkt in PcapReader(filename):
            self.mhp.process(pkt, rawpkt=pkt)
        stats = self.mhp.get_stats()
        print("Processed", stats['packets'], "packets")

class MHGenPoogie(Poogie):
    """Poogie for Monster Hunter Generations
    """

    types = {
        0x0e04: MonsterStatus,
        0x2504: FaintEvent,
        0xee03: PlayerStatus,
        0xf603: PlayerEquipment,
    }
