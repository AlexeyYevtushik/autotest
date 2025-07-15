from playwright.sync_api import Page, expect
from utils.read_config import AppConfiguration
from PIL import Image, ImageChops
import os

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        config = AppConfiguration.get_app_configuration()
        self.default_navigation_timeout = int(config["DefaultNavigationTimeout"])
        self.default_timeout = int(config["DefaultTimeout"])

    def login(self, username: str, password: str):
        self.page.fill('input[data-test="username"]', username, timeout=self.default_timeout)
        self.page.fill('input[data-test="password"]', password, timeout=self.default_timeout)
        self.page.click('input[data-test="login-button"]', timeout=self.default_timeout)

    def get_error(self):
        return self.page.locator('[data-test="error"]')

    def expect_logged_out(self):
        assert self.page.locator('input[data-test="username"]').is_visible(), "Actual result: Username field is not visible, user might still be logged in\nExpected result: Username field is visible"
        assert self.page.locator('input[data-test="password"]').is_visible(), "Actual result: Password field is not visible, user might still be logged in\nExpected result: Password field is visible"

    def expect_login_error(self, message):
        error_locator = self.page.locator('[data-test="error"]')
        assert error_locator.is_visible(), "Actual result: Error message is not visible\nExpected result: Error message should be visible"
        assert error_locator.inner_text() == message, f"Actual result: Expected error message '{message}', but got '{error_locator.inner_text()}'\nExpected result: Error message should match"

    def check_page_image(self, threshold: int = 10) -> bool:
        # Save current screenshot
        current_path = f"tests/tmp/current_login_page.png"

        os.makedirs(os.path.dirname(current_path), exist_ok=True)
        self.page.screenshot(path=current_path, full_page=True)

        # Path to expected image
        expected_path = f"tests/tmp/login_page_expected.png"

        # Load images
        img1 = Image.open(expected_path).convert("RGB")
        img2 = Image.open(current_path).convert("RGB")

        # Find the difference
        diff = ImageChops.difference(img1, img2)

        # If there are no differences, diff.getbbox() will be None
        if diff.getbbox() is None:
            assert False, "Actual result: No differences found, but expected some.\nExpected result: Differences should be present in the login page image."

        # Analysis: can be extended
        diff_hist = diff.histogram()
        diff_score = sum(diff_hist)

        assert diff_score < threshold, f"Actual result: {diff_score}\nExpected result: < {threshold}"


