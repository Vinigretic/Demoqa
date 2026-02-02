import json
from datetime import datetime

import allure


def safe_attach(data, name, attachment_type):
    """Safely attach any artifact to Allure report."""
    try:
        allure.attach(data, name=name, attachment_type=attachment_type)
    except Exception:
        pass


def attach_screenshot(driver, name="Screenshot"):
    try:
        screenshot = driver.get_screenshot_as_png()
        safe_attach(screenshot, f"{name} {datetime.today()}", allure.attachment_type.PNG)
    except Exception:
        pass


def attach_page_source(driver, name="Page Source"):
    # the current page's HTML source
    try:
        safe_attach(driver.page_source, name, allure.attachment_type.TEXT)
    except Exception:
        pass


def attach_browser_logs(driver, name="Browser logs"):
    try:
        logs = driver.get_log("browser")
        safe_attach(json.dumps(logs, indent=2), name, allure.attachment_type.JSON)
    except Exception:
        pass


def attach_url(driver, name="Current URL"):
    try:
        safe_attach(driver.current_url, name, allure.attachment_type.TEXT)
    except Exception:
        pass
