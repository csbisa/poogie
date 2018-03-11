meta:
  id: guild_card
  endian: le
types:
  guildcard:
    seq:
      - id: unknown1
        size: 18
      - id: name
        type: str
        size: 24
        encoding: UTF-16
      - id: unknown2
        type: u2
      - id: hr
        type: u2
      - id: name2
        type: str
        size: 24
        encoding: UTF-16
      - id: caravan_low_quests
        doc: Low-rank Caravan quests completed.
        type: u2
      - id: ghall_low_quests
        doc: Low-rank Guild Hall quests completed.
        type: u2
      - id: ghall_high_quests
        doc: High-rank Guild Hall quests completed.
        type: u2
      - id: guild_quests
        doc: Guild Quest quests completed.
        type: u2
      - id: arena_quests
        doc: Arena quests completed.
        type: u2
      - id: caravan_high_quests
        doc: High-rank Caravan quests completed.
        type: u2
      - id: grank_quests
        doc: G-Rank quests completed.
        type: u2
      - id: unknown3
        size: 0x68
  guildcard2:
    seq:
      - id: unknown
        size: 104
      - id: greeting
        type: str
        size: 88
        encoding: UTF-16
        doc: Greeting for the guild card.
