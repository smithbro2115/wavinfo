
import struct


from .wave_ixml_reader import WavIXMLFormat

from collections import namedtuple


ListChunkDescriptor = namedtuple('ListChunk' , 'signature children')


class ChunkDescriptor(namedtuple('Chunk', 'ident start length') ):
    def read_data(self, from_stream):
        from_stream.seek(self.start)
        return from_stream.read(self.length)


def parse_list_chunk(stream, length):
    children = []

    start = stream.tell()

    signature = stream.read(4)

    while (stream.tell() - start) < length:
        children.append(parse_chunk(stream))

    return ListChunkDescriptor(signature=signature, children=children)


def parse_chunk(stream):
    ident = stream.read(4)
    if len(ident) != 4: 
        return

    sizeb = stream.read(4)
    size  = struct.unpack('<I',sizeb)[0]

    displacement = size
    if displacement % 2 is not 0:
        displacement = displacement + 1

    if ident in [b'RIFF',b'LIST']:
        return parse_list_chunk(stream=stream, length=size)
    else:
        start = stream.tell()
        stream.seek(displacement,1)
        return ChunkDescriptor(ident=ident, start=start, length=size)



WavInfoFormat = namedtuple("WavInfoFormat",'audio_format channel_count sample_rate byte_rate block_align bits_per_sample')

WavBextFormat = namedtuple("WavBextFormat",'description originator originator_ref ' + 
    'originator_date originator_time time_reference version umid ' + 
    'loudness_value loudness_range max_true_peak max_momentary_loudness max_shortterm_loudness ' +
    'coding_history')








        



