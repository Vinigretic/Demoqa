import random
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_objects.base_page import BasePage


class BrowserWindowsPage(BasePage):
    BrowserWindowsButton = (By.XPATH, "//span[contains(text(), 'Browser Windows')]")
    NewTabButton = (By.ID, "tabButton")
    NewWindowButton = (By.ID, "windowButton")
    NewWindowMessageButton = (By.ID, "messageWindowButton")
    SamplePageTitle = (By.ID, "sampleHeading")

    def go_to_browser_windows_page(self):
        self.element_is_clickable(self.BrowserWindowsButton).click()

    def check_open_new_tab_or_window(self, locator):
        self.element_is_clickable(locator).click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        sample_page_url = self.driver.current_url
        sample_page_title = self.element_is_presence(self.SamplePageTitle).text
        return sample_page_url, sample_page_title


class AlertsPage(BasePage):
    AlertsButton = (By.XPATH, "//span[contains(text(), 'Alerts')]")
    AlertButton = (By.ID, "alertButton")
    TimerAlertButton = (By.ID, "timerAlertButton")
    ConfirmButton = (By.ID, "confirmButton")
    PromtButton = (By.ID, "promtButton")
    ConfirmResult = (By.ID, "confirmResult")
    PromptResult = (By.ID, "promptResult")

    def go_to_alerts_page(self):
        self.element_is_clickable(self.AlertsButton).click()

    def check_alert_button(self):
        self.element_is_clickable(self.AlertButton).click()
        alert = self.driver.switch_to.alert
        return alert.text

    def check_timer_alert_button(self, timeout=5):
        self.safe_click(self.TimerAlertButton)
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            return alert.text
        except TimeoutException:
            return None

    def check_confirm_button(self, command):
        self.safe_click(self.ConfirmButton)
        alert = self.driver.switch_to.alert
        if command == 'accept':
            alert.accept()
        elif command == 'dismiss':
            alert.dismiss()
        else:
            raise ValueError(f"Unknown command: {command}")

        return self.element_is_presence(self.ConfirmResult).text

    def check_promt_button(self):
        self.safe_click(self.PromtButton)
        alert = self.driver.switch_to.alert
        text = f"test{random.randint(0, 999)}"
        alert.send_keys(text)
        alert.accept()
        result_message = self.element_is_presence(self.PromptResult).text
        return result_message, text
