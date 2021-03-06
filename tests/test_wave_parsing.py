import os.path
import sys
import json
import subprocess
from subprocess import PIPE

from unittest import TestCase

import wavinfo

FFPROBE='ffprobe'

def ffprobe(path):
    arguments = [ FFPROBE , "-of", "json" , "-show_format", "-show_streams", path ]
    if int(sys.version[0]) <  3:
        process = subprocess.Popen(arguments, stdout=PIPE)
        process.wait()
        if process.returncode == 0:
            output = process.communicate()[0]
            if output:
                output_str = output.decode('utf-8')
                return json.loads(output_str)
        else:
            return None
    else: 
        process = subprocess.run(arguments, stdin=None, stdout=PIPE, stderr=PIPE)
        if process.returncode == 0:
            output_str = process.stdout.decode('utf-8')
            return json.loads(output_str)
        else:
            return None

        
def all_files():
    for dirpath, _, filenames in os.walk('tests/test_files'):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in ['.wav','.WAV']:
                yield os.path.join(dirpath, filename)
        
class TestWaveInfo(TestCase):
    def test_sanity(self):
        for wav_file in all_files():
            info = wavinfo.WavInfoReader(wav_file)
            self.assertTrue(info is not None)

    def test_fmt_against_ffprobe(self):
        for wav_file in all_files():
            info = wavinfo.WavInfoReader(wav_file)
            ffprobe_info = ffprobe(wav_file)

            self.assertEqual( info.fmt.channel_count , ffprobe_info['streams'][0]['channels']  )
            self.assertEqual( info.fmt.sample_rate   , int(ffprobe_info['streams'][0]['sample_rate'])  )
            self.assertEqual( info.fmt.bits_per_sample, int(ffprobe_info['streams'][0]['bits_per_raw_sample']) )

            if info.fmt.audio_format == 1:
                self.assertTrue(ffprobe_info['streams'][0]['codec_name'].startswith('pcm')  )
                byte_rate = int(ffprobe_info['streams'][0]['sample_rate']) \
                        * ffprobe_info['streams'][0]['channels'] \
                        * int(ffprobe_info['streams'][0]['bits_per_raw_sample']) / 8
                self.assertEqual( info.fmt.byte_rate     , byte_rate  )

    def test_data_against_ffprobe(self):
        for wav_file in all_files():
            info = wavinfo.WavInfoReader(wav_file)
            ffprobe_info = ffprobe(wav_file)
            self.assertEqual( info.data.frame_count, int(ffprobe_info['streams'][0]['duration_ts'] ))

    def test_bext_against_ffprobe(self):
        for wav_file in all_files():
            info = wavinfo.WavInfoReader(wav_file)
            ffprobe_info = ffprobe(wav_file)
            if info.bext:
                self.assertEqual( info.bext.description, ffprobe_info['format']['tags']['comment']  )
                self.assertEqual( info.bext.originator, ffprobe_info['format']['tags']['encoded_by']  )
                if 'originator_reference' in ffprobe_info['format']['tags']:
                    self.assertEqual( info.bext.originator_ref, ffprobe_info['format']['tags']['originator_reference']  )
                else:
                    self.assertEqual( info.bext.originator_ref, '')

                # these don't always reflect the bext info
                # self.assertEqual( info.bext.originator_date, ffprobe_info['format']['tags']['date']  )
                # self.assertEqual( info.bext.originator_time, ffprobe_info['format']['tags']['creation_time']  )
                self.assertEqual( info.bext.time_reference, int(ffprobe_info['format']['tags']['time_reference'])  )

                if 'coding_history' in ffprobe_info['format']['tags']:
                    self.assertEqual( info.bext.coding_history, ffprobe_info['format']['tags']['coding_history']  )
                else:
                    self.assertEqual( info.bext.coding_history, '' )

    def test_ixml(self):
        expected = {'A101_4.WAV': {'project' : 'BMH', 'scene': 'A101', 'take': '4',
                        'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124015008231000'},
                    'A101_3.WAV': {'project' : 'BMH', 'scene': 'A101', 'take': '3',
                        'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124014008228300'},
                    'A101_2.WAV': {'project' : 'BMH', 'scene': 'A101', 'take': '2',
                        'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124004008218600'},
                    'A101_1.WAV': {'project' : 'BMH', 'scene': 'A101', 'take': '1',
                        'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124001008206300'},
                }

        for wav_file in all_files():
            basename =  os.path.basename(wav_file)
            if basename in expected:
                info = wavinfo.WavInfoReader(wav_file)
                e = expected[basename]

                self.assertEqual( e['project'], info.ixml.project )
                self.assertEqual( e['scene'], info.ixml.scene )
                self.assertEqual( e['take'], info.ixml.take )
                self.assertEqual( e['tape'], info.ixml.tape )
                self.assertEqual( e['family_uid'], info.ixml.family_uid )
