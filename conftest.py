import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()