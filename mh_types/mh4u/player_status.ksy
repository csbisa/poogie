meta:
  id: player_status
  endian: le
seq:
  - id: unknown1
    size: 24
  - id: current_health
    type: u2
    doc: Current health for the player.
  - id: max_health
    type: u2
    doc: Maximum health for the player.
  - id: unknown2
    size: 5
  - id: status
    type: u1
    doc: |
      * 0x2 - Cold Drink
  - id: unknown3
    size: 24
  - id: zone
    type: u1
    doc: Current zone the player is in.
  - id: unknown4
    size: 5
