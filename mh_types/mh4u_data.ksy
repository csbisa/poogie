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
        size: 4
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
    - id: unknown1
      type: u2
    - id: unknown2
      type: u2
    - id: unknown3
      type: u1
    - id: count
      type: u1
    - id: blocks
      type: subblock
      repeat: eos
  subblock:
    seq:
      - id: unknown1
        type: u1
      - id: length
        type: u1
      - id: unknown2
        type: u2
      - id: type
        type: u2
      - id: data
        size: length-4
        if: length != 0xFF and length != 0xFE and length >= 4
