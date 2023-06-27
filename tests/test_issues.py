""" Tests in this file all relate to specific issues listed at
    https://github.com/bw2/ConfigArgParse/issues/275

    No fixes without a test case!
"""
import os, sys, re
from unittest.mock import patch

import configargparse

from tests.test_base import TestCase

class TestMisc(TestCase):

    def test_issue_275(self):
        """Including -- to end processing of named args does not work as
           advertised.
        """

        p = configargparse.ArgParser()

        p.add('--foo', '-f', nargs='?', env_var='FOO', required=False)
        p.add('bar', nargs='*')

        options = p.parse_args( args = ['--', 'arg1', 'arg2'],
                                env_vars = dict(FOO = 'environ_value')  )

        self.assertEqual(vars(options), dict( foo = 'environ_value',
                                              bar = ['arg1', 'arg2'] ))
