import pytest

from page_objects.alerts_frame_windows import BrowserWindowsPage, FramesPage
from tests.base.base_test_page import BaseTestPage


class TestAlertsFrameWindowsPage:
    class TestBrowserWindowsPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_browser_windows_page(self, driver):
            self.browser_windows_get_page(driver)
            assert "browser-windows" in driver.current_url.lower(), 'The transition to the Browser Windows page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize(
            'locator', (BrowserWindowsPage.NewTabButton, BrowserWindowsPage.NewWindowButton))
        def test_new_tab_or_window(self, driver, locator):
            browser_windows_page = self.browser_windows_get_page(driver)
            sample_page_url, sample_page_title = browser_windows_page.check_open_new_tab_or_window(locator)
            assert 'sample' in sample_page_url, 'The transition to the sample page failed'
            assert sample_page_title == "This is a sample page", 'The title of the sample page does not match'

    class TestAlertsPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_alerts_page(self, driver):
            self.alerts_get_page(driver)
            assert "alerts" in driver.current_url.lower(), 'The transition to the Alerts page failed'

        @pytest.mark.positive
        def test_check_alert_button(self, driver):
            alert_page = self.alerts_get_page(driver)
            alert_text = alert_page.check_alert_button()
            assert 'You clicked a button' == alert_text, 'The alert button was not appeared'

        @pytest.mark.positive
        def test_check_timer_alert_button(self, driver):
            alert_text = alert_page.check_timer_alert_button()
            assert 'This alert appeared after 5 seconds' == alert_text, \
                'The timer alert button was not appeared after 5 seconds or text does not match.'

        @pytest.mark.positive
        @pytest.mark.parametrize('command, message',
                                 (('accept', 'You selected Ok'), ('dismiss', 'You selected Cancel')))
        def test_check_confirm_button(self, driver, command, message):
            alert_page = self.alerts_get_page(driver)
            result_message = alert_page.check_confirm_button(command)
            assert message == result_message, 'The confirm alert button was not appeared'

        @pytest.mark.positive
        def test_check_promt_button(self, driver):
            alert_page = self.alerts_get_page(driver)
            result_message, text = alert_page.check_promt_button()
            assert text in result_message, 'The promt alert button was not appeared'

    class TestFramesPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_frames_page(self, driver):
            self.frames_get_page(driver)
            assert "frames" in driver.current_url.lower(), 'The transition to the Frames page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize('locator, width, height',
                                 ((FramesPage.FrameOne, '500px', '350px'), (FramesPage.FrameTwo, '100px', '100px')))
        def test_check_frame(self, driver, locator, width, height):
            frames_page = self.frames_get_page(driver)
            assert frames_page.check_frame(locator) is not None, "The frame does not exist"
            width_result, height_result, frame_title = frames_page.check_frame(locator)
            assert width == width_result and height == height_result and 'This is a sample page' == frame_title

    class TestNestedFramesPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_nested_frames_page(self, driver):
            self.nested_frames_get_page(driver)
            assert "nestedframes" in driver.current_url.lower(), 'The transition to the Nested frames page failed'

        @pytest.mark.positive
        def test_check_nested_frame(self, driver):
            nested_frame_page = self.nested_frames_get_page(driver)
            frame_parent_text, frame_child_text = nested_frame_page.check_nested_frame()
            assert frame_parent_text == 'Parent frame', 'The parent frame does not exist'
            assert frame_child_text == 'Child Iframe', 'The child frame does not exist'
