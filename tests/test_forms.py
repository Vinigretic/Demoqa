import pytest

from generator.forms_generator import *
from tests.base.base_test_page import BaseTestPage


class TestFormsPage(BaseTestPage):
    @pytest.mark.positive
    def test_go_to_forms_page(self, driver):
        self.practice_form_get_page(driver)
        assert "automation-practice-form" in driver.current_url.lower(), 'The transition to the Forms page failed'

    @pytest.mark.positive
    def test_full_student_form(self, driver):
        forms_page = self.practice_form_get_page(driver)
        person = full_student_form_fields()
        try:
            forms_page.full_student_form(person)
            result = forms_page.form_result()
            assert (f"{person.first_name} {person.last_name}", person.email) == (
                result[0], result[1]), 'The form has not been filled'
        finally:
            person.delete_file(person.picture)
