from playwright.sync_api import Page
from utils.read_config import AppConfiguration
import re

class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        config = AppConfiguration.get_app_configuration()
        self.default_navigation_timeout = int(config["DefaultNavigationTimeout"])
        self.default_timeout = int(config["DefaultTimeout"])

    def add_to_cart(self, item_test_id: str):
        self.page.wait_for_selector(f'button[data-test="add-to-cart-{item_test_id}"]', timeout=self.default_timeout, state='visible')
        self.page.click(f'button[data-test="add-to-cart-{item_test_id}"]')

    def remove_from_cart(self, item_test_id: str):
        self.page.wait_for_selector(f'button[data-test="remove-{item_test_id}"]', timeout=self.default_timeout, state='visible')
        self.page.click(f'button[data-test="remove-{item_test_id}"]')

    def open_cart(self):
        self.page.wait_for_selector('.shopping_cart_link', timeout=self.default_timeout, state='visible')
        self.page.click('.shopping_cart_link')

    def get_title(self):
        return self.page.locator('.title')

    def select_option(self,sort_option: str):
        sort_selection = self.page.locator('//select[@data-test="product-sort-container"]')
        sort_selection.click()
        self.page.locator('//select[@data-test="product-sort-container"]').select_option(sort_option)
        self.page.wait_for_selector('.inventory_item', state='visible', timeout=self.default_timeout)

    def assert_first_item(self, name):
        first_item = self.page.locator('.inventory_item').first
        assert name in first_item.inner_text()

    def assert_number_on_badge(self, expected_count: int):
        badge = self.page.locator('.shopping_cart_badge')
        if expected_count > 0:
            assert badge.is_visible(), "Cart badge should be visible"
            assert badge.inner_text() == str(expected_count), f"Expected {expected_count} items in cart, found {badge.inner_text()}"
        else:
            assert not badge.is_visible(), "Cart badge should not be visible when cart is empty"

    def check_images_unique(self):
        """Check that every product image on the inventory page is unique"""
        image_srcs = self.page.eval_on_selector_all(
            '.inventory_item_img img',
            'nodes => nodes.map(n => n.src)'
        )
        assert len(image_srcs) == len(set(image_srcs)), "Not all product images are unique!"

    def assert_product_names_and_descriptions_no_invalid_symbols(self):
        """E2E: Ensure product names and descriptions do not contain invalid symbols like 'text.text()'"""
        names = self.page.eval_on_selector_all('.inventory_item_name', 'nodes => nodes.map(n => n.textContent)')
        descriptions = self.page.eval_on_selector_all('.inventory_item_desc', 'nodes => nodes.map(n => n.textContent)')

        # Define a regex for allowed characters (alphanumeric, space, basic punctuation)
        allowed_pattern = re.compile(r"\.[a-zA-Z()]+")
        
        for name in names:
            assert allowed_pattern.match(name.strip()), f"Invalid symbol found in product name: {name!r}"
        
        for description in descriptions:
            assert allowed_pattern.match(description.strip()), f"Invalid symbol found in product description: {description!r}"

    def expect_title_contains_text(self, text: str):
        """Assert that the page title contains the specified text."""
        self.page.wait_for_selector('.title', timeout=self.default_timeout)
        title = self.page.locator('.title').text_content()
        assert text in title, f"Expected title to contain '{text}', but got '{title}'"