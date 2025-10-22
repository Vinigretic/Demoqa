from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage


class MainPage(BasePage):
    Elements = (By.XPATH, "//div[contains(@class, 'card mt-4 top-card') and .//h5[contains(text(), 'Elements')]]")

    def go_to_elements(self):
        self.safe_click(self.Elements)
