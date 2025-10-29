import shutil
import tempfile

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("--headless=new")
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope="function")
def driver_for_download_file():
    # Create a temporary download folder
    download_dir = tempfile.mkdtemp()
    # C:\Users\vbaka\AppData\Local\Temp\tmpd2q8c5gr

    options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    # options.add_argument("--headless=new")
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    browser.maximize_window()
    yield browser, download_dir
    browser.quit()
    shutil.rmtree(download_dir) # standard python module for working with files and directories, rmtree, deletes the entire folder structure.





