Broadcast WAV Extension
=======================

.. module:: wavinfo

.. autoclass:: wavinfo.wave_bext_reader.WavBextReader
   :members:


Notes
-----
A WAV file produced to Broadcast-WAV specifications will have the broadcast metadata extension,
which includes a 256-character free text descrption, creating entity identifier (usually the 
recording application or equipment), the date and time of recording and a time reference for 
timecode synchronization.

The `coding_history` is designed to contain a record of every conversion performed on the audio
file.

In this example (from a Sound Devices 702T) the bext metadata contains scene/take slating
information in the `description`. Here also the `originator_ref` is a serial number conforming
to EBU Rec 99.

If the bext metadata conforms to EBU 3285 v1, it will contain the WAV's 32 or 64 byte SMPTE 
330M UMID. The 32-byte version of the UMID is usually just a random number, while the 64-byte 
UMID will also have information on the recording date and time, recording equipment and entity, 
and geolocation data.

If the bext metadata conforms to EBU 3285 v2, it will hold precomputed program loudness values
as described by EBU Rec 128.

..  code:: python

    print(info.bext.description)
    print("----------")
    print("Originator:", info.bext.originator)
    print("Originator Ref:", info.bext.originator_ref)
    print("Originator Date:", info.bext.originator_date)
    print("Originator Time:", info.bext.originator_time)
    print("Time Reference:", info.bext.time_reference)
    print(info.bext.coding_history)

Result: 

::

    sSPEED=023.976-ND
    sTAKE=1
    sUBITS=$12311801
    sSWVER=2.67
    sPROJECT=BMH
    sSCENE=A101
    sFILENAME=A101_1.WAV
    sTAPE=18Y12M31
    sTRK1=MKH516 A
    sTRK2=Boom
    sNOTE=
    
    ----------
    Originator: Sound Dev: 702T S#GR1112089007
    Originator Ref: USSDVGR1112089007124001008206301
    Originator Date: 2018-12-31
    Originator Time: 12:40:00
    Time Reference: 2190940753
    A=PCM,F=48000,W=24,M=stereo,R=48000,T=2 Ch
