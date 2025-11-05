from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage


class MainPage(BasePage):
    Elements = (By.XPATH, "//div[contains(@class, 'card mt-4 top-card') and .//h5[contains(text(), 'Elements')]]")
    Forms = (By.XPATH, "//div[contains(@class, 'card mt-4 top-card') and .//h5[contains(text(), 'Forms')]]")
    AlertsFrameWindows = (By.XPATH,
                          "//div[contains(@class, 'card mt-4 top-card') and .//h5[contains(text(), 'Alerts, Frame & Windows')]]")
    Widgets = (By.XPATH, "//div[contains(@class, 'card mt-4 top-card') and .//h5[contains(text(), 'Widgets')]]")

    def go_to_elements(self):
        self.safe_click(self.Elements)

    def go_to_forms(self):
        self.safe_click(self.Forms)

    def go_to_alerts_frame_windows(self):
        self.safe_click(self.AlertsFrameWindows)

    def go_to_widgets(self):
        self.safe_click(self.Widgets)
