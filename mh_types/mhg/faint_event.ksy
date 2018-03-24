meta:
  id: faint_event
  endian: le
seq:
  - id: magic
    contents: [0x23, 0x2e, 0x0e, 0x88]
  - id: req
    type: u1
    doc: |
      * 0 - Notification of event
      * 1 - Confirmation of event. Quest host sends confirmation to all other
            players once notification has been received.
  - id: player_id
    type: u1
    doc: ID for the player that fainted
