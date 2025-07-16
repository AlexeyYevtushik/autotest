from playwright.sync_api import Page
from utils.read_config import AppConfiguration
from PIL import Image, ImageChops
import os

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        config = AppConfiguration.get_app_configuration()
        self.default_navigation_timeout = int(config["DefaultNavigationTimeout"])
        self.default_timeout = int(config["DefaultTimeout"])

    def check_page_image(self, current_path: str, expected_path: str, threshold: int = 10) -> bool:
        # Save current screenshot
        os.makedirs(os.path.dirname(current_path), exist_ok=True)
        self.page.screenshot(path=current_path, full_page=True)

        # Load images
        img1 = Image.open(expected_path).convert("RGB")
        img2 = Image.open(current_path).convert("RGB")

        # Find the difference
        diff = ImageChops.difference(img1, img2)

        # If there are no differences, diff.getbbox() will be None
        if diff.getbbox() is None:
            assert False, "Actual result: No differences found, but expected some.\nExpected result: Differences should be present in the page image."

        # Analysis: can be extended
        diff_hist = diff.histogram()
        diff_score = sum(diff_hist)

        assert diff_score < threshold, f"Actual result: {diff_score}\nExpected result: < {threshold}"