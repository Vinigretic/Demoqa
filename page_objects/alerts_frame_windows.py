import random
import allure

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.base_page import BasePage


class BrowserWindowsPage(BasePage):
    BrowserWindowsButton = (By.XPATH, "//span[contains(text(), 'Browser Windows')]")
    NewTabButton = (By.ID, "tabButton")
    NewWindowButton = (By.ID, "windowButton")
    NewWindowMessageButton = (By.ID, "messageWindowButton")
    SamplePageTitle = (By.ID, "sampleHeading")

    @allure.step("Go to Browser Windows page")
    def go_to_browser_windows_page(self):
        self.element_is_clickable(self.BrowserWindowsButton).click()

    @allure.step("Open new tab/window and get URL and title")
    def check_open_new_tab_or_window(self, locator):
        with allure.step("Scroll to open button"):
            self.scroll_to_element(locator)
        with allure.step("Click button to open new tab/window"):
            self.element_is_clickable(locator).click()
        with allure.step("Switch to the last opened tab/window"):
            self.driver.switch_to.window(self.driver.window_handles[-1])
        sample_page_url = self.driver.current_url
        with allure.step("Read sample page title"):
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

    @allure.step("Go to Alerts page")
    def go_to_alerts_page(self):
        self.element_is_clickable(self.AlertsButton).click()

    @allure.step("Click simple alert and get text")
    def check_alert_button(self):
        with allure.step("Click alert button"):
            self.element_is_clickable(self.AlertButton).click()
        with allure.step("Switch to alert and read text"):
            alert = self.driver.switch_to.alert
            return alert.text

    @allure.step("Click timer alert and get text (timeout: {timeout}s)")
    def check_timer_alert_button(self, timeout=5):
        with allure.step("Click timer alert button"):
            self.safe_click(self.TimerAlertButton)
        try:
            with allure.step("Wait for alert to appear"):
                WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            with allure.step("Switch to alert and read text"):
                alert = self.driver.switch_to.alert
                return alert.text
        except TimeoutException:
            return None

    @allure.step("Click confirm alert and execute command: {command}")
    def check_confirm_button(self, command):
        with allure.step("Click confirm button"):
            self.safe_click(self.ConfirmButton)
        alert = self.driver.switch_to.alert
        with allure.step(f"Handle alert: {command}"):
            if command == 'accept':
                alert.accept()
            elif command == 'dismiss':
                alert.dismiss()
            else:
                raise ValueError(f"Unknown command: {command}")
        with allure.step("Read result text from page"):
            return self.element_is_presence(self.ConfirmResult).text

    @allure.step("Click prompt alert, enter random text and accept")
    def check_promt_button(self):
        with allure.step("Click prompt button"):
            self.safe_click(self.PromtButton)
        alert = self.driver.switch_to.alert
        text = f"test{random.randint(0, 999)}"
        with allure.step(f"Enter text into prompt: {text}"):
            alert.send_keys(text)
        with allure.step("Accept prompt"):
            alert.accept()
        with allure.step("Read result text from page"):
            result_message = self.element_is_presence(self.PromptResult).text
        return result_message, text


class FramesPage(BasePage):
    FramesButton = (By.XPATH, "//span[text()='Frames']")
    FrameOne = (By.ID, "frame1")
    FrameTwo = (By.ID, "frame2")
    FrameSamplePageTitle = (By.ID, "sampleHeading")

    @allure.step("Go to Frames page")
    def go_to_frames_page(self):
        self.safe_click(self.FramesButton)

    @allure.step("Check frame size and title")
    def check_frame(self, locator):
        try:
            with allure.step("Locate frame element"):
                frame = self.element_is_presence(locator)
            with allure.step("Read frame size attributes"):
                width = frame.get_attribute("width")
                height = frame.get_attribute("height")
            with allure.step("Switch to frame and read title"):
                self.driver.switch_to.frame(frame)
                frame_title = self.element_is_presence(self.FrameSamplePageTitle).text
            with allure.step("Switch back to default content"):
                self.driver.switch_to.default_content()
            return width, height, frame_title
        except TimeoutException:
            return None


class NestedFramesPage(BasePage):
    NestedFramesButton = (By.XPATH, "//span[text()='Nested Frames']")
    FrameParent = (By.ID, "frame1")
    FrameChild = (By.CSS_SELECTOR, 'iframe[srcdoc="<p>Child Iframe</p>"]')
    FrameParentText = (By.CSS_SELECTOR, 'body')
    FrameChildText = (By.CSS_SELECTOR, 'p')

    @allure.step("Go to Nested Frames page")
    def go_to_nested_frames_page(self):
        self.safe_click(self.NestedFramesButton)

    @allure.step("Check nested frames structure (parent/child)")
    def check_nested_frame(self):
        frame_child_text = None
        try:
            with allure.step("Switch to parent frame"):
                parent_frame = self.element_is_presence(self.FrameParent)
                self.driver.switch_to.frame(parent_frame)
            with allure.step("Read parent frame text"):
                frame_parent_text = self.element_is_presence(self.FrameParentText).text
            try:
                with allure.step("Switch to child frame"):
                    child_frame = self.element_is_presence(self.FrameChild)
                    self.driver.switch_to.frame(child_frame)
                with allure.step("Read child frame text"):
                    frame_child_text = self.element_is_presence(self.FrameChildText).text
            except TimeoutException:
                frame_child_text = None
        except TimeoutException:
            frame_parent_text = None
        finally:
            with allure.step("Switch back to default content"):
                self.driver.switch_to.default_content()
        return frame_parent_text, frame_child_text


class ModalDialogsPage(BasePage):
    ModalDialogsButton = (By.XPATH, "//span[contains(text(), 'Modal Dialogs')]")
    SmallModalButton = (By.ID, "showSmallModal")
    LargeModalButton = (By.ID, "showLargeModal")
    SmallModalTitle = (By.ID, "example-modal-sizes-title-sm")
    LargeModalTitle = (By.ID, "example-modal-sizes-title-lg")
    SmallModalCloseButton = (By.ID, "closeSmallModal")
    LargeModalCloseButton = (By.ID, "closeLargeModal")

    @allure.step("Go to Modal Dialogs page")
    def go_to_modal_dialogs_page(self):
        self.safe_click(self.ModalDialogsButton)

    @allure.step("Open modal, read title and close it")
    def check_modal(self, open, title, close):
        with allure.step("Open modal dialog"):
            self.element_is_clickable(open).click()
        with allure.step("Read modal title"):
            modal_title = self.element_is_visible(title).text
        with allure.step("Close modal dialog"):
            self.element_is_clickable(close).click()
        modal_closed = True
        try:
            with allure.step("Wait for modal to become invisible"):
                WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(title))
        except TimeoutException:
            modal_closed = False
        return modal_title, modal_closed
