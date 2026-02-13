from typing import Any, Optional

from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from selenium.webdriver.remote.webdriver import WebDriver

from utils.allure_utils import (
    attach_setup_fail_artifacts,
    attach_call_fail_artifacts,
    attach_call_pass_artifacts,
)
from utils.logger import logger, ui_logger
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def handle_ui_test(item: Any, call: CallInfo[Any], result: TestReport) -> None:
    """Handle UI test reporting and artifact attachment."""
    driver: Optional[WebDriver] = None
    download_dir: Optional[str] = None

    if "driver" in item.funcargs:
        driver = item.funcargs["driver"]
    elif "driver_for_download_file" in item.funcargs:
        browser, download_dir = item.funcargs["driver_for_download_file"]
        driver = browser

    if result.when == "setup" and result.failed:
        ui_logger.error(f"UI Test {item.nodeid} FAILED during setup: {call.excinfo.value}\n {'*' * 150}")
        attach_setup_fail_artifacts(driver)

    elif result.when == "call" and result.failed:
        ui_logger.error(f"UI Test {item.nodeid} FAILED during call: {call.excinfo.value}\n {'*' * 150}")
        attach_call_fail_artifacts(driver, result.when, download_dir)

    elif result.when == "call" and result.passed:
        ui_logger.info(f"UI Test {item.nodeid} PASSED \n {'*' * 100}")
        attach_call_pass_artifacts(driver, result.when)


def handle_api_test(item: Any, call: CallInfo[Any], result: TestReport) -> None:
    """Handle API test reporting and artifact attachment."""
    pass


def handle_common_test(item: Any, call: CallInfo[Any], result: TestReport) -> None:
    """Handle common test reporting without UI or API fixtures."""
    if result.failed:
        logger.error(f"Test {item.nodeid} FAILED: {call.excinfo.value}\n {'*' * 150}")


def create_chrome_driver(options: Options) -> webdriver.Chrome:
    """Create and return a Chrome WebDriver instance with given options."""
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    browser.maximize_window()
    return browser
