#!/usr/bin/env python
'''Play a wav file on Linux

Freely copied from
http://www.velocityreviews.com/forums/t337346-how-to-play-sound-in-python.html
'''

import wave
import ossaudiodev

def playwave(wavefile):
    fo = wave.open(wavefile, "rb")
    (nc, sw, fr, nf, comptype, compname) = fo.getparams()
    dsp = ossaudiodev.open("/dev/dsp", "w")
    dsp.setparameters(ossaudiodev.AFMT_S16_NE, nc, fr)
    data = fo.readframes(nf)
    fo.close()
    dsp.write(data)
    dsp.close()

def main(argv=None):
    import sys
    from optparse import OptionParser
    from os.path import isfile

    argv = argv or sys.argv

    parser = OptionParser("%prog WAVEFILE")
    opts, args = parser.parse_args(argv[1:])
    if len(args) != 1:
        parser.error("wrong number of arguments") # Will exit

    wavefile = args[0]
    if not isfile(wavefile):
        raise SystemExit("error: can't find %s" % wavefile)


    playwave(wavefile)

if __name__ == "__main__":
    main()

