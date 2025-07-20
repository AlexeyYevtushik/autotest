from playwright.sync_api import Page
from utils.read_config import AppConfiguration
import re
from playwright.sync_api import expect
from pages.base_page import BasePage

class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        config = AppConfiguration.get_app_configuration()
        self.default_navigation_timeout = int(config["DefaultNavigationTimeout"])
        self.default_timeout = int(config["DefaultTimeout"])

    def add_to_cart(self, item_test_id: str):
        self.page.wait_for_selector(f'button[data-test="add-to-cart-{item_test_id}"]', timeout=self.default_timeout)
        self.page.click(f'button[data-test="add-to-cart-{item_test_id}"]')

    def remove_from_cart(self, item_test_id: str):
        self.page.wait_for_selector(f'button[data-test="remove-{item_test_id}"]', timeout=self.default_timeout)
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
        assert name in first_item.inner_text(), "Actual result: First item name does not match\nExpected result: First item name should match"

    def assert_number_on_badge(self, expected_count: int):
        badge = self.page.locator('.shopping_cart_badge')
        if expected_count > 0:
            assert badge.inner_text() == str(expected_count), f"Actual result: Expected {expected_count} items in cart, found {badge.inner_text()}\nExpected result: {expected_count} items in cart"
        else:
            assert not badge.is_visible(), "Actual result: Cart badge should not be visible when cart is empty\nExpected result: Cart badge should not be visible when cart is empty"
    
    def check_images_unique(self):
        """Check that every product image on the inventory page is unique"""
        image_srcs = self.page.eval_on_selector_all(
            '.inventory_item_img img',
            'nodes => nodes.map(n => n.src)'
        )
        assert len(image_srcs) == len(set(image_srcs)), "Actual result: Not all product images are unique\nExpected result: All product images should be unique"

    def assert_product_names_have_no_invalid_symbols(self):
        """E2E: Ensure product names do not contain invalid symbols like 'text.text()'"""
        names = self.page.eval_on_selector_all('.inventory_item_name', 'nodes => nodes.map(n => n.textContent)')
        
        # Define a regex for allowed characters (alphanumeric, space, basic punctuation)
        allowed_pattern = re.compile(r"\.[a-zA-Z()]+")
        
        for name in names:
            assert allowed_pattern.match(name.strip()), f"Actual result: Invalid symbol found in product name: {name!r}\nExpected result: Valid product name"

    def assert_product_descriptions_have_no_invalid_symbols(self):
        """E2E: Ensure product descriptions do not contain invalid symbols like 'text.text()'"""
        descriptions = self.page.eval_on_selector_all('.inventory_item_desc', 'nodes => nodes.map(n => n.textContent)')

        # Define a regex for allowed characters (alphanumeric, space, basic punctuation)
        allowed_pattern = re.compile(r"\.[a-zA-Z()]+")
        
        for description in descriptions:
            assert allowed_pattern.match(description.strip()), f"Actual result: Invalid symbol found in product description: {description!r}\nExpected result: Valid product description"

    def expect_title_contains_text(self, text: str):
        """Assert that the page title contains the specified text."""
        self.page.wait_for_selector('.title', timeout=self.default_timeout)
        title = self.page.locator('.title').text_content()
        assert text in title, f"Expected title to contain '{text}', but got '{title}'"

    def click_facebook_button(self):
        """Click the Facebook button in the footer, verify the new tab URL, and close it."""
        with self.page.expect_popup() as popup_info:
            self.page.wait_for_selector('a[data-test="social-facebook"]', timeout=self.default_timeout)
            self.page.click('a[data-test="social-facebook"]')
    
        facebook_page = popup_info.value
        facebook_page.wait_for_load_state('load', timeout=self.default_navigation_timeout)

        assert 'facebook.com' in facebook_page.url, f"Actual result: Expected Facebook URL, got: {facebook_page.url}\nExpected result: Facebook URL"

        facebook_page.close()

    def click_linkedin_button(self):
        """Click the LinkedIn button in the footer."""
        with self.page.expect_popup() as popup_info:
            self.page.wait_for_selector('a[data-test="social-linkedin"]', timeout=self.default_timeout)
            self.page.click('a[data-test="social-linkedin"]')
        linkedin_page = popup_info.value
        linkedin_page.wait_for_load_state('load', timeout=self.default_navigation_timeout)
        assert 'linkedin.com' in linkedin_page.url, f"Actual result: Expected LinkedIn URL, got: {linkedin_page.url}\nExpected result: LinkedIn URL"
        linkedin_page.close()

    def click_x_button(self):
        """Click the X button in the footer."""

        with self.page.expect_popup() as popup_info:
            self.page.wait_for_selector('a[data-test="social-twitter"]', timeout=self.default_timeout)
            self.page.click('a[data-test="social-twitter"]')
        twitter_page = popup_info.value
        twitter_page.wait_for_load_state('load', timeout=self.default_navigation_timeout)
        assert 'x.com' in twitter_page.url, f"Actual result: Expected Twitter URL, got: {twitter_page.url}\nExpected result: Twitter URL"
        twitter_page.close()


    def check_page_image(self, page_name: str = "products", threshold: int = 10) -> bool:
        base_page = BasePage(self.page)
        base_page.check_page_image(f"tests/tmp/current_{page_name}_page.png", f"tests/tmp/{page_name}_page_expected.png", threshold)