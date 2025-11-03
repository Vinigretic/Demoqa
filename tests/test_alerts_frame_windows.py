import pytest

from page_objects.alerts_frame_windows import BrowserWindowsPage
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
