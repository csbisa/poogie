from mh_types.generated.mh4u_remote_packet import Mh4uRemotePacket
from mh_types.generated.mh4u_data import Mh4uData
from scapy.utils import PcapReader
from scapy.layers.inet import IP, UDP, Raw

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

def generate_stream_key(pkt):
    return str(pkt[IP].src) + str(pkt[UDP].sport) + '->' + str(pkt[IP].dst) + str(pkt[UDP].dport)

class MHPacketProcessor():
    def __init__(self, callback):
        self.callback = callback

        self.base_time = 0
        self.current_superblocks = {}

        # initialize counters
        self.failed_remote_packet_load = 0
        self.failed_block_parse = 0
        self.parsed_subblocks = 0
        self.superblock_count = 0
        self.pkt_count = 0
        self.duplicate_subblocks = 0
        self.unrelated_packets = 0

    def process(self, pkt, verbose=False, stateful=True, **kwargs):
        """Processes a single scapy packet.

        If the packet is determined to be related, the object's callback
        function will be called with a data chunk, flags and relative
        time for the packet, as well as any additional keyword arguments
        provided to this function.

        In stateful mode, superblocks will be parsed and the callback
        will only be invoked with assembled superblocks and not with
        partial superblocks.
        """
        if self.base_time == 0:
            self.base_time = pkt.time
        self.pkt_count += 1

        if UDP not in pkt or Raw not in pkt or pkt[Raw].load[0:2] != b'\xea\xd0':
            return

        try:
            parsed = Mh4uRemotePacket.from_bytes(pkt[Raw].load)
        except:
            self.failed_remote_packet_load += 1
            #self.failed_pkts.append(pkt)
            if verbose:
                print("Failed to parse remote packet from", pkt[IP].src)
                print(pkt[Raw].load)
            return

        if parsed.flags != 0x882:
            self.unrelated_packets += 1
            if verbose:
                print("Skipped unrelated packet from", pkt[IP].src)
            return

        for block in parsed.data_blocks.data_blocks:
            block = unobfuscate(block.data, block.length)
            try:
                parsed_block = try_parse(block)
            except:
                self.failed_block_parse += 1
                #self.failed_pkts.append(pkt)
                if verbose:
                    print("Failed to parse block")
                return

            for r in parsed_block.blocks:
                for s in r.data.blocks:
                    if not (s.flags & 0x20):
                        # Skipping dupes
                        self.duplicate_subblocks += 1
                        continue

                    self.parsed_subblocks += 1
                    handled = stateful and self._handle_superblock(s, pkt, **kwargs)
                    if not handled:
                        self.callback(s.data, s.flags, time=pkt.time - self.base_time, **kwargs)

    # Data may span over multiple subblocks, which is indicated by 0x40 in the
    # subblock flags. For lack of a better name, we call those superblocks.
    # Determining the end of the su[erblock appears to be context-dependent, so
    # we just use the simple heuristic of terminating the superblock once a
    # subblock of non-maximal length is processed.
    def _handle_superblock(self, s, pkt, **kwargs):
        if s.length == 0xFF or s.length == 0xFE:
            return False
        if not (s.flags & 0x40):
            return False

        key = generate_stream_key(pkt)
        sb = self.current_superblocks.get(key)
        if sb is None:
            #print("Found start of a running subblock")
            sb = [s]
            self.current_superblocks[key] = sb
        else:
            #print("Appending running subblock")
            sb.append(s)

        if s.length == 192:
            #print("Running subblock isn't complete yet, added:")
            #self.callback(s.data, self.current_superblock[0].flags, time=pkt.time - self.base_time, **kwargs)
            return True
        #print("Found running subblock end, its length is", s.length)
        self.superblock_count += 1
        #print("Calling back with running subblock of length", len(self.current_superblock))
        data = b''.join([d.data for d in sb])
        self.callback(data, sb[0].flags, time=pkt.time - self.base_time, **kwargs)
        del self.current_superblocks[key]
        return True

    def get_stats(self):
        return {'parsed_subblocks': self.parsed_subblocks,
                'unrelated_packets': self.unrelated_packets,
                'failed_remote_packet_load': self.failed_remote_packet_load,
                'failed_block_parse': self.failed_block_parse,
                'superblocks': self.superblock_count,
                'packets': self.pkt_count,
                'duplicate_subblocks': self.duplicate_subblocks}
