meta:
  id: player_equipment
  endian: be
seq:
  - id: unknown1
    size: 4
  - id: weapon_type
    type: u1
  - id: unknown2
    size: 52
  - id: hunter_name
    type: str
    encoding: UTF-8
    size: 10 # TODO This isn't right, not sure what the max length is.
  - id: unknown3
    size: 299
  - id: weapon_id
    type: u2
  - id: weapon_lvl
    type: u1
  - id: unknown4
    size: 33
  - id: head_id
    type: u2
  - id: head_lvl
    type: u1
  - id: unknown5
    size: 33
  - id: body_id
    type: u2
  - id: body_lvl
    type: u1
  - id: unknown6
    size: 33
  - id: arm_id
    type: u2
  - id: arm_lvl
    type: u1
  - id: unknown7
    size: 33
  - id: waist_id
    type: u2
  - id: waist_lvl
    type: u1
  - id: unknown8
    size: 33
  - id: legs_id
    type: u2
  - id: legs_lvl
    type: u1
  - id: unknown9
    size: 68
  - id: attack
    type: u2
  - id: defense
    type: u2
enums:
  weapon_type:
    0: greatsword
    2: hammer
    3: lance
    12: huntinghorn
