#!/usr/bin/python

# Uses poogie to dump quest information from a pcap file. Only works with MHGen.
#
#  ./get-quests.py <pcap file>
#
# Most of this will get moved into poogie itself at some point.

from poogie.poogie import MHGenPoogie
import sys
from datetime import timedelta
from mh_data.mhg_quests import mhg_quests
import matplotlib.pyplot as plt
from mh_data.mhg_armor import mhg_head_armor_list, mhg_body_armor_list, mhg_arm_armor_list, mhg_waist_armor_list, mhg_legs_armor_list
from mh_data.mhg_weapons import mhg_weapons

def get_weapon_name(weapon_type, weapon_id):
    return mhg_weapons[weapon_type][weapon_id]

def get_armor_name(armor_type, armor_id):
    if armor_type == 0:
        return mhg_head_armor_list[armor_id]
    elif armor_type == 1:
        return mhg_body_armor_list[armor_id]
    elif armor_type == 2:
        return mhg_arm_armor_list[armor_id]
    elif armor_type == 3:
        return mhg_waist_armor_list[armor_id]
    elif armor_type == 4:
        return mhg_legs_armor_list[armor_id]

def count_faints(events, player):
    faints = [e for e in events if e.type == 'FaintEvent' and e.ip == player and e.instance.req == 0]
    faint_count = 0
    last_faint_time = 0
    # there's no aggregation for the sender, so do some basic
    # duplication checking to make sure only one faint event
    # is tracked for the sender
    for f in faints:
        if abs(f.time - last_faint_time) <= 5:
            continue
        last_faint_time = f.time
        faint_count += 1
    return faint_count

# TODO damage taken doesnt account for faints since player status never reports 0 health
def count_damage_taken(events, player):
    health = [e.instance for e in events if e.type == 'PlayerStatus' and e.ip == player]
    return -sum([v for v in [b.cur_health-a.cur_health for a,b in zip(health, health[1:])] if v < 0])

pcap_file = sys.argv[1]

poogie = MHGenPoogie()
poogie.process_pcap_file(pcap_file)

events = poogie.get_events()
for q in poogie.qp.get_quests():
    if not q.started:
        continue
    print("Quest:", mhg_quests.get(str(q.quest_id), 'unknown'))
    print("Quest length:", str(timedelta(seconds=int(q.end_time - q.quest_start_time))))
    quest_packets = [e for e in events
                     if e.time >= q.quest_start_time and e.time < q.end_time]

    # Only quest participants send PlayerStatus packets.
    participant_ips = set([e.ip for e in quest_packets if e.type == 'PlayerStatus'])
    print("Hunters:")
    for p in participant_ips:
        # Find last equipment packet before quest started
        try:
            equip = next(o.instance for o in reversed([e for e in events if e.type == 'PlayerEquipment'])
                        if o.time <= q.quest_start_time and o.ip == p)

            print("", equip.hunter_name.rstrip('\0'))
            print("   Equipment:", " / ".join([get_weapon_name(equip.weapon_type, equip.weapon_id),
                                              get_armor_name(0, equip.head_id),
                                              get_armor_name(1, equip.body_id),
                                              get_armor_name(2, equip.arm_id),
                                              get_armor_name(3, equip.waist_id),
                                              get_armor_name(4, equip.legs_id)]))
        except:
            print(" Failed to get hunter info for", p)
        print("   Damage taken:", count_damage_taken(quest_packets, p))
        print("   Faints:", count_faints(quest_packets, p))

    health = [(e.instance.id, e.instance.health, e.time - q.quest_start_time) for e in quest_packets
              if e.type == 'MonsterStatus']
    monster_ids = set([d[0] for d in health])
    for i in monster_ids:
        datapoints = list(zip(*[d[1:] for d in health if d[0] == i]))
        plt.plot(list(datapoints[1]), list(datapoints[0]))
    plt.title('Monster Health')
    plt.xlabel('Quest Time')
    plt.xlim(0)
    plt.ylabel('HP')
    plt.ylim(0)
    # TODO Find the actual monster name
    intruder_ids = [d for d in monster_ids if d >= 62]
    monster_ids = [d for d in monster_ids if d < 62]
    plt.legend(['Monster '+chr(ord('A')+i) for i in range(len(monster_ids))] +
               ['Intruder '+chr(ord('A')+i) for i in range(len(intruder_ids))])

    figname = "/tmp/monster-quest-health-" + hex(q.id) + ".png"
    plt.savefig(figname)
    print("Monster health graph at", figname)
    plt.close()

    print("")
