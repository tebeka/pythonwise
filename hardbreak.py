#!/usr/bin/env python

__author__ = "Miki Tebeka <miki.tebeka@gmail.com>"

'''*Hard* breakpoints'''
from pdb import set_trace

def buggy_function():
    pass
    pass
    set_trace() # Break here
    pass
    pass

if __name__ == "__main__":
    buggy_function()
