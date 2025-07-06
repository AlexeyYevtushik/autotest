from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        self.page.fill('input[data-test="firstName"]', first_name)
        self.page.fill('input[data-test="lastName"]', last_name)
        self.page.fill('input[data-test="postalCode"]', postal_code)
        self.page.click('input[data-test="continue"]')

    def finish(self):
        self.page.click('button[data-test="finish"]')

    def get_confirmation(self):
        return self.page.locator('.complete-header')

    def click_back_to_products(self):
        self.page.click('button[data-test="back-to-products"]')

    def click_cancel(self):
        self.page.click('button[data-test="cancel"]')
