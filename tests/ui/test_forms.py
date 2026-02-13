import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from tests.base.base_test_page import BaseTestPage
from utils.logger import ui_logger


@allure.suite("Forms")
class TestFormsPage(BaseTestPage):
    """Test suite for Forms page functionality."""

    @allure.feature("Practice Form")
    @allure.story("Navigation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Navigate to Forms page")
    @pytest.mark.positive
    def test_go_to_forms_page(self, driver: WebDriver) -> None:
        """Verify navigation to the Forms page."""

        ui_logger.log("STEP", "Start test: Navigate to Forms page")
        self.practice_form_get_page(driver)
        ui_logger.debug(f"Current URL after navigation: {driver.current_url}")
        assert "automation-practice-form" in driver.current_url.lower(), 'The transition to the Forms page failed'
        ui_logger.log("STEP", "Successfully navigated to Forms page")

    @allure.feature("Fill Student Registration Form")
    @allure.story("Form filling")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Fill in all form fields")
    @pytest.mark.positive
    def test_full_student_form(self, driver: WebDriver, student_person) -> None:
        """Verify filling and submitting the student form."""

        ui_logger.log("STEP", "Start test: Fill in all form fields")
        forms_page = self.practice_form_get_page(driver)
        forms_page.full_student_form(student_person)
        result = forms_page.form_result()
        ui_logger.debug(f"Form result from modal: {result}")
        assert (f"{student_person.first_name} {student_person.last_name}", student_person.email) == (
            result[0], result[1]), 'The form has not been filled'
        ui_logger.log("STEP", "Form successfully filled and validated")
