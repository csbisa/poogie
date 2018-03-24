meta:
  id: monster_status
  endian: le
seq:
  - id: unknown1
    size: 8
  - id: id
    type: u2be
    doc: |
      Monster identifier for quest, which follows a specific pattern:
      * 0: first monster in a multi-monster quest
      * 1: second monster in a multi-monster quest
      * 10, 20, 30: subsequent monsters
      * 62+: intruder
  - id: unknown2
    type: u2be
  - id: stagger_health
    type: stagger_health
    repeat: expr
    repeat-expr: 8
  - id: unknown3
    size: 16
  - id: health
    type: u4be
  - id: unknown4
    size: 20
  - id: hunger
    type: u2be
  - id: unknown5
    size: 6
  - id: current_zone
    type: u1
  - id: unknown6
    size: 119
types:
  stagger_health:
    seq:
      - id: count
        type: b4
      - id: unknown
        type: b4
      - id: health
        type: u1
