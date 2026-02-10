import os
import shutil
import tempfile

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from generator.forms_generator import full_student_form_fields
from generator.upload_download_generator import FileFactory
from utils.allure_utils import attach_url, attach_screenshot, attach_page_source, attach_browser_logs


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
    shutil.rmtree(
        download_dir)  # standard python module for working with files and directories, rmtree, deletes the entire folder structure.


@pytest.fixture
def student_person():
    person = full_student_form_fields()
    yield person
    person.delete_file(person.picture)


@pytest.fixture
def temp_file(request):
    method_name = request.param
    create_method = getattr(FileFactory, request.param)
    file_name = create_method()
    yield file_name, method_name
    FileFactory.delete_file(file_name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    driver = None
    download_dir = None

    if "driver" in item.funcargs:
        driver = item.funcargs["driver"]
    elif "driver_for_download_file" in item.funcargs:
        browser, download_dir = item.funcargs["driver_for_download_file"]
        driver = browser

    if not driver:
        return

    # Attach only once per test phase to avoid duplicates (setup/call/teardown)
    if result.when == "setup" and result.failed:
        with allure.step("Attach artifacts on FAIL (setup)"):
            attach_url(driver, "URL (setup FAIL)")
            attach_screenshot(driver, "Screenshot (setup FAIL)")
            attach_browser_logs(driver, "Browser logs (setup FAIL)")
        return

    # On FAIL - full set of artifacts
    if result.when == "call" and result.failed:
        with allure.step(f"Attach artifacts on FAIL ({result.when})"):
            attach_url(driver, "Final URL")
            attach_screenshot(driver, f"Screenshot on FAIL ({result.when})")
            attach_page_source(driver, f"Page Source on FAIL ({result.when})")
            attach_browser_logs(driver, f"Browser logs on FAIL ({result.when})")

            if download_dir and os.path.exists(download_dir):
                try:
                    files = os.listdir(download_dir)
                    if files:
                        allure.attach("\n".join(files), "Downloaded files",
                                      attachment_type=allure.attachment_type.TEXT)
                    else:
                        allure.attach("No files downloaded", "Download Status",
                                      attachment_type=allure.attachment_type.TEXT)
                except OSError as e:
                    allure.attach(f"Failed to list downloads: {str(e)}",
                                  "Download Error",
                                  attachment_type=allure.attachment_type.TEXT)
        return

    # On PASS - light typing (e.g. URL only)
    if result.when == "call" and result.passed:
        with allure.step(f"Attach artifacts on PASS ({result.when})"):
            attach_url(driver, "Final URL")
