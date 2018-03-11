from mh_types.generated.mh4u_remote_packet import Mh4uRemotePacket
from mh_types.generated.mh4u_data import Mh4uData
from scapy.utils import PcapReader
from scapy.layers.inet import UDP, Raw

def generate_xor_bytes(byte1, byte2):
    seed = byte1 + (byte2 << 8)
    seed = seed * 0xfc21
    seed = seed + 0x1a2b
    while True:
        val = ((seed & 0xffff) * 0xfc21) & 0xffffffff
        val = (val + (seed >> 16)) & 0xffffffff
        yield val & 0xff
        val2 = val
        val = ((val & 0xffff) * 0xfc21) & 0xffffffff
        val = (val + (val2 >> 16)) & 0xffffffff
        yield val & 0xff
        seed = val

def unobfuscate(payload, len):
    g = generate_xor_bytes(payload[0], payload[1])
    # TODO Probably should discard the first two bytes, but current type
    # formats account for it.
    return payload[0:2] + bytes(a ^ b for a, b in zip(payload[2:], g))

# FIXME Blocks currently have padding which isn't accounted for. This hack just
# tries all possible padding lengths and returns whatever succeeeds.
def try_parse(data):
    for i in [0, 1, 2, 3, 4, 5, 6, 7]:
        try:
            return Mh4uData.from_bytes(data[:len(data)-i])
        except EOFError:
            pass
    raise

class MHPacketProcessor():
    base_time = 0
    unrelated_packets = 0
    failed_remote_packet_load = 0
    failed_block_parse = 0
    parsed_subblocks = 0

    def __init__(self, callback):
        self.callback = callback

    def process(self, pkt, verbose=False, **kwargs):
        """Processes a single scapy packet.

        If the packet is determined to be related, the object's callback
        function will be called with a Subblock and relative time for
        the packet, as well as any additional keyword arguments provided
        to this function.
        """
        if self.base_time == 0:
            self.base_time = pkt.time

        if UDP not in pkt or Raw not in pkt or pkt[Raw].load[0:2] != b'\xea\xd0':
            return

        try:
            parsed = Mh4uRemotePacket.from_bytes(pkt[Raw].load)
        except:
            self.failed_remote_packet_load += 1
            if verbose:
                print("Failed to parse remote packet")
            return

        if parsed.flags != 0x882:
            self.unrelated_packets += 1
            if verbose:
                print("Skipped unrelated packet")
            return

        for block in parsed.data_blocks.data_blocks:
            block = unobfuscate(block.data, block.length)
            try:
                parsed_block = try_parse(block)
            except:
                self.failed_block_parse += 1
                if verbose:
                    print("Failed to parse block")
                return

            for r in parsed_block.blocks:
                for s in r.data.blocks:
                    self.parsed_subblocks += 1
                    self.callback(s, time=pkt.time - self.base_time, **kwargs)

    def get_stats(self):
        return {'parsed_subblocks': self.parsed_subblocks,
                'unrelated_packets': self.unrelated_packets,
                'failed_remote_packet_load': self.failed_remote_packet_load,
                'failed_block_parse': self.failed_block_parse}
