import requests
import json
from bs4 import BeautifulSoup
from omega_wp.config import DEFAULT_HEADERS


class LoginService:
    def __init__(self, wp_url: str):
        self.wp_url = wp_url
    
    def is_xmlrpc_enabled(self):
        response = requests.post(f'{self.wp_url}/xmlrpc.php', headers=DEFAULT_HEADERS)

        return response.ok

    def check_admin_login(self, username: str, password: str):
        payload = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<methodCall> '
            f'<methodName>wp.getUsersBlogs</methodName>'
            f'<params>'
            f'<param><value>{username}</value></param>'
            f'<param><value>{password}</value></param>'
            f'</params>'
            f'</methodCall>'
        )
        login_error_str = 'Incorrect username or password.'

        # Check login is correct
        response = requests.post(f'{self.wp_url}/xmlrpc.php', data=payload, headers=DEFAULT_HEADERS)
        if (login_error_str in response.text):
            raise Exception('Wrong credentials')

        # Check if the user is admin
        soup = BeautifulSoup(response.text, 'xml')
        response_text = json.loads(
            str(soup.findAll(text=True)).replace('\\n', '').replace("'", '"'))
        is_admin = response_text[response_text.index('isAdmin') + 1] == '1'

        if(not is_admin):
            raise Exception('User is not admin')

    def get_wp_admin_session(self, username: str, password: str) -> requests.Session:
        login_data = {
            'log': username,
            'pwd': password,
            'rememberme': 'forever',
            'redirect_to': f'{self.wp_url}/wp-admin',
            'redirect_to_automatic': '1'
        }
        wp_admin_session = requests.Session()
        response = wp_admin_session.post(f'{self.wp_url}/wp-login.php', data=login_data, headers=DEFAULT_HEADERS)

        if(not response.ok or 'login_error' in response.text):
            raise Exception('Error  trying to login')

        return wp_admin_session
