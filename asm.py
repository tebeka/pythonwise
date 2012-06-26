#!/usr/bin/env python
'''Demo assembler'''

# Each opcode is 16 bits
# Four MSB are instrucion code, rest is arguments
# We have:
# * Eight general registers r0-r7
# * ALU operators: move, add, sub
# * Memory operators: load, store
# * Unconditional jump: jmp

# Miki Tebeka <mtebeka@qualcomm.com>

ENV = globals().copy() # Clean user environment, should be first

PROGRAM = [] # Program is just a list of commands

# Location of fields
INST_SHIFT = 12
SLOT1_SHIFT = 8
SLOT2_SHIFT = 4
SLOT3_SHIFT = 0

from inspect import getouterframes, currentframe
def here():
    '''Get file and line number in source file'''
    try:
        return getouterframes(currentframe())[3][1:3]
    except:
        return '???', 0

def out(type, filename, line, msg):
    '''Output message'''
    print('{}:{}: {}: {}'.format(filename, line, type, msg))

def error(file, line, msg):
    '''Print error message'''
    out('error', file, line, msg)

def warn(file, line, msg):
    '''Print warning message'''
    out('warning', file, line, msg)

class ASM:
    '''Base ASM instruction'''
    def __init__(self):
        self.file, self.line = here()
        PROGRAM.append(self)

    def genbits(self):
        '''Generate bits

            code will be defined in each derived class
        '''
        return (self.code << INST_SHIFT) | self._genbits()

class ALU3(ASM):
    '''ALU instruction with 3 operands'''
    def __init__(self, src1, src2, dest):
        ASM.__init__(self)
        self.src1 = src1
        self.src2 = src2
        self.dest = dest

    def _genbits(self):
        return (self.src1 << SLOT1_SHIFT) | \
               (self.src2 << SLOT2_SHIFT)  | \
               (self.dest << SLOT3_SHIFT)

class add(ALU3):
    '''`add' instruction'''
    code = 0

class sub(ALU3):
    '''`sub' instruction'''
    code = 1

class move(ASM):
    code = 2

    '''`move' instruction'''
    def __init__(self, src, dest):
        ASM.__init__(self)
        self.src = src
        self.dest = dest

    def _genbits(self):
        return (self.src << SLOT1_SHIFT) | \
               (self.dest << SLOT2_SHIFT)

class MemOp(ASM):
    '''Memory operation'''
    def __init__(self, reg, addr):
        ASM.__init__(self)
        self.reg = reg
        if addr >= (1 << 16): # Check that address is valid
            warn(self.file, self.line, '0x%X too big, will truncate' % addr)
            addr &= ((1 << 16) - 1) # Mask all bits above 16
        self.addr = addr

    def _genbits(self):
        return (self.reg << SLOT1_SHIFT) | \
               self.addr

class load(MemOp):
    '''`load' instruction'''
    code = 3

class store(MemOp):
    '''`store' instruction'''
    code = 4

class jmp(ASM):
    code = 5

    '''`jmp' instruction'''
    def __init__(self, dest):
        ASM.__init__(self)
        self.dest = dest

    def _genbits(self):
        return self.dest

def label(name):
    '''Setting a label'''
    ENV[name] = len(PROGRAM)


def initialize():
    # Setup user environment
    # Add registers
    for i in range(8):
        ENV['r%d' % i] = i

    # Add operators
    for op in (add, sub, move, load, store, label, jmp):
        ENV[op.__name__] = op

def main(argv=None):
    import sys
    from argparse import ArgumentParser
    from os.path import splitext, isfile
    from array import array
    from sys import exc_info, byteorder

    argv = argv or sys.argv

    parser = ArgumentParser()
    parser.add_argument('-o', '--output', help='output file', dest='outfile',
        default='')
    parser.add_argument('-g', help='create debug file', dest='debug',
        action='store_true', default=0)
    parser.add_argument('file', help='File to assemble')

    args = parser.parse_args()

    if not isfile(args.file):
        raise SystemExit('cannott find {}'.format(args.file))

    initialize()

    try:
        execfile(args.file, ENV, {})
    except SyntaxError, e:
        error(e.filename, e.lineno, e.msg)
        raise SystemExit(1)
    except Exception, e:
        # Get last traceback and print it
        # Most of this code is taken from traceback.py:print_exception
        etype, value, tb = exc_info()
        while tb: # Find last traceback
            last = tb
            tb = tb.tb_next
        lineno = last.tb_lineno # Line number
        f = last.tb_frame
        co = f.f_code
        error(co.co_filename, lineno, e)
        raise SystemExit(1)

    a = array('H')
    for cmd in PROGRAM:
        a.append(cmd.genbits())
    if byteorder == 'little':
            a.byteswap()

    if not args.outfile:
        args.outfile = splitext(args.file)[0] + '.o'

    open(args.outfile, 'wb').write(a.tostring())
    if args.debug: # Emit debug information
        with open(splitext(args.file)[0] + '.dbg', 'w') as dbg:
            for cmd in PROGRAM:
                dbg.write('{}: {}\n'.format(cmd.file, cmd.line))

if __name__ == '__main__':
    main()
