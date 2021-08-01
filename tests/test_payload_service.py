import unittest, responses, requests
from omega_wp.services import PayloadService
from tests import mocks


class PayloadServiceTest(unittest.TestCase):
    wp_url = 'http://fancy-wordpress-site.com'
    
    @responses.activate
    def test_get_theme_name(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.wp_url}/wp-admin/themes.php',
            'status'         : 200,
            'body'           : mocks.wordpress_themes_response
        })
        
        payload_service = PayloadService(self.wp_url, requests.Session())
        self.assertEqual(payload_service.get_theme_name(), 'twentytwentyone')
    
    @responses.activate
    def test_get_theme_name_error(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.wp_url}/wp-admin/themes.php',
            'status'         : 403
        })
        
        payload_service = PayloadService(self.wp_url, requests.Session())
        self.assertRaises(Exception, payload_service.get_theme_name, 'twentytwentyone')
    
    @responses.activate
    def test_get_theme_404_template_form_data(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.wp_url}/wp-admin/theme-editor.php?file=404.php&theme=twentytwentyone',
            'status'         : 200,
            'body'           : mocks.wordpress_theme_editor_response
        })
        
        payload_service = PayloadService(self.wp_url, requests.Session())
        form_data = payload_service.get_theme_404_template_form_data('twentytwentyone')
        self.assertTrue(type(form_data) is dict)
    
    @responses.activate
    def test_get_theme_404_template_form_data_error(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.wp_url}/wp-admin/theme-editor.php?file=404.php&theme=twentytwentyone',
            'status'         : 403
        })
        
        payload_service = PayloadService(self.wp_url, requests.Session())
        self.assertRaises(Exception, payload_service.get_theme_404_template_form_data, 'twentytwentyone')
    
    def test_is_payload_already_dropped(self):
        payload_service = PayloadService(self.wp_url, requests.Session())
        self.assertTrue(payload_service.is_payload_already_dropped(payload_service.payload))
    
    def test_is_not_payload_already_dropped(self):
        payload_service = PayloadService(self.wp_url, requests.Session())
        self.assertFalse(payload_service.is_payload_already_dropped('123123123'))
    
    @responses.activate
    def test_drop_payload(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.wp_url}/wp-admin/themes.php',
            'status'         : 200,
            'body'           : mocks.wordpress_themes_response
        })
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.wp_url}/wp-admin/theme-editor.php?file=404.php&theme=twentytwentyone',
            'status'         : 200,
            'body'           : mocks.wordpress_theme_editor_response
        })
        responses.add(**{
            'method'         : responses.POST,
            'url'            : f'{self.wp_url}/wp-admin/theme-editor.php',
            'status'         : 200
        })

        payload_service = PayloadService(self.wp_url, requests.Session())
        result = payload_service.drop_payload()
        self.assertEqual(result, 'http://fancy-wordpress-site.com/wp-content/themes/twentytwentyone/404.php')
    
    @responses.activate
    def test_drop_payload_error(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.wp_url}/wp-admin/themes.php',
            'status'         : 200,
            'body'           : mocks.wordpress_themes_response
        })
        responses.add(**{
            'method'         : responses.GET,
            'url'            : f'{self.wp_url}/wp-admin/theme-editor.php?file=404.php&theme=twentytwentyone',
            'status'         : 200,
            'body'           : mocks.wordpress_theme_editor_response
        })
        responses.add(**{
            'method'         : responses.POST,
            'url'            : f'{self.wp_url}/wp-admin/theme-editor.php',
            'status'         : 403
        })

        payload_service = PayloadService(self.wp_url, requests.Session())
        self.assertRaises(Exception, payload_service.drop_payload)

if __name__ == '__main__':
    unittest.main()
