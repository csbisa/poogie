#from mh_data.mhg_quests import mhg_quests
from mh_types.generated.mhg.monster_status import MonsterStatus
from mh_types.generated.mhg.faint_event import FaintEvent
from mh_types.generated.mhg.player_status import PlayerStatus
from mh_types.generated.mhg.player_equipment import PlayerEquipment

# TODO Only confirmed with MHGen, need to check other games.
# Quest packets start with a byte of one of the following:
#  06: quest post
#  07: quest cancel
#  08: quest start
#  09: quest start ack
#  0a: quest join notification
#  0b: quest join ack
#  0d: broadcast of quest join
#  0e: quest quit notification
#  0f: quest quit ack
#  12: ready notification
#  13: ready ack
#  15: broadcast of quest ready
#  16: cancel ready notification
#  17: cancel ready ack
#  19: broadcast of cancel ready
#  1d: broadcast of quest quit (complete, abandon, or whatever)
# N.B. 'broadcast' sends it to everyone except the initiator, i.e.
# A hosts quest, B joins quest, C/D present
# B sends 0a, A sends 0b to B and 0d to C and D

quest_headers = [ 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xd, 0xe, 0xf,
                  0x12, 0x13, 0x15, 0x16, 0x17, 0x19, 0x1d ]

class Quest():
    """Per-quest metadata
    """
    def __init__(self, identifier):
        self.id = identifier
        self.start_time = 0
        self.quest_start_time = 0
        self.end_time = 0
        self.pkts = 0
        self.started = False
        self.quest_id = 0

    def process_meta_packet(self, header, data, time):
        if self.start_time == 0:
            self.start_time = time

        if time < self.start_time:
            self.start_time = time
        if time > self.end_time:
            self.end_time = time

        if header == 0x6:
            self.quest_id = int.from_bytes(data[13:17], byteorder='little')
            #print("Found quest ID", self.quest_id, "name", mhg_quests.get(str(self.quest_id), 'unknown'))
        elif header == 0x8:
            self.quest_start_time = time
            self.started = True

        self.pkts += 1

class QuestProcessor():
    """Handles quest packets in order to aggregate quest information
    """
    def __init__(self):
        self.quests = {}

    def process_packet(self, data, flags, time, rawpkt=None):
        header = data[0]
        if header not in quest_headers:
            return
        # health check packets use 0x12, skip those
        if flags & 0x2:
            return

        # special handling for 0x8
        if header == 0x08:
            identifier = int.from_bytes(data[5:8], byteorder='big')
            #print("Found quest start for id", hex(identifier))
        else:
            identifier = int.from_bytes(data[1:4], byteorder='big')

        # all quests (stared or otherwise) are initiated with this
        if header == 0x06:
            if self.quests.get(identifier) is None:
                #print("Added quest with id", hex(identifier))
                self.quests[identifier] = Quest(identifier)

        q = self.quests.get(identifier)
        if q is None:
            print("Saw packet with unknown quest identifier", hex(identifier))
            return
        q.process_meta_packet(header, data, time)
        self.current_quest = q

    def get_quests(self):
        return self.quests.values()
