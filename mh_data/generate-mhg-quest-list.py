#!/usr/bin/python

#find unpacked/romfs/loc/arc/quest/ -name '*eng.gmd' -exec ./generate-quest-list.py {} \; | tee quests.txt

import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = f.read()

strings = data[40:].split('\x00')

print "'" + str(int(strings[0].split('_')[1])) + "': \"" + strings[2]  + "\""
