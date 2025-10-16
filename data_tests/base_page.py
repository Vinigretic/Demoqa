from selenium.common import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)

    def element_is_visible(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def element_is_clickable(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def element_is_presence(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.presence_of_element_located(locator))


    def safe_click(self, locator, timeout=10):
        element = self.element_is_clickable(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)  # scrolls the page so that the element is in the visible part of the window, usually at the top.
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)  # performs a click via JavaScript, bypassing Selenium's standard .click().
            # If a regular .click() doesn't work (e.g. the element is obscured, there's an animation, or a loader), JS-click bypasses the restrictions and clicks anyway.
