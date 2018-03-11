meta:
  id: chat
  endian: le
seq:
  - id: unknown1
    size: 16
  - id: name
    type: str
    size: 24
    encoding: UTF-16
  - id: msg
    type: str
    size: 54
    encoding: UTF-16
    doc: Null-terminated. The remaining bytes may have data as it is not
         zeroed out by the client.
