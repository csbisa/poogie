meta:
  id: guild_card
  endian: be
seq:
  - id: unknown1
    size: 12
  - id: hunter_name_len
    type: u1
  - id: hunter_name
    type: str
    encoding: UTF-16LE
    size: 10 # TODO need max name size
  - id: unknown2
    size: 12
  - id: hunter_rank
    type: u2le
  - id: unknown3
    size: 1983
  - id: village_quests
    type: u2
    doc: Number of Village quests completed.
  - id: hub_low_quests
    type: u2
    doc: Number of Low-Rank Hub quests completed.
  - id: hub_high_quests
    type: u2
    doc: Number of High-Rank Hub quests completed.
  - id: special_permit_quests
    type: u2
    doc: Number of Special Permit quests completed.
  - id: arena_quests
    type: u2
    doc: Number of Arena quests compelted.
  - id: unknown4
    size: 8
  - id: greeting
    type: str
    encoding: UTF-16BE
    size: 54
  - id: unknown5
    size: 15
  - id: village_weapon_usage
    type: weapon_usage
    doc: Weapon usage breakdown for village quests.
  - id: hub_weapon_usage
    type: weapon_usage
    doc: Weapon usage breakdown for hub quests.
  - id: arena_weapon_usage
    type: weapon_usage
    doc: Weapon usage breakdown for arena quests.
  - id: unknown6
    size: 1622
  - id: monster_stats
    type: monster_stats
    repeat: expr
    repeat-expr: 69
types:
  weapon_usage:
    seq:
      - id: gs
        type: u2le
      - id: sns
        type: u2le
      - id: hammer
        type: u2le
      - id: lance
        type: u2le
      - id: hbg
        type: u2le
      - id: lbg
        type: u2le
      - id: ls
        type: u2le
      - id: sa
        type: u2le
      - id: gl
        type: u2le
      - id: bow
        type: u2le
      - id: db
        type: u2le
      - id: hh
        type: u2le
      - id: ig
        type: u2le
      - id: cb
        type: u2le
      - id: otomo
        type: u2le
  monster_stats:
    seq:
      - id: max_length
        type: u1
        doc: |
          Mapping of monster length to actual value. Varies by monster.
          * 90: small size
          * 100: base size
          * 115: big size
          * 123: king size
      - id: min_length
        type: u2
      - id: kill_count
        type: u2
      - id: capture_count_and_unknown3
        type: u2le
      - id: unknown4
        type: u1
    instances:
      capture_count:
        value: (capture_count_and_unknown3 & 0xFFC0) >> 6
      unknown3:
        value: (capture_count_and_unknown3 & 0x3F)
