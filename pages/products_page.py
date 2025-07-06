from playwright.sync_api import Page

class ProductsPage:
    def __init__(self, page: Page):
        self.page = page

    def add_to_cart(self, item_test_id: str):
        self.page.wait_for_selector(f'button[data-test="add-to-cart-{item_test_id}"]', timeout=10000, state='visible')
        self.page.click(f'button[data-test="add-to-cart-{item_test_id}"]')

    def remove_from_cart(self, item_test_id: str):
        self.page.wait_for_selector(f'button[data-test="remove-{item_test_id}"]', timeout=10000, state='visible')
        self.page.click(f'button[data-test="remove-{item_test_id}"]')

    def open_cart(self):
        self.page.wait_for_selector('.shopping_cart_link', timeout=10000, state='visible')
        self.page.click('.shopping_cart_link')

    def get_title(self):
        return self.page.locator('.title')

    def select_option(self,sort_option: str):
        sort_selection = self.page.locator('//select[@data-test="product-sort-container"]')
        sort_selection.click()
        self.page.locator('//select[@data-test="product-sort-container"]').select_option(sort_option)


