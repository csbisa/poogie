meta:
  id: mh4u_remote_packet
  endian: le
  application: |
    Specifies the outer wrapper for network packets for the following games:
    * Monster Hunter 3 Ultimate
    * Monster Hunter 4 Ultimate
    * Monster Hunter Generations
    TODO The Japanese version of games may use a different header magic value.
    TODO I believe a given packet can have multiple of the following sequence.
seq:
  - id: magic
    contents: [0xea, 0xd0]
  - id: val0
    type: u1
  - id: extra_hdr_len
    type: u1
  - id: data_length
    type: u2
    doc: Dictates the total length of data blocks at the end of the packet,
         including the data block lengths.
  - id: val1
    type: u1
  - id: val2
    type: u1
  - id: flags
    type: u2
    doc: |
      * 0x20: Data block starts with a little-endian 4-byte length specifier
              rather than the usual big-endian 2-byte length specifier.
              TODO This is apparently used for 0x0082 too, but that doesn't
                   contain a positive indicator for it.
  - id: identifier
    type: u2
  - id: seq_num
    type: u2
  - id: checksum
    size: 16
    doc: MD5 checksum of packet contents
  - id: extra_hdr
    size: extra_hdr_len
  - id: data_blocks
    type: data_blocks
    size: data_length
types:
  data_blocks:
    seq:
      - id: data_blocks
        type: data_block
        repeat: eos
  data_block:
    seq:
      - id: length
        type: u2be
        if: (_parent._parent.flags & 0x2020) == 0 and _parent._parent.flags != 0x0082
      - id: length
        type: u4
        if: (_parent._parent.flags & 0x20) != 0 or _parent._parent.flags == 0x0082
      - id: data
        size: length
        if: (_parent._parent.flags & 0x2000) == 0
      - id: data
        size: 4
        if: (_parent._parent.flags & 0x2000) != 0
