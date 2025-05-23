from pages.main_google_page import MainGooglePage
from tests.test_base import BaseTest
from utils.read_config import AppConfiguration
from playwright.sync_api import expect
from utils.logger import logger

    
class TestGoogle(BaseTest):

    configuration = AppConfiguration.get_common_info()

    def test_run_google(self):
        self.page.goto(self.configuration["Url"])
        google_page = MainGooglePage(self.page)
        google_page.click_accept_all_cookies()
