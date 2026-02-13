from typing import Tuple, List

from selenium.common import ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

from utils.logger import ui_logger


class BasePage:
    """Base class for all page objects.
    Provides reusable methods for element interaction, waits, and user actions.
    """
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver: WebDriver, url: str) -> None:
        """Initialize the BasePage."""
        self.driver = driver
        self.url = url

    def open(self) -> None:
        """Open the page URL in the browser."""
        ui_logger.log("STEP", f"Go to: {self.url}")
        self.driver.get(self.url)

    def element_is_visible(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """Wait until element is visible."""
        ui_logger.debug(f"Waiting for an element to be visible: {locator}")
        return wait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def elements_are_visible(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> List[WebElement]:
        """Wait until all elements are visible."""
        ui_logger.debug(f"Waiting for elements to be visible: {locator}")
        return wait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))

    def element_is_clickable(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """Wait until element is clickable."""
        ui_logger.debug(f"Waiting for an element to be clickable: {locator}")
        return wait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def element_is_presence(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """Wait until element is present in DOM."""
        ui_logger.debug(f"Waiting for an element to appear in DOM: {locator}")
        return wait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def elements_are_presence(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> List[WebElement]:
        """Wait until elements are present in DOM."""
        ui_logger.debug(f"Waiting for elements to appear in DOM: {locator}")
        return wait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def safe_click(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> None:
        """Safely click an element, fallback to JS click if intercepted."""
        element = self.element_is_clickable(locator, timeout)
        ui_logger.debug(f"Click on an element: {locator}")
        self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                   element)  # scrolls the page so that the element is in the visible part of the window, usually at the top.
        try:
            element.click()
        except ElementClickInterceptedException:
            ui_logger.warning(f"Element {locator} is blocked, execute JS‑click")
            self.driver.execute_script("arguments[0].click();",
                                       element)  # performs a click via JavaScript, bypassing Selenium's standard .click().
            # If a regular .click() doesn't work (e.g. the element is obscured, there's an animation, or a loader), JS-click bypasses the restrictions and clicks anyway.

    def element_is_not_visible(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """Wait until element disappears from DOM."""
        ui_logger.debug(f"Waiting for the element to disappear: {locator}")
        return wait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    def scroll_to_element(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """Scroll to element and return it."""
        ui_logger.debug(f"Scroll to element: {locator}")
        element = self.element_is_presence(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return element

    def action_double_click(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> None:
        """Perform double click on element."""
        ui_logger.debug(f"Double click on an element: {locator}")
        element = self.element_is_visible(locator, timeout)
        action = ActionChains(self.driver)
        action.double_click(element).perform()

    def action_right_click(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> None:
        """Perform right click on element."""
        ui_logger.debug(f"Right click on an element: {locator}")
        element = self.element_is_visible(locator, timeout)
        action = ActionChains(self.driver)
        action.context_click(element).perform()

    def action_drag_and_drop_by_offset(self, element: WebElement, x_coords: int, y_coords: int) -> None:
        """Drag element by offset."""
        ui_logger.debug(f"Drag&Drop the {element} element by offset ({x_coords}, {y_coords})")
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(element, x_coords, y_coords)
        action.perform()

    def action_move_to_element(self, element: WebElement) -> None:
        """Hover element."""
        ui_logger.debug(f"hover an element: {element}")
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.perform()

    def action_drag_and_drop_to_element(self, source: WebElement, target: WebElement) -> None:
        """Drag source element to target element."""
        ui_logger.debug(f"Drag&Drop the {source} element to the {target}")
        # scroll to elements
        self.driver.execute_script("arguments[0].scrollIntoView(true);", source)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", target)
        action = ActionChains(self.driver)
        action.drag_and_drop(source, target)
        action.perform()

    def js_right_click(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> None:
        """Perform right click via JavaScript."""
        ui_logger.debug(f"JS-right click on an element: {locator}")
        element = self.element_is_visible(locator, timeout)
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('contextmenu', {bubbles: true}));",
                                   element)
