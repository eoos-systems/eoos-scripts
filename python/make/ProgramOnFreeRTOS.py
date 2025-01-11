#!/usr/bin/env python3
# @file      ProgramOnFreeRTOS.py
# @author    Sergey Baigudin, sergey@baigudin.software
# @copyright 2024, Sergey Baigudin, Baigudin Software

from make.Program import Program
from common.Message import Message

class ProgramOnFreeRTOS(Program):
    """
    Program on ProgramOnFreeRTOS.
    """

    def _do_build(self):
        if self._get_args().build is None:
            return

        args = ['cmake', \
                f'-DCMAKE_TOOLCHAIN_FILE=./../cmake/Toolchain.cortex-m3.gcc.cmake', \
                f'-DCMAKE_BUILD_TYPE={self._get_args().config}' \
        ]

        if self._get_args().build == 'ALL':
            Message.out(f'[BUILD] Generating CMake project for all targets...', Message.INF)
        elif self._get_args().build == 'EOOS':
            raise Exception(f'The EOOS parameter of --build argument is not processed for the moment')
        else:
            raise Exception(f'Cannot process --build {self._get_args().build} argument')

        if self._get_args().define is not None:
            for d in self._get_args().define:
                args.append(f'-D{d}')

        args.append('..')
        self._run_subprocess_from_build_dir(args)

        args.clear()
        args = ['make', 'all']

        if self._get_args().verbose is True:
            args.append('VERBOSE=1')
        if self._get_args().jobs is not None:
            args.extend(['-j', str(self._get_args().jobs)])

        Message.out(f'[BUILD] Building Make project...', Message.INF)
        self._run_subprocess_from_build_dir(args)


    def _do_install(self):
        if self._get_args().install is True:
            raise Exception(f'FreeRTOS program is not installable')


    def _do_run(self):
        if self._get_args().run is not None:
            raise Exception(f'FreeRTOS program is not runnable')


    def _do_coverage(self):
        if self._get_args().coverage is True:
            raise Exception(f'FreeRTOS program is not coverable')


    def _get_run_ut_executable_path_to(self):
        return './codebase/tests'


    def _get_run_ut_executable_path_back(self):
        return './../..'


    def _get_run_executable(self):
        return f'./EoosTests'
