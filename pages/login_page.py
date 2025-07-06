from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def login(self, username: str, password: str):
        self.page.fill('input[data-test="username"]', username)
        self.page.fill('input[data-test="password"]', password)
        self.page.click('input[data-test="login-button"]')

    def get_error(self):
        return self.page.locator('[data-test="error"]')

    def expect_logged_out(self):
        assert self.page.locator('input[data-test="username"]').is_visible(), "Username field is not visible, user might still be logged in"
        assert self.page.locator('input[data-test="password"]').is_visible(), "Password field is not visible, user might still be logged in"

    def expect_login_error(self, message):
        error_locator = self.page.locator('[data-test="error"]')
        assert error_locator.is_visible(), "Error message is not visible"
        assert error_locator.inner_text() == message, f"Expected error message '{message}', but got '{error_locator.inner_text()}'"
        