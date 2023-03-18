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
from common.System import System

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
            self.__do_clean()
            self.__do_create()
            self.__do_build()
            self.__do_install()
            self.__do_run()
            self.__do_coverage()
        except Exception as e:
            Message.out(f'[EXCEPTION] {e}', Message.ERR)        
            error = 1
        finally:
            status = Message.OK
            not_word = ''
            if error != 0:
                status = Message.ERR
                not_word = ' NOT'
            time_execute = round(time.time() - time_start, 9)
            Message.out(f'{self.__PROGRAM_NAME} has{not_word} been completed in {str(time_execute)} seconds', status, is_block=True)
            return error
          
          
    def __do_clean(self):
        if self.__args.clean is not True:
            return
        if os.path.isdir(self.__PATH_TO_BUILD_DIR):
            Message.out(f'[BUILD] Deleting "build" directory...', Message.INF)        
            shutil.rmtree(self.__PATH_TO_BUILD_DIR)
            
            
    def __do_create(self):
        if not os.path.exists(self.__PATH_TO_BUILD_DIR):
            Message.out(f'[BUILD] Creating "build" directory...', Message.INF)
            os.makedirs(self.__PATH_TO_BUILD_DIR)
            os.makedirs(self.__PATH_TO_BUILD_DIR + '/CMakeInstallDir')
            os.makedirs(self.__PATH_TO_BUILD_DIR + '/sca')


    def __do_build(self):
        if self.__args.build is None:    
            return
            
        args = ['cmake']
        if System.is_posix() is True:
            args.append('-DCMAKE_BUILD_TYPE=' + self.__args.config)
        if self.__args.build == 'ALL':
            Message.out(f'[BUILD] Generating CMake project for all targets...', Message.INF)
            args.append('-DEOOS_ENABLE_TESTS=ON')
            if System.is_posix() is True and self.__args.coverage is True:
                args.append('-DEOOS_ENABLE_GCC_COVERAGE=ON')
        elif self.__args.build == 'EOOS':
            Message.out(f'[BUILD] Generating CMake project for the EOOS target...', Message.INF)
        else:
            raise Exception(f'Cannot process --build {self.__args.build} argument')
        args.append('..')
        self.__run_subprocess_from_build_dir(args)
        
        args.clear()
        if System.is_win32():
            Message.out(f'[BUILD] Building CMake project...', Message.INF)            
            args = ['cmake', '--build', '.', '--config', self.__args.config]
        elif System.is_posix():
            Message.out(f'[BUILD] Building Make project...', Message.INF)            
            args = ['make', 'all']
        else:
            raise Exception(f'Unknown host operating system')
        if self.__args.jobs is not None:
            args.extend(['-j', str(self.__args.jobs)])         
        self.__run_subprocess_from_build_dir(args)


    def __do_install(self):
        if self.__args.install is not True:
            return
        Message.out(f'[BUILD] installing the library...', Message.INF)        
        args = []
        if System.is_posix():
            args.extend(['sudo', 'make', 'install'])
        elif System.is_win32():
            args.extend(['cmake', '--install', '.', '--config', self.__args.config])
        else:
            raise Exception(f'Unknown host operating system')
        self.__run_subprocess_from_build_dir(args)


    def __do_run(self):
        if self.__args.run is not True:
            return
        Message.out(f'[BUILD] Running unit tests...', Message.INF)
        args = [self.__get_run_executable(), '--gtest_shuffle']
        path_to = f'{self.__PATH_TO_BUILD_DIR}/{ self.__get_run_ut_executable_path_to()}'
        path_back = f'{self.__get_run_ut_executable_path_back()}/{self.__PATH_TO_SCRIPT_DIR}'
        self.__run_subprocess_from_build_dir(args, path_to, path_back)


    def __do_coverage(self):
        if self.__args.coverage is not True:
            return
        Message.out(f'[BUILD] Generating code coverage report...', Message.INF)
        if System.is_posix():
            args = ['make', 'coverage']
            self.__run_subprocess_from_build_dir(args)
        if System.is_win32():
            path = f'./build/{self.__get_run_ut_executable_path_to()}/{self.__get_run_executable()}'
            args = ['OpenCppCoverage.exe'
                , '--sources', 'codebase\interface'
                , '--sources', 'codebase\library'
                , '--sources', 'codebase\system'
                , '--export_type', 'html:build\coverage'
                , '--', path]            
            path_to = f'{self.__PATH_TO_BUILD_DIR}/..'
            path_back = f'./build/{self.__PATH_TO_SCRIPT_DIR}'
            self.__run_subprocess_from_build_dir(args, path_to, path_back)            

        
    def __run_subprocess_from_build_dir(self, args, path_to=None, path_back=None):
        if path_to is None: 
            path_to = self.__PATH_TO_BUILD_DIR
        if path_back is None:
            path_back = self.__PATH_TO_SCRIPT_DIR
        os.chdir(path_to)
        ret = subprocess.run(args).returncode        
        os.chdir(path_back)
        if ret != 0:
            raise Exception(f'CMake project is not built with code [{ret}]')


    def __get_run_ut_executable_path_to(self):
        if System.is_posix():
            return f'./codebase/tests'
        elif System.is_win32():
            return f'./codebase/tests/{self.__args.config}'
        else:
            raise Exception(f'Unknown host operating system')


    def __get_run_ut_executable_path_back(self):
        if System.is_posix():
            return f'./../..'
        elif System.is_win32():
            return f'./../../..'
        else:
            raise Exception(f'Unknown host operating system')


    def __get_run_executable(self):
        if System.is_posix():
            return f'./EoosTests'
        elif System.is_win32():
            return f'EoosTests.exe'
        else:
            raise Exception(f'Unknown host operating system')


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
        parser = argparse.ArgumentParser(prog=self.__PROGRAM_NAME\
            , description='Builds and installs the EOOS project to your host OS'\
            , epilog='(c) 2023, Sergey Baigudin, Baigudin Software' )
        parser.add_argument('-c', '--clean'\
            , action='store_true'\
            , help='rebuild the project by removing the "build" directory')
        parser.add_argument('-b', '--build'\
            , choices=['EOOS', 'ALL']\
            , help='compile the project')
        parser.add_argument('-r', '--run'\
            , action='store_true'\
            , help='run unit tests')
        parser.add_argument('--coverage'\
            , action='store_true'\
            , help='run unit tests and create code coverage report')    
        parser.add_argument('--install'\
            , action='store_true'\
            , help='install on OS')
        parser.add_argument('--config'\
            , choices=['Release', 'Debug', 'RelWithDebInfo', 'MinSizeRel']\
            , default='Debug'
            , help='set project configuration')
        parser.add_argument('-j', '--jobs'\
            , type=int\
            , help='set number of parallel jobs to build')
        parser.add_argument('--version'\
            , action='version'\
            , version=f'%(prog)s {self.__PROGRAM_VERSION}')
        self.__args = parser.parse_args()
        
        
    def __print_args(self):
        if self.__args.clean is True:
            Message.out(f'[INFO] Argument CLEAN = {self.__args.clean}', Message.INF)
        if self.__args.build is not None:
            Message.out(f'[INFO] Argument BUILD = {self.__args.build}', Message.INF)
        if self.__args.run is True:
            Message.out(f'[INFO] Argument RUN = {self.__args.run}', Message.INF)
        if self.__args.coverage is True:
            Message.out(f'[INFO] Argument COVERAGE = {self.__args.coverage}', Message.INF)
        if self.__args.install is True:
            Message.out(f'[INFO] Argument INSTALL = {self.__args.install}', Message.INF)
        if self.__args.config is not None:
            Message.out(f'[INFO] Argument CONFIG = {self.__args.config}', Message.INF)
        if self.__args.jobs is not None:
            Message.out(f'[INFO] Argument JOBS = {self.__args.jobs}', Message.INF)
        if self.__args.install is True:
            Message.out(f'[NOTE] To install EOOS on Windows, a console has to be run as Administrator.', Message.NOR)


    __PROGRAM_NAME = 'EOOS Automotive Project Builder'
    __PROGRAM_VERSION = '1.0.0'
    __PATH_TO_BUILD_DIR = './../../build'
    __PATH_TO_SCRIPT_DIR = './../scripts/python'
 