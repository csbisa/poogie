meta:
  id: player_info
  endian: le
seq:
  - id: unknown1
    size: 24
  - id: weapon_class
    type: u2
    enum: weapon_class
  - id: weapon
    type: u2
  - id: unknown2
    size: 26
  - id: body_gear
    type: u2
  - id: unknown3
    size: 26
  - id: arm_gear
    type: u2
  - id: unknown4
    size: 26
  - id: leg_gear
    type: u2
  - id: unknown5
    size: 26
  - id: foot_gear
    type: u2
  - id: unknown6
    size: 26
  - id: head_gear
    type: u2
  - id: unknown7
    size: 20
enums:
  weapon_class:
    7: greatsword
    9: hammer
    18: huntinghorn
    19: insectglaive
    20: chargeaxe

# some weapon keys
#  92 - worn great sword
#  78 - vulcanis
#  168 - cera cymmetry
#  215 - fatalis iregard
#  162 - demonlord hammer
#  118 - dancing grisdrum
#  122 - hellruin glaive omen
#  70 - ceadeus regalia

# some head keys
#  881 - craftsmans specs
#  338 - ukanlos mask
#  882 - felyne hairband x
