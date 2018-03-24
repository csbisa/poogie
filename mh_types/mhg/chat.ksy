meta:
  id: chat
  endian: le
seq:
  - id: unknown1
    size: 4
  - id: unknown2
    type: u2be
  - id: name
    type: strz
    encoding: UTF-8
  - id: msg
    type: strz
    encoding: UTF-8
