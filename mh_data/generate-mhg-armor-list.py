#!/usr/bin/python

#unpacked/romfs/eng/arc/resident_eng/eng/table/armorSeriesData_eng.gmd

# format is:
# - singular string, ignore
# - list of 10 items
#   - names (5), in order-- partial armor sets have (None) in unused slots
#   - description (5)

# weapon mappings:
armor_ordering = ['head', 'body', 'arm', 'waist', 'legs']

filename = 'unpacked/romfs/eng/arc/resident_eng/eng/table/armorSeriesData_eng.gmd'
with open(filename, 'r') as f:
    data = f.read()
strings = data[40:].split('\x00')[1:]

# stride every 10 elements, with 0-4 base
for armor_type in range(len(armor_ordering)):
    print("mhg_" + armor_ordering[armor_type] + "_armor_list = {")
    for i in range(armor_type, len(strings)-1, 10):
        print str(i//10) + ": \"" + strings[i]  + "\","
    print("}")
    print("")
