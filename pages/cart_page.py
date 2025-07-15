from playwright.sync_api import Page
from utils.read_config import AppConfiguration
from PIL import Image, ImageChops
import os

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        config = AppConfiguration.get_app_configuration()
        self.default_navigation_timeout = int(config["DefaultNavigationTimeout"])
        self.default_timeout = int(config["DefaultTimeout"])

    def checkout(self):
        self.page.click('button[data-test="checkout"]', timeout=self.default_timeout)

    def remove_item(self, item_test_id: str):
        self.page.click(f'button[data-test="remove-{item_test_id}"]', timeout=self.default_timeout)

    def is_cart_empty(self):
        return self.page.locator('.cart_item').count() == 0
    
    def click_continue_shopping(self):
        self.page.click('button[data-test="continue-shopping"]', timeout=self.default_timeout)
        assert 'inventory.html' in self.page.url

    def assert_cart_is_empty(self):
        assert self.is_cart_empty(), "Actual result: Cart is not empty, items are still present.\nExpected result: Cart should be empty."

    def check_page_image(self, threshold: int = 10) -> bool:
        # Save current screenshot
        current_path = f"tests/tmp/current_cart_page.png"

        os.makedirs(os.path.dirname(current_path), exist_ok=True)
        self.page.screenshot(path=current_path, full_page=True)

        # Path to expected image
        expected_path = f"tests/tmp/cart_page_expected.png"

        # Load images
        img1 = Image.open(expected_path).convert("RGB")
        img2 = Image.open(current_path).convert("RGB")

        # Find the difference
        diff = ImageChops.difference(img1, img2)

        # If there are no differences, diff.getbbox() will be None
        if diff.getbbox() is None:
            assert False, "Actual result: No differences found, but expected some.\nExpected result: Differences should be present in the cart page image."

        # Analysis: can be extended
        diff_hist = diff.histogram()
        diff_score = sum(diff_hist)

        assert diff_score < threshold, f"Actual result: {diff_score}\nExpected result: < {threshold}"


