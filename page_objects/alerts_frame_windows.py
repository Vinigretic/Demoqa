from selenium.webdriver.common.by import By

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
