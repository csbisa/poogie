meta:
  id: monster_status
  endian: le
seq:
  - id: id
    type: u2
    doc: Per-monster identifier.
  - id: unknown1
    type: u1
    doc: Appears to always be zero.
  - id: id2
    type: u1
    doc: Appears to be identical to id
  - id: unknown3
    type: u2
  - id: unknown4
    type: u2
    doc: Appears to be identical to unknown3
  - id: unknown5
    type: u2
    doc: Appears to be the same value as unknown6, 7, 8, 9, 10
  - id: unknown6
    type: u2
  - id: unknown7
    type: u2
  - id: unknown8
    type: u2
  - id: unknown9
    type: u2
  - id: unknown10
    type: u2
  - id: unknown11
    type: u2
  - id: unknown12
    type: u2
  - id: position1
    type: u1
    repeat: expr
    repeat-expr: 12
  - id: unknown13
    type: u2
  - id: unknown14
    type: u2
  - id: unknownarray1
    type: u1
    repeat: expr
    repeat-expr: 16
  - id: unknownarray2
    type: u1
    repeat: expr
    repeat-expr: 16
  - id: unknownarray3
    type: u1
    repeat: expr
    repeat-expr: 12

  - id: health
    type: u4
    doc: Current health of the monster.
  - id: negativeone2
    type: u1
    doc: Seems to always be 0xff
  - id: unknown15
    type: u1

  - id: zone
    type: u1
    doc: Zone the monster is currently in
  - id: unknown15
    type: u1
  - id: negativeone
    type: u2
    doc: Seems to always be 0xffff
  - id: hunger
    type: u2
    doc: Current hunger of the monster. The monster is hungry when this value is zero.
  #- id: unknown2
  #  size: 52
  - id: unknownarray4
    type: u1
    repeat: expr
    repeat-expr: 26
  - id: unknownarray5
    type: u1
    repeat: expr
    repeat-expr: 26
