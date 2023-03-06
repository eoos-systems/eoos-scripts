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
        self.__path_to_script_dir = None
        self.__construct()


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
            self.__do_run_app_hello_world()
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


    def __do_build(self):
        if self.__args.build is not True:    
            return
        os.chdir(self.__PATH_TO_BUILD_DIR)
        ret = subprocess.run(['cmake', '..']).returncode
        os.chdir(self.__path_to_script_dir)        
        if ret != 0:
            raise Exception(f'CMake project is not generated with code [{ret}]')
        Message.out(f'[BUILD] Building CMake project...', Message.INF)
        args = ['cmake', '--build', '.', '--config', self.__args.config]
        if self.__args.jobs is not None:
            args.append('-j') 
            args.append(str(self.__args.jobs))        
        os.chdir(self.__PATH_TO_BUILD_DIR)
        ret = subprocess.run(args).returncode
        os.chdir(self.__path_to_script_dir)        
        if ret != 0:
            raise Exception(f'CMake project is not built with code [{ret}]')        


    def __do_run_app_hello_world(self):
        if self.__args.run is not True:    
            return        
    
        Message.out(f'[RUN] EoosAppHelloWorld with 0 arg...', Message.INF)
        os.chdir(self.__PATH_TO_BUILD_DIR)
        os.chdir(self.__get_run_ut_executable_path_to())
        ret = subprocess.run([self.__get_run_executable()]).returncode
        os.chdir(self.__get_run_ut_executable_path_back())
        os.chdir(self.__path_to_script_dir)
        if ret != 0:
            raise Exception(f'UT execution error with exit code [{ret}]')

        Message.out(f'[RUN] EoosAppHelloWorld with 1 arg...', Message.INF)
        os.chdir(self.__PATH_TO_BUILD_DIR)
        os.chdir(self.__get_run_ut_executable_path_to())
        ret = subprocess.run([self.__get_run_executable(), 'Think']).returncode
        os.chdir(self.__get_run_ut_executable_path_back())
        os.chdir(self.__path_to_script_dir)
        if ret != 0:
            raise Exception(f'UT execution error with exit code [{ret}]')            
        
        Message.out(f'[RUN] EoosAppHelloWorld with 2 arg...', Message.INF)
        os.chdir(self.__PATH_TO_BUILD_DIR)
        os.chdir(self.__get_run_ut_executable_path_to())
        ret = subprocess.run([self.__get_run_executable(), 'Think', 'Create']).returncode
        os.chdir(self.__get_run_ut_executable_path_back())
        os.chdir(self.__path_to_script_dir)
        if ret != 0:
            raise Exception(f'UT execution error with exit code [{ret}]')

        Message.out(f'[RUN] EoosAppHelloWorld with 3 arg...', Message.INF)
        os.chdir(self.__PATH_TO_BUILD_DIR)
        os.chdir(self.__get_run_ut_executable_path_to())
        ret = subprocess.run([self.__get_run_executable(), 'Think', 'Create', 'Win']).returncode
        os.chdir(self.__get_run_ut_executable_path_back())
        os.chdir(self.__path_to_script_dir)
        if ret != 0:
            raise Exception(f'UT execution error with exit code [{ret}]')
        
        Message.out(f'[RUN] EoosAppHelloWorld with 4 arg...', Message.INF)
        os.chdir(self.__PATH_TO_BUILD_DIR)
        os.chdir(self.__get_run_ut_executable_path_to())
        ret = subprocess.run([self.__get_run_executable(), 'Think', 'Create', 'Win', 'Destroy']).returncode
        os.chdir(self.__get_run_ut_executable_path_back())
        os.chdir(self.__path_to_script_dir)
        if ret != 1:
            raise Exception(f'UT execution error with exit code [{ret}]')


    def __get_run_ut_executable_path_to(self):
        if Os.is_posix():
            return f'./codebase/app-hello-world'
        elif Os.is_win32():
            return f'./codebase/app-hello-world/{self.__args.config}'
        else:
            raise Exception(f'Unknown OS to build')


    def __get_run_ut_executable_path_back(self):
        if Os.is_posix():
            return f'./../..'
        elif Os.is_win32():
            return f'./../../..'
        else:
            raise Exception(f'Unknown OS to build')


    def __get_run_executable(self):
        if Os.is_posix():
            return f'./EoosAppHelloWorld'
        elif Os.is_win32():
            return f'EoosAppHelloWorld.exe'
        else:
            raise Exception(f'Unknown OS to build')


    def __construct(self):
        self.__set_platform_paths() 


    def __set_platform_paths(self):
        if Os.is_posix():
            self.__path_to_script_dir = "./../../eoos-if-posix/scripts/python"
        elif Os.is_win32():
            self.__path_to_script_dir = "./../../eoos-if-win32/scripts/python"
        else:
            raise Exception(f'Unknown OS to build')


    def __check_run_path(self):
        if self.__is_correct_location() is not True:
            raise Exception(f'Script run directory is wrong, or you did not clone EOOS Super Repository.')


    def __is_correct_location(self):
        if os.path.isdir(f'./../python') is not True:
            return False
        if os.path.isdir(f'./../../scripts') is not True:
            return False
        if os.path.isdir(f'./../../codebase') is not True:
            return False
        if os.path.isdir(f'./../../../eoos-sample-applications') is not True:
            return False
        return True


    def __parse_args(self):
        parser = argparse.ArgumentParser(prog=self.__PROGRAM_NAME\
            , description='Builds and runs the EOOS sample applications project'\
            , epilog='(c) 2023, Sergey Baigudin, Baigudin Software' )
        parser.add_argument('-c', '--clean'\
            , action='store_true'\
            , help='rebuild the project by removing the "build" directory')
        parser.add_argument('-b', '--build'\
            , action='store_true'\
            , help='compile the project')
        parser.add_argument('-r', '--run'\
            , action='store_true'\
            , help='run all sample applications one by one')
        parser.add_argument('--config'\
            , choices=['Release', 'Debug', 'RelWithDebInfo', 'MinSizeRel']\
            , default='RelWithDebInfo'
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
        if self.__args.build is True:
            Message.out(f'[INFO] Argument BUILD = {self.__args.build}', Message.INF)
        if self.__args.run is True:
            Message.out(f'[INFO] Argument RUN = {self.__args.run}', Message.INF)            
        if self.__args.config is not None:
            Message.out(f'[INFO] Argument CONFIG = {self.__args.config}', Message.INF)
        if self.__args.jobs is not None:
            Message.out(f'[INFO] Argument JOBS = {self.__args.jobs}', Message.INF)


    __PROGRAM_NAME = 'EOOS Sample Application Builder'
    __PROGRAM_VERSION = '1.0.0'
    __PATH_TO_BUILD_DIR = './../../../eoos-sample-applications/build'
 