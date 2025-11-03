import pytest

from page_objects.alerts_frame_windows import BrowserWindowsPage
from tests.base.base_test_page import BaseTestPage


class TestAlertsFrameWindowsPage:
    # class TestBrowserWindowsPage(BaseTestPage):
    #     @pytest.mark.positive
    #     def test_go_to_browser_windows_page(self, driver):
    #         self.browser_windows_get_page(driver)
    #         assert "browser-windows" in driver.current_url.lower(), 'The transition to the Browser Windows page failed'
    #
    #     @pytest.mark.positive
    #     @pytest.mark.parametrize(
    #         'locator', (BrowserWindowsPage.NewTabButton, BrowserWindowsPage.NewWindowButton))
    #     def test_new_tab_or_window(self, driver, locator):
    #         browser_windows_page = self.browser_windows_get_page(driver)
    #         sample_page_url, sample_page_title = browser_windows_page.check_open_new_tab_or_window(locator)
    #         assert 'sample' in sample_page_url, 'The transition to the sample page failed'
    #         assert sample_page_title == "This is a sample page", 'The title of the sample page does not match'

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
            alert_page = self.alerts_get_page(driver)
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
