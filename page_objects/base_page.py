from selenium.common import ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait


class BasePage:

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)

    def element_is_visible(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def elements_are_visible(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))

    def element_is_clickable(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def element_is_presence(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def elements_are_presence(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def safe_click(self, locator, timeout=10):
        element = self.element_is_clickable(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                   element)  # scrolls the page so that the element is in the visible part of the window, usually at the top.
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();",
                                       element)  # performs a click via JavaScript, bypassing Selenium's standard .click().
            # If a regular .click() doesn't work (e.g. the element is obscured, there's an animation, or a loader), JS-click bypasses the restrictions and clicks anyway.

    def element_is_not_visible(self, locator, timeout=10):
        return wait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    def scroll_to_element(self, locator, timeout=10):
        element = self.element_is_presence(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();",element)
        return element

    def action_double_click(self, locator, timeout=10):
        element = self.element_is_visible(locator, timeout)
        action = ActionChains(self.driver)
        action.double_click(element).perform()

    def action_right_click(self, locator, timeout=10):
        element = self.element_is_visible(locator, timeout)
        action = ActionChains(self.driver)
        action.context_click(element).perform()

    def action_drag_and_drop_by_offset(self, element, x_coords, y_coords):
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(element, x_coords, y_coords)
        action.perform()

    def action_move_to_element(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.perform()

    def js_right_click(self, locator, timeout=10):
        element = self.element_is_visible(locator, timeout)
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('contextmenu', {bubbles: true}));",
                                   element)
