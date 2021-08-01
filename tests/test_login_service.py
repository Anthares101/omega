import unittest, responses, requests
from tests import mocks
from omega_wp.services import LoginService


class LoginServiceTest(unittest.TestCase):
    wp_url = 'http://fancy-wordpress-site.com'

    @responses.activate
    def test_xmlrpc_is_active(self):
        responses.add(**{
            'method'         : responses.POST,
            'url'            : f'{self.wp_url}/xmlrpc.php',
            'status'         : 200
        })

        login_service = LoginService(self.wp_url)
        result = login_service.is_xmlrpc_enabled()

        self.assertTrue(result)
    
    @responses.activate
    def test_xmlrpc_is_disabled(self):
        responses.add(**{
            'method'         : responses.POST,
            'url'            : f'{self.wp_url}/xmlrpc.php',
            'status'         : 404
        })

        login_service = LoginService(self.wp_url)
        result = login_service.is_xmlrpc_enabled()

        self.assertFalse(result)
    
    @responses.activate
    def test_check_admin_login_success(self):
        responses.add(**{
            'method'         : responses.POST,
            'url'            : f'{self.wp_url}/xmlrpc.php',
            'status'         : 200,
            'body'           : mocks.xmlrpc_right_admin_credentials_response
        })

        login_service = LoginService(self.wp_url)
        login_service.check_admin_login('user', 'password')
    
    @responses.activate
    def test_check_admin_login_success_not_admin(self):
        responses.add(**{
            'method'         : responses.POST,
            'url'            : f'{self.wp_url}/xmlrpc.php',
            'status'         : 200,
            'body'           : mocks.xmlrpc_right_not_admin_credentials_response
        })

        login_service = LoginService(self.wp_url)
        self.assertRaises(Exception, login_service.check_admin_login, 'user', 'password')
    
    @responses.activate
    def test_check_admin_login_error(self):
        responses.add(**{
            'method'         : responses.POST,
            'url'            : f'{self.wp_url}/xmlrpc.php',
            'status'         : 200,
            'body'           : mocks.xmlrpc_wrong_credentials_response
        })

        login_service = LoginService(self.wp_url)
        self.assertRaises(Exception, login_service.check_admin_login, 'user', 'password')
    
    @responses.activate
    def test_get_wp_admin_session(self):
        responses.add(**{
            'method'         : responses.POST,
            'url'            : f'{self.wp_url}/wp-login.php',
            'status'         : 200
        })

        login_service = LoginService(self.wp_url)
        session = login_service.get_wp_admin_session('user', 'password')

        self.assertTrue(type(session) is requests.Session)


if __name__ == '__main__':
    unittest.main()
