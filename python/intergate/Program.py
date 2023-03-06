#!/usr/bin/env python3
# @file      Program.py
# @author    Sergey Baigudin, sergey@baigudin.software
# @copyright 2023, Sergey Baigudin, Baigudin Software

import os
import time
import argparse
import shutil
import subprocess
from common.Message import Message
from common.Os import Os

class Program():

    def __init__(self):
        self.__args = None


    def execute(self):
        time_start = time.time()
        error = 0
        try:
            Message.out(f'Welcome to {self.__PROGRAM_NAME}', Message.OK, True)
            self.__parse_args()
            self.__check_run_path()
            self.__print_args()
            self.__do_run_eoos_ut('Release')
            self.__do_run_eoos_ut('Debug')
            self.__do_run_eoos_ut('RelWithDebInfo')
            self.__do_run_eoos_ut('MinSizeRel')
            self.__do_install_eoos('RelWithDebInfo')
            self.__do_run_eoos_sample_applications('RelWithDebInfo')
        except Exception as e:
            Message.out(f'[EXCEPTION] {e}', Message.ERR)        
            error = 1
        finally:
            self.__do_clean()
            status = Message.OK
            not_word = ''
            if error != 0:
                status = Message.ERR
                not_word = ' NOT'
            time_execute = round(time.time() - time_start, 9)
            Message.out(f'{self.__PROGRAM_NAME} has{not_word} been completed in {str(time_execute)} seconds', status, is_block=True)
            return error


    def __do_run_eoos_ut(self, config):
        if self.__args.build != 'EOOS' and self.__args.build != 'ALL':
            return
        Message.out(f'Run EOOS Unit Tests for "{config}" configuration', Message.INF, True)
        ret = subprocess.run([self.__args.interpreter, 'MakeEoos.py', '-c', '-b', 'ALL', '-r', '--config', config, '-j', '8']).returncode
        if ret != 0:
            raise Exception(f'EOOS build error with exit code [{ret}]')


    def __do_install_eoos(self, config):
        if self.__args.no_install is True:
            return    
        Message.out(f'Install EOOS for "{config}" configuration', Message.INF, True)
        ret = subprocess.run([self.__args.interpreter, 'MakeEoos.py', '-c', '-b', 'EOOS', '--install', '--config', config, '-j', '8']).returncode
        if ret != 0:
            raise Exception(f'EOOS install error with exit code [{ret}]')


    def __do_run_eoos_sample_applications(self, config):
        if self.__args.build != 'APPS' and self.__args.build != 'ALL':
            return    
        Message.out(f'Run EOOS Sample Applications for "{config}" configuration', Message.INF, True)
        ret = subprocess.run([self.__args.interpreter, 'MakeApp.py', '-c', '-b', '-r', '--config', config, '-j', '8']).returncode
        if ret != 0:
            raise Exception(f'APP build error with exit code [{ret}]')


    def __do_clean(self):
        if os.path.isdir(self.__PATH_TO_EOOS_BUILD_DIR):
            Message.out(f'[BUILD] Deleting EOOS "build" directory...', Message.INF)        
            shutil.rmtree(self.__PATH_TO_EOOS_BUILD_DIR)
        if os.path.isdir(self.__PATH_TO_APPS_BUILD_DIR):
            Message.out(f'[BUILD] Deleting APPS "build" directory...', Message.INF)        
            shutil.rmtree(self.__PATH_TO_APPS_BUILD_DIR)            


    def __check_run_path(self):
        if self.__is_correct_location() is not True:
            raise Exception(f'Script run directory is wrong. Please, run it from "\scripts\python\" directory')


    def __is_correct_location(self):
        if os.path.isdir(f'./../python') is not True:
            return False
        if os.path.isdir(f'./../../scripts') is not True:
            return False
        if os.path.isdir(f'./../../codebase') is not True:
            return False
        return True


    def __parse_args(self):
        pyVer = ''
        if Os.is_posix():
            pyVer = '3'
        parser = argparse.ArgumentParser(prog=self.__PROGRAM_NAME\
            , description='Runs the EOOS intergation build'\
            , epilog='(c) 2023, Sergey Baigudin, Baigudin Software' )
        parser.add_argument('-b', '--build'\
            , choices=['EOOS', 'APPS', 'ALL']\
            , default='ALL'\
            , help='compile appropriate projects')
        parser.add_argument('--no-install'\
            , action='store_true'\
            , help='do not install EOOS on OS')
        parser.add_argument('--interpreter'\
            , default=f'python{pyVer}'\
            , metavar='PYTHON_EXECUTABLE'\
            , help='set Python interpreter')
        parser.add_argument('--version'\
            , action='version'\
            , version=f'%(prog)s {self.__PROGRAM_VERSION}')
        self.__args = parser.parse_args()
 
 
    def __print_args(self):
        Message.out(f'[INFO] Argument BUILD = {self.__args.build}', Message.INF)
        Message.out(f'[INFO] Argument NO-INSTALL = {self.__args.no_install}', Message.INF)
 
    __PROGRAM_NAME = 'EOOS Automotive Intergator'
    __PROGRAM_VERSION = '1.0.0'    
    __PATH_TO_EOOS_BUILD_DIR = './../../build'
    __PATH_TO_APPS_BUILD_DIR = './../../../eoos-sample-applications/build'
