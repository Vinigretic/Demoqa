import pytest
import allure
from tests.base.base_test_page import BaseTestPage


@allure.suite("Main Page")
class TestMainPage:
    @allure.feature("Elements")
    class TestElementsMainPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigate to Elements")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Elements page")
        def test_go_to_elements(self, driver):
            elements = self.get_main_page(driver)
            elements.go_to_elements()
            assert "elements" in driver.current_url.lower(), "The transition to the Elements page failed"

    @allure.feature("Forms")
    class TestFormsMainPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigate to Forms")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Forms page")
        def test_go_to_forms(self, driver):
            forms = self.get_main_page(driver)
            forms.go_to_forms()
            assert "forms" in driver.current_url.lower(), "The transition to the Forms page failed"

    @allure.feature("Alerts, Frame & Windows")
    class TestAlertsFrameWindowsMainPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigate to Alerts, Frame & Windows")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Alerts Frame Windows page")
        def test_go_to_alerts_frame_windows(self, driver):
            alerts_frame_windows = self.get_main_page(driver)
            alerts_frame_windows.go_to_alerts_frame_windows()
            assert "alertswindows" in driver.current_url.lower(), "The transition to the Alerts Frame Windows page failed"

    @allure.feature("Widgets")
    class TestWidgetsMainPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigate to Widgets")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Widgets page")
        def test_go_to_widgets_page(self, driver):
            widgets = self.get_main_page(driver)
            widgets.go_to_widgets()
            assert "widgets" in driver.current_url.lower(), "The transition to the Widgets page failed"

    @allure.feature("Interactions")
    class TestInteractionsMainPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigate to Interactions")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Interactions page")
        def test_go_to_interactions_page(self, driver):
            interactions = self.get_main_page(driver)
            interactions.go_to_interactions()
            assert "interaction" in driver.current_url.lower(), "The transition to the Interactions page failed"
