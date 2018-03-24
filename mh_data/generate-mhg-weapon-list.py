#!/usr/bin/python

#unpacked/romfs/eng/arc/resident_eng/eng/table/weapon02MsgData_eng.gmd

# format is:
# - singular string, ignore
# - list of 4 items
#   - name (1)
#   - description (1)
#   - max lvl name (1)
#   - max lvl description (1)

# weapon mappings:
weapon_map = {
0: 'gs',
1: 'sns',
2: 'hammer',
3: 'lance',
4: 'hbg',
6: 'lbg',
7: 'ls',
8: 'sa',
9: 'gl',
10: 'bow',
11: 'db',
12: 'hh',
13: 'ig',
14: 'cb',
}

print "mhg_weapons = {"
for weapon_type in weapon_map.keys():
    filename = 'unpacked/romfs/eng/arc/resident_eng/eng/table/weapon{:02d}MsgData_eng.gmd'.format(weapon_type)
    with open(filename, 'r') as f:
        data = f.read()
    strings = data[40:].split('\x00')[1:]
    print(str(weapon_type) + ": {")
    for i in range(0, len(strings)-1, 4):
        print str(i/4) + ": \"" + strings[i].replace('"', '\\"') + "\","
    print("},")
print("}")
