import unittest, sys
from argparse import Namespace
from io import StringIO
from omega_wp.services import ParametersParserService


class ParametersParserServiceTest(unittest.TestCase):
    def test_no_arguments_parse(self):
        sys.argv = ['./omega.py']
        parameterParserService = ParametersParserService()

        with unittest.mock.patch('sys.stderr', new=StringIO()) as fakeOutput:
            try:
                parameterParserService.parse_params()
            except SystemExit:
                self.assertTrue('error: the following arguments are required: -u/--wp-url, -l/--username, -p/--password, -H/--lhost' in fakeOutput.getvalue().strip())
    
    def test_arguments_parse(self):
        sys.argv = ['./omega.py', '-u', 'http://example', '-l', 'user', '-p', 'password', '--lhost', '127.0.0.1', '--lport', '8000']
        parameterParserService = ParametersParserService()

        with unittest.mock.patch('sys.stderr', new=StringIO()):
            try:
                params = parameterParserService.parse_params()
                self.assertEqual(params, Namespace(lhost='127.0.0.1', lport=8000, no_pty=False, password='password', username='user', wp_url='http://example'))
            except SystemExit:
                raise Exception('Wrong parameters!')
    
    def test_arguments_parse_default_port(self):
        sys.argv = ['./omega.py', '-u', 'http://example', '-l', 'user', '-p', 'password', '--lhost', '127.0.0.1']
        parameterParserService = ParametersParserService()

        with unittest.mock.patch('sys.stderr', new=StringIO()):
            try:
                params = parameterParserService.parse_params()
                self.assertEqual(params, Namespace(lhost='127.0.0.1', lport=8080, no_pty=False, password='password', username='user', wp_url='http://example'))
            except SystemExit:
                raise Exception('Wrong parameters!')
    
    def test_arguments_parse_error(self):
        sys.argv = ['./omega.py', '-u', 'http://example', '-l', 'user', '-p', 'password', '--lhost']
        parameterParserService = ParametersParserService()

        with unittest.mock.patch('sys.stderr', new=StringIO()) as fakeOutput:
            try:
                parameterParserService.parse_params()
            except SystemExit:
                self.assertTrue('error: argument -H/--lhost: expected one argument' in fakeOutput.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
