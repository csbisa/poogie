meta:
  id: player_movement
  endian: le
seq:
  - id: unknown1
    size: 59
  - id: activity
    type: u1
    doc: |
      * 0 - Stationary
      * 1 - Moving
      * 2 - Sheathing
      * 4 - Attacking
      * 6 - Rolling
      * 11 - Gesturing
  - id: action
    type: u1
  - id: unknown2
    size: 71
enums:
  gesture:
    0: none
    1: wave
    2: fistpump
    3: clap
    4: nod
    5: bow
    6: lament
    7: rant
    8: shadowbox
    9: shrug
    10: point
    11: greet
    12: kickback
    15: flaunt
    16: prance
    17: taunt
    20: dance
    84: drinking
    86: eating
    87: postconsume # after consuming item
    90: sharpening
  attackhammer:
    0: sideswing
    1: pound1
    2: pound4 # after sideswing2
    3: pound2
    4: golfswing
    6: unsheatheupswing
    7: charging
    11: charge1
    12: uppercut # lv2 charge while stationary
    13: movingswing # lv1 charge while moving
    14: uppercut2 # lv2 charge while moving
    16: superpound # lv3 charge while stationary
    18: spin # lv3 charge while moving
    19: spinfinish # timed spin finisher
    20: spinearlyfinish # early finish during lv3 spin
    21: upswing # after lv1 charge
    22: chargeafterpound2
    23: chargeaftergolfswing
    26: sideswing2 # after uppercut
    27: pound3 # 2nd attack after lv1 charge
    29: chargeroll # charging after a roll
