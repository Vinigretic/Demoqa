import pytest
import allure

from page_objects.alerts_frame_windows import BrowserWindowsPage, FramesPage, ModalDialogsPage
from tests.base.base_test_page import BaseTestPage


@allure.suite("Alerts, Frame & Windows")
class TestAlertsFrameWindowsPage:
    @allure.feature("Browser Windows")
    class TestBrowserWindowsPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Browser Windows page")
        def test_go_to_browser_windows_page(self, driver):
            self.browser_windows_get_page(driver)
            assert "browser-windows" in driver.current_url.lower(), 'The transition to the Browser Windows page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize(
            'locator', (BrowserWindowsPage.NewTabButton, BrowserWindowsPage.NewWindowButton))
        @allure.story("Open in new tab or window")
        @allure.severity(allure.severity_level.NORMAL)
        def test_new_tab_or_window(self, driver, locator):
            allure.dynamic.title(f"Open {'New Tab' if locator == BrowserWindowsPage.NewTabButton else 'New Window'}")
            browser_windows_page = self.browser_windows_get_page(driver)
            sample_page_url, sample_page_title = browser_windows_page.check_open_new_tab_or_window(locator)
            assert 'sample' in sample_page_url, 'The transition to the sample page failed'
            assert sample_page_title == "This is a sample page", 'The title of the sample page does not match'

    @allure.feature("Alerts")
    class TestAlertsPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Alerts page")
        def test_go_to_alerts_page(self, driver):
            self.alerts_get_page(driver)
            assert "alerts" in driver.current_url.lower(), 'The transition to the Alerts page failed'

        @pytest.mark.positive
        @allure.story("Alert")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Click simple alert button")
        def test_check_alert_button(self, driver):
            alert_page = self.alerts_get_page(driver)
            alert_text = alert_page.check_alert_button()
            assert 'You clicked a button' == alert_text, 'The alert button was not appeared'

        @pytest.mark.positive
        @allure.story("Alert")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Alert appears after 5 seconds")
        def test_check_timer_alert_button(self, driver):
            alert_page = self.alerts_get_page(driver)
            alert_text = alert_page.check_timer_alert_button()
            assert 'This alert appeared after 5 seconds' == alert_text, \
                'The timer alert button was not appeared after 5 seconds or text does not match.'

        @pytest.mark.positive
        @pytest.mark.parametrize('command, message',
                                 (('accept', 'You selected Ok'), ('dismiss', 'You selected Cancel')))
        @allure.story("Confirm alert")
        @allure.severity(allure.severity_level.NORMAL)
        def test_check_confirm_button(self, driver, command, message):
            allure.dynamic.title(f"Confirm alert: {command}")
            alert_page = self.alerts_get_page(driver)
            result_message = alert_page.check_confirm_button(command)
            assert message == result_message, 'The confirm alert button was not appeared'

        @pytest.mark.positive
        @allure.story("Prompt alert")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Prompt alert accepts input")
        def test_check_promt_button(self, driver):
            alert_page = self.alerts_get_page(driver)
            result_message, text = alert_page.check_promt_button()
            assert text in result_message, 'The promt alert button was not appeared'

    @allure.feature("Frames")
    class TestFramesPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Frames page")
        def test_go_to_frames_page(self, driver):
            self.frames_get_page(driver)
            assert "frames" in driver.current_url.lower(), 'The transition to the Frames page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize('locator, width, height',
                                 ((FramesPage.FrameOne, '500px', '350px'), (FramesPage.FrameTwo, '100px', '100px')))
        @allure.story("Frames")
        @allure.severity(allure.severity_level.NORMAL)
        def test_check_frame(self, driver, locator, width, height):
            allure.dynamic.title(f"Check frame size {width} x {height}")
            frames_page = self.frames_get_page(driver)
            assert frames_page.check_frame(locator) is not None, "The frame does not exist"
            width_result, height_result, frame_title = frames_page.check_frame(locator)
            assert width == width_result and height == height_result and 'This is a sample page' == frame_title

    @allure.feature("Nested Frames")
    class TestNestedFramesPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Nested Frames page")
        def test_go_to_nested_frames_page(self, driver):
            self.nested_frames_get_page(driver)
            assert "nestedframes" in driver.current_url.lower(), 'The transition to the Nested frames page failed'

        @pytest.mark.positive
        @allure.story("Nested frames")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Check nested frames structure")
        def test_check_nested_frame(self, driver):
            nested_frame_page = self.nested_frames_get_page(driver)
            frame_parent_text, frame_child_text = nested_frame_page.check_nested_frame()
            assert frame_parent_text == 'Parent frame', 'The parent frame does not exist'
            assert frame_child_text == 'Child Iframe', 'The child frame does not exist'

    @allure.feature("Modal Dialogs")
    class TestModalDialogsPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Modal Dialogs page")
        def test_go_modal_dialogs_get_page(self, driver):
            self.modal_dialogs_get_page(driver)
            assert "modal-dialogs" in driver.current_url.lower(), 'The transition to the Modal dialogs page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize('open, title, close, title_result', (
                (ModalDialogsPage.SmallModalButton, ModalDialogsPage.SmallModalTitle,
                 ModalDialogsPage.SmallModalCloseButton, "Small Modal"),
                (ModalDialogsPage.LargeModalButton, ModalDialogsPage.LargeModalTitle,
                 ModalDialogsPage.LargeModalCloseButton, "Large Modal")))
        @allure.story("Modal dialogs")
        @allure.severity(allure.severity_level.NORMAL)
        def test_check_modal(self, driver, open, title, close, title_result):
            allure.dynamic.title(f"Open and close {title_result}")
            modal_dialogs_page = self.modal_dialogs_get_page(driver)
            modal_title, modal_closed = modal_dialogs_page.check_modal(open, title, close)
            assert modal_title == title_result, f"The {title_result} dialog was not opened"
            assert modal_closed is True, f"The {title_result} dialog was not closed"
