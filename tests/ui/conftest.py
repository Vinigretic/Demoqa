import shutil
import tempfile
from typing import Any

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from generator.forms_generator import full_student_form_fields
from generator.upload_download_generator import FileFactory
from utils.allure_utils import attach_file_as_text
from utils.logger import ui_logger
from utils.test_handlers import create_chrome_driver


@pytest.fixture(scope="function")
def driver() -> webdriver.Chrome:
    """Provide a Chrome WebDriver instance for UI tests."""
    options = Options()
    # options.add_argument("--headless=new")  # enable if headless mode is needed
    browser = create_chrome_driver(options)
    yield browser
    browser.quit()


@pytest.fixture(scope="function")
def driver_for_download_file() -> tuple[webdriver.Chrome, str]:
    """Provide a Chrome WebDriver with a temporary download directory."""
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
    browser = create_chrome_driver(options)
    yield browser, download_dir
    browser.quit()
    shutil.rmtree(
        download_dir)  # standard python module for working with files and directories, rmtree, deletes the entire folder structure.


@pytest.fixture
def student_person() -> Any:
    """Provide a generated student form data object."""
    person = full_student_form_fields()
    yield person
    person.delete_file(person.picture)


@pytest.fixture
def temp_file(request) -> tuple[str, str]:
    """Provide a temporary file created by FileFactory based on param method name."""
    method_name = request.param
    create_method = getattr(FileFactory, request.param)
    file_name = create_method()
    yield file_name, method_name
    FileFactory.delete_file(file_name)


@pytest.fixture(autouse=True)
def attach_ui_logs(request) -> None:
    """Attach per-test UI logs to Allure report."""
    log_file = f"logs/{request.node.name}_ui.log"  # only logs of a specific test
    handler_id = ui_logger.add(log_file, level="INFO")
    yield
    ui_logger.remove(handler_id)
    attach_file_as_text(log_file)
