This file covers type categorization notes. Eventually, this should
end up in the format specification but the formats aren't accurate
enough and will likely need to be reworked.

## MH4U Types

The ``type`` field is currently not really accurate. As seen in the
list below, there's a component which is actually used to identify the
player. For example, with player movement, the first player will send
packets with type 0x0101, and the second player will send 0x0102, and
so on.

Some categorized types:

* 0101: player movement (sender-identified)
* 0102: player movement (sender-identified)
* 0b01: player status (sender-identified)
* 0b02: player status (sender-identified)
* 0105: monster status
* 0515: guild card
* 0715: player info
* 1001: chat
* 010b: palico status (same player as 030b)
* 030b: palico status (same player as 010b)

### Still needs to be categorized:

* Quest post (and unpost): This appears to only match ``unknown2 &
  0xff == 0x6``. The ``type`` field is actually a sequence number
  in this case.

### Ignored

* Subblocks with a length of 254 or 255 (i.e. 0xfe and 0xff) don't
  have a payload.
* Subblocks with a type of 0xdc19 appears to used as a healthcheck.
