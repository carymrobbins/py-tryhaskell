# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import cmd
from collections import namedtuple
import json
import re
import sys

import requests

__version__ = '0.2.0'
__author__ = 'Cary Robbins <carymrobbins@gmail.com>'


class TryHaskell:
    Result = namedtuple('Result', 'ok, expr, files, stdout, type, value')

    class Error(Exception):
        pass

    @classmethod
    def _bad_result(cls, error):
        """
        :param str|unicode error: Syntax error from TryHaskell.
        :rtype: TryHaskell.Result
        """
        return cls.Result(ok=False, expr='', files={}, stdout='', type='', value=error)

    @classmethod
    def eval(cls, exp, files=None):
        """
        :param str|unicode exp: Haskell expression to evaluate.
        :rtype: str|unicode
        """
        return cls.show(cls.get(exp, files=files))

    @classmethod
    def get(cls, exp, files=None):
        """
        :param str|unicode exp: Haskell expression to evaluate.
        :param dict[str|unicode, str|unicode] files: Dictionary of file names->contents
        :rtype: TryHaskell.Result
        """
        return cls.parse(cls.raw(exp, files=files))


    @classmethod
    def raw(cls, exp, files=None):
        """
        :param str|unicode exp: Haskell expression to evaluate.
        :param dict[str|unicode, str|unicode] files: Dictionary of file names->contents
        :rtype: dict
        """
        payload = {'exp': exp}
        if files:
            # TODO: Implement stdin.
            stdin = []
            payload['args'] = json.dumps([stdin, files])
        try:
            return requests.get('http://tryhaskell.org/eval', params=payload).json()
        except ValueError as e:
            raise cls.Error(e)

    @classmethod
    def parse(cls, j):
        """
        :param dict j: JSON response from TryHaskell.
        :rtype: TryHaskell.Result
        """
        error = j.get('error')
        if error:
            return cls._bad_result(error)
        success = j.get('success')
        if success:
            try:
                return cls.Result(ok=True, **j.get('success'))
            except (TypeError, ValueError) as e:
                raise cls.Error(e)
        # If there was neither a success nor an error, the service
        # is probably expecting something from stdin, which is not
        # currently implemented.
        # TODO: Implement stdin.
        return cls._bad_result('Unsupported operation.')

    @classmethod
    def show(cls, result):
        """
        :param TryHaskell.Result result: Parse result of JSON data.
        :rtype: str|unicode
        """
        if result.ok:
            if result.stdout:
                out = '\n'.join(result.stdout)
                if result.value and result.value != '()':
                    return '\n'.join([out, result.value])
                return out
            if result.value and not cls._is_function_value(result.value):
                return result.value
            return cls.show_type(result)
        return result.value

    @classmethod
    def show_type(cls, result):
        """
        :param TryHaskell.Result result: Parse result of JSON data.
        :rtype: str|unicode
        """
        if result.ok:
            return ' :: '.join([result.expr, result.type])
        return result.value

    @classmethod
    def repl(cls):
        # We have to do this for the λ prompt; and yes, it's worth it.
        reload(sys)
        # noinspection PyUnresolvedReferences
        sys.setdefaultencoding('utf-8')
        # Start the repl.
        Repl().cmdloop()

    @classmethod
    def _is_function_value(cls, value, regex=re.compile(r'^.*<.*->.*>.*$')):
        return regex.match(value)


class Repl(cmd.Cmd):
    prompt = 'λ '

    def __init__(self, *args, **kwargs):
        cmd.Cmd.__init__(self, *args, **kwargs)
        self.file_state = TryHaskell.get('()').files

    def default(self, line):
        if line.startswith(':t'):
            print(TryHaskell.show_type(TryHaskell.get(line[2:].strip())))
        else:
            result = TryHaskell.get(line, files=self.file_state)
            self.file_state = result.files
            print(TryHaskell.show(result))

    def cmdloop(self, intro=None):
        try:
            cmd.Cmd.cmdloop(self, intro)
        except KeyboardInterrupt:
            print('^C')
            print('(Type exit or press Ctrl+D to exit.)')
            self.cmdloop(intro)

    @staticmethod
    def do_exit(_):
        return True

    @staticmethod
    def do_quit(_):
        return True

    # noinspection PyPep8Naming
    @staticmethod
    def do_EOF(_):
        print()
        return True


if __name__ == '__main__':
    TryHaskell.repl()
