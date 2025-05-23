import pytest
from utils.logger import logger


@pytest.mark.usefixtures("setup")
class BaseTest:
    pass