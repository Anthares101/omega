import argparse
from omega_wp.config import VERSION


class ParametersParserService:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description='Provides a reverse shell (stabilized if possible) to a Wordpress host. You need admin credentials!')
		self.parser.add_argument('-v', '--version', action='version', version='%(prog)s version ' + VERSION)
		self.parser.add_argument('--no-pty', action='store_true', help='if this flag is set, no shell stabilization is perform')
		self.parser.add_argument('-u', '--wp-url', type=str, help='the target Wordpress url', required=True)
		self.parser.add_argument('-l', '--username', type=str, help='Wordpress admin user to use for login', required=True)
		self.parser.add_argument('-p', '--password', type=str, help='Wordpress admin password to use for login', required=True)
		self.parser.add_argument('-H', '--lhost', type=str, help='the ip where the reverse shell should connect to', required=True)
		self.parser.add_argument('-P', '--lport', type=int, help='the port used to listen for the reverse shell (Default: 8080)', default=8080)

	def parse_params(self) -> argparse.Namespace:
		return self.parser.parse_args()
