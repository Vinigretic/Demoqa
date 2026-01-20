import pytest

from tests.base.base_test_page import BaseTestPage


class TestMainPage:
    class TestElementsMainPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_elements(self, driver):
            elements = self.get_main_page(driver)
            elements.go_to_elements()
            assert "elements" in driver.current_url.lower(), "The transition to the Elements page failed"

    class TestFormsMainPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_forms(self, driver):
            forms = self.get_main_page(driver)
            forms.go_to_forms()
            assert "forms" in driver.current_url.lower(), "The transition to the Forms page failed"

    class TestAlertsFrameWindowsMainPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_alerts_frame_windows(self, driver):
            alerts_frame_windows = self.get_main_page(driver)
            alerts_frame_windows.go_to_alerts_frame_windows()
            assert "alertswindows" in driver.current_url.lower(), "The transition to the Alerts Frame Windows page failed"

    class TestWidgetsMainPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_widgets_page(self, driver):
            widgets = self.get_main_page(driver)
            widgets.go_to_widgets()
            assert "widgets" in driver.current_url.lower(), "The transition to the Widgets page failed"

    class TestInteractionsMainPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_interactions_page(self, driver):
            interactions = self.get_main_page(driver)
            interactions.go_to_interactions()
            assert "interaction" in driver.current_url.lower(), "The transition to the Interactions page failed"
