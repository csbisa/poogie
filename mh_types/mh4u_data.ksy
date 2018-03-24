meta:
  id: mh4u_data
  endian: le
seq:
  - id: ignore
    size: 2
    doc: Leading two bytes used for decoding.
  - id: random
    size: 2
  - id: blocks
    type: block
    repeat: eos
types:
  block:
    seq:
      - id: flags
        type: u2
        doc: |
          * 0x40: Indicates that the actual block size is the length plus 128.
      - id: length
        type: u2
      - id: seqnum
        type: u4be
      - id: random
        size: 8
      - id: data
        size: actual_length
        type: subblockhdr
    instances:
      actual_length:
        value: (((flags & 0x40) >> 6) * 0x100) + length
  subblockhdr:
    seq:
    - id: seq1
      type: u2be
    - id: seq2
      type: u2be
    - id: unknown3
      type: u1
    - id: count
      type: u1
    - id: blocks
      type: subblock
      repeat: expr
      repeat-expr: count
  subblock:
    seq:
      - id: flags
        type: u1
        doc: |
          * 0x02: Health check packet
          * 0x10: Empty subblock (accompanied by length of 0xFE or 0xFF).
          * 0x20: Initial transmit. On retransmits, this bit is not set.
          * 0x40: Data spans multiple subblocks.
      - id: length_spec
        type: u1
        doc: Specifies the length of the data. If this value is 0xFE or 0xFF,
             the length of the data is 4.
      - id: data
        size: length
    instances:
      length:
        value: '(length_spec & 0xFE) != 0xFE ? length_spec : 4'
