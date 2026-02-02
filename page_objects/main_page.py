import allure
from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage


class MainPage(BasePage):
    Elements = (By.XPATH, "//div[contains(@class, 'card mt-4 top-card') and .//h5[contains(text(), 'Elements')]]")
    Forms = (By.XPATH, "//div[contains(@class, 'card mt-4 top-card') and .//h5[contains(text(), 'Forms')]]")
    AlertsFrameWindows = (By.XPATH,
                          "//div[contains(@class, 'card mt-4 top-card') and .//h5[contains(text(), 'Alerts, Frame & Windows')]]")
    Widgets = (By.XPATH, "//div[contains(@class, 'card mt-4 top-card') and .//h5[contains(text(), 'Widgets')]]")
    Interactions = (By.XPATH,
                    "//div[contains(@class, 'card mt-4 top-card') and .//h5[contains(text(), 'Interactions')]]")

    @allure.step("Navigate: Elements")
    def go_to_elements(self):
        with allure.step("Click on 'Elements' card"):
            self.safe_click(self.Elements)

    @allure.step("Navigate: Forms")
    def go_to_forms(self):
        with allure.step("Click on 'Forms' card"):
            self.safe_click(self.Forms)

    @allure.step("Navigate: Alerts, Frame & Windows")
    def go_to_alerts_frame_windows(self):
        with allure.step("Click on 'Alerts, Frame & Windows' card"):
            self.safe_click(self.AlertsFrameWindows)

    @allure.step("Navigate: Widgets")
    def go_to_widgets(self):
        with allure.step("Click on 'Widgets' card"):
            self.safe_click(self.Widgets)

    @allure.step("Navigate: Interactions")
    def go_to_interactions(self):
        with allure.step("Click on 'Interactions' card"):
            self.safe_click(self.Interactions)
