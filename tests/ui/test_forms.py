import allure
import pytest

from generator.forms_generator import full_student_form_fields
from tests.base.base_test_page import BaseTestPage


@allure.suite("Forms")
class TestFormsPage(BaseTestPage):
    @allure.feature("Practice Form")
    @allure.story("Navigation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Navigate to Forms page")
    @pytest.mark.positive
    def test_go_to_forms_page(self, driver):
        self.practice_form_get_page(driver)
        assert "automation-practice-form" in driver.current_url.lower(), 'The transition to the Forms page failed'

    @allure.feature("Fill Student Registration Form")
    @allure.story("Form filling")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Fill in all form fields")
    @pytest.mark.positive
    def test_full_student_form(self, driver, student_person):
        forms_page = self.practice_form_get_page(driver)
        forms_page.full_student_form(student_person)
        result = forms_page.form_result()
        assert (f"{student_person.first_name} {student_person.last_name}", student_person.email) == (
            result[0], result[1]), 'The form has not been filled'
