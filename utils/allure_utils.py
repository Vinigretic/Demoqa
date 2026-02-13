import json
import os
from datetime import datetime
from typing import Optional  # Optional[X] — Union[X, None]

import allure
from selenium.webdriver.remote.webdriver import WebDriver


def safe_attach(data: str | bytes, name: str, attachment_type) -> None:
    """Safely attach any artifact to Allure report."""
    try:
        allure.attach(data, name=name, attachment_type=attachment_type)
    except Exception:
        pass


def attach_screenshot(driver: WebDriver, name: str = "Screenshot") -> None:
    """Attach screenshot to Allure report."""
    try:
        screenshot = driver.get_screenshot_as_png()
        safe_attach(screenshot, f"{name} {datetime.today()}", allure.attachment_type.PNG)
    except Exception:
        pass


def attach_page_source(driver: WebDriver, name: str = "Page Source") -> None:
    """Attach Page Source to Allure report."""
    # the current page's HTML source
    try:
        safe_attach(driver.page_source, name, allure.attachment_type.TEXT)
    except Exception:
        pass


def attach_browser_logs(driver: WebDriver, name: str = "Browser logs") -> None:
    """Attach Browser logs to Allure report."""
    try:
        logs = driver.get_log("browser")
        safe_attach(json.dumps(logs, indent=2), name, allure.attachment_type.JSON)
    except Exception:
        pass


def attach_url(driver: WebDriver, name: str = "Current URL") -> None:
    """Attach Current URL to Allure report."""
    try:
        safe_attach(driver.current_url, name, allure.attachment_type.TEXT)
    except Exception:
        pass


def attach_setup_fail_artifacts(driver: WebDriver) -> None:
    """Attach artifacts when test fails during setup phase."""
    with allure.step("Attach artifacts on FAIL (setup)"):
        attach_url(driver, "URL (setup FAIL)")
        attach_screenshot(driver, "Screenshot (setup FAIL)")
        attach_browser_logs(driver, "Browser logs (setup FAIL)")


def attach_call_fail_artifacts(driver: WebDriver, when: str, download_dir: Optional[str] = None) -> None:
    """Attach artifacts when test fails during execution phase."""
    with allure.step(f"Attach artifacts on FAIL ({when})"):
        attach_url(driver, "Final URL")
        attach_screenshot(driver, f"Screenshot on FAIL ({when})")
        attach_page_source(driver, f"Page Source on FAIL ({when})")
        attach_browser_logs(driver, f"Browser logs on FAIL ({when})")

    attach_downloaded_files(download_dir)


def attach_downloaded_files(download_dir: Optional[str] = None) -> None:
    """Attach information about downloaded files if present."""
    if download_dir and os.path.exists(download_dir):
        try:
            files = os.listdir(download_dir)  # return only list names of files
            if files:
                safe_attach("\n".join(files),
                            "Downloaded files",
                            attachment_type=allure.attachment_type.TEXT)
            else:
                safe_attach("No files downloaded",
                            "Download Status",
                            attachment_type=allure.attachment_type.TEXT)
        except OSError as e:
            safe_attach(f"Failed to list downloads: {e}",
                        "Download Error",
                        attachment_type=allure.attachment_type.TEXT)


def attach_call_pass_artifacts(driver: WebDriver, when: str) -> None:
    """Attach minimal artifacts when test passes."""
    with allure.step(f"Attach artifacts on PASS ({when})"):
        attach_url(driver, "Final URL")


def attach_file_as_text(log_file: str) -> None:
    """Reads the file and attaches it to Allure as text, then deletes the file"""
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    safe_attach(content, name="UI test log", attachment_type=allure.attachment_type.TEXT)
        finally:
            os.remove(log_file)
