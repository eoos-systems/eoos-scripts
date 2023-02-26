#!/usr/bin/env python3
# @file      build.py
# @author    Sergey Baigudin, sergey@baigudin.software
# @copyright 2023, Sergey Baigudin, Baigudin Software

import os
import sys
import time
import argparse
from common.Message import Message

class Program():

    def __init__(self):
        self.__args = None
        self.__construct()


    def execute(self):
        time_start = time.time()
        error = 0
        try:
            Message.out('BUILDING OF PROJECT HAS BEEN INVOKED', Message.OK, True)
            if self.__args.clean is True:
                self.__do_clean()
            if self.__args.build is True:
                self.__do_build()
            if self.__args.run is True:
                self.__run()
        except Exception as e:
            print('EXCEPTION:', e)
            error = -1;
        finally:
            time_execute = time.time() - time_start
            status = Message.OK
            not_word = ''
            if error != 0:
                status = Message.ERR
                not_word = ' NOT'
            Message.out(f'BUILDING OF PROJECT HAS{not_word} BEEN COMPLETED in {str(time_execute)} seconds', status, is_block=True)
            return error
          
          
    def __do_clean(self):
        Message.out('[BUILD] EOOS flag set: CLEAN', Message.INF)
        is_exist = os.path.isdir('./../../build')
        

    def __do_build(self):
        Message.out('[BUILD] EOOS flag set: BUILD', Message.INF)

        
    def __do_run(self):
        Message.out('[BUILD] EOOS flag set: RUN', Message.INF)    

    
    def __construct(self):
        self.__parse_args()


    def __parse_args(self):
        parser = argparse.ArgumentParser(prog='EOOS Automotive Project Builder'                              \
            , description='Builds and installs the EOOS project to your host OS'  \
            , epilog='(c) 2023, Sergey Baigudin, Baigudin Software' )
        parser.add_argument('-c', '--clean', action='store_true', help='Rebuilds the project by removing the "build" directory')
        parser.add_argument('-b', '--build', action='store_true', help='Compiles the project')
        parser.add_argument('-r', '--run', action='store_true', help='Runs unit tests after the build')
        self.__args = parser.parse_args()


def main():
    program = Program()
    return program.execute()

if __name__ == "__main__":
    sys.exit( main() )
