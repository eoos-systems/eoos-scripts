#!/usr/bin/env python3
# @file      ProgramOnUbuntu.py
# @author    Sergey Baigudin, sergey@baigudin.software
# @copyright 2023, Sergey Baigudin, Baigudin Software

from make.Program import Program
from common.Message import Message

class ProgramOnUbuntu(Program):

    def _do_build(self):    
        if self._get_args().build is None:    
            return
            
        args = ['cmake', f'-DCMAKE_BUILD_TYPE={self._get_args().config}']
        if self._get_args().build == 'ALL':
            Message.out(f'[BUILD] Generating CMake project for all targets...', Message.INF)
            args.append('-DEOOS_ENABLE_TESTS=ON')
            if self._get_args().coverage is True:
                args.append('-DEOOS_ENABLE_GCC_COVERAGE=ON')
        elif self._get_args().build == 'EOOS':
            Message.out(f'[BUILD] Generating CMake project for the EOOS target...', Message.INF)
        else:
            raise Exception(f'Cannot process --build {self._get_args().build} argument')
        args.append('..')
        self._run_subprocess_from_build_dir(args)
        
        args.clear()
        args = ['make', 'all']        
        if self._get_args().jobs is not None:
            args.extend(['-j', str(self._get_args().jobs)])
        Message.out(f'[BUILD] Building Make project...', Message.INF)                
        self._run_subprocess_from_build_dir(args)


    def _do_install(self):
        if self._get_args().install is True:
            Message.out(f'[BUILD] installing the library...', Message.INF)
            args = ['sudo', 'make', 'install']
            self._run_subprocess_from_build_dir(args)


    def _do_coverage(self):
        if self._get_args().coverage is not True:
            return
        Message.out(f'[BUILD] Generating code coverage report...', Message.INF)
        args = ['make', 'coverage']
        self._run_subprocess_from_build_dir(args)


    def _get_run_ut_executable_path_to(self):
        return './codebase/tests'


    def _get_run_ut_executable_path_back(self):
        return './../..'


    def _get_run_executable(self):
        return f'./EoosTests'
