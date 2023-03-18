#!/usr/bin/env python3
# @file      Make.py
# @author    Sergey Baigudin, sergey@baigudin.software
# @copyright 2023, Sergey Baigudin, Baigudin Software

import sys

from common.System import System
from make.ProgramOnUbuntu import ProgramOnUbuntu
from make.ProgramOnWindows import ProgramOnWindows


def main():
    try:
        program = None
        if System.is_posix():
            program = ProgramOnUbuntu()
        elif System.is_win32():
            program = ProgramOnWindows()
        else:
            raise Exception(f'Unknown host operating system')
        return program.execute()
    except BaseException as e:
        print(e)    
        return 1


if __name__ == "__main__":
    sys.exit( main() )
