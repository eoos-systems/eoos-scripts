#!/usr/bin/env python3
# @file      ProgramOnWin32.py
# @author    Sergey Baigudin, sergey@baigudin.software
# @copyright 2023-2025, Sergey Baigudin, Baigudin Software

from make.Program import Program
from common.System import System
from common.Message import Message

class ProgramOnWin32(Program):
    """
    Program on WIN32.
    """

    def __init__(self, args):
        if System.is_win32() is not True:
            raise Exception(f'Unsuppoted host OS')
        super().__init__(args)


    def _do_build(self):
        if self._get_args().build is None:
            return

        args = ['cmake']
        if self._get_args().build == 'ALL':
            Message.out(f'[BUILD] Generating CMake project for all targets...', Message.INF)
            args.append('-DEOOS_CMAKE_ENABLE_TESTS=ON')
        elif self._get_args().build == 'EOOS':
            Message.out(f'[BUILD] Generating CMake project for the EOOS target...', Message.INF)
        else:
            raise Exception(f'Cannot process --build {self._get_args().build} argument')
        if self._get_args().define is not None:
            for d in self._get_args().define:
                args.append(f'-D{d}')
        args.append('..')
        self._run_subprocess_from_build_dir(args)

        args.clear()
        Message.out(f'[BUILD] Building CMake project...', Message.INF)
        args = ['cmake', '--build', '.', '--config', self._get_args().config]
        if self._get_args().verbose is True:
            args.append('--verbose')
        if self._get_args().jobs is not None:
            args.extend(['-j', str(self._get_args().jobs)])
        self._run_subprocess_from_build_dir(args)


    def _do_install(self):
        if self._get_args().install is True:
            Message.out(f'[BUILD] installing the library...', Message.INF)
            args = ['cmake', '--install', '.', '--config', self._get_args().config]
            self._run_subprocess_from_build_dir(args)


    def _do_run(self):
        self._do_run_ut()


    def _do_coverage(self):
        if self._get_args().coverage is not True:
            return
        Message.out(f'[BUILD] Generating code coverage report...', Message.INF)
        path = f'./build/{self._get_run_ut_executable_path_to()}/{self._get_run_executable()}'
        args = ['OpenCppCoverage.exe'
            , '--sources', 'codebase\interface'
            , '--sources', 'codebase\library'
            , '--sources', 'codebase\system'
            , '--export_type', 'html:build\coverage'
            , '--', path]
        path_to = f'{self._PATH_TO_BUILD_DIR}/..'
        path_back = f'./build/{self._PATH_TO_SCRIPT_DIR}'
        self._run_subprocess_from_build_dir(args, path_to, path_back)


    def _get_run_ut_executable_path_to(self):
        return f'./codebase/tests/{self._get_args().config}'


    def _get_run_ut_executable_path_back(self):
        return './../../..'


    def _get_run_executable(self):
        return 'EoosTests.exe'
