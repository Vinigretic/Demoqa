import pytest

from data_tests.text_box_data import *
from generator.text_box_generator import *
from page_objects.main_page import MainPage
from tests.base.base_test_page import BaseTestPage


class TestMainPage:

    def test_go_to_elements(self, driver):
        elements = MainPage(driver, "https://demoqa.com/")
        elements.open()
        elements.go_to_elements()
        assert "elements" in driver.current_url.lower()


class TestElementsPage:
    class TestTextBoxPageFillForm(BaseTestPage):
        # def test_go_to_text_box(self, driver):
        #     self.text_box_page_create(driver)
        #     assert "text-box" in driver.current_url.lower()
        #
        # def test_text_box_submit_form(self, driver):
        #     text_box = self.text_box_page_create(driver)
        #     full_name, email, current_address, permanent_address = text_box.text_box_submit_form()
        #     created_full_name, created_email, created_current_address, created_permanent_address = text_box.get_info_from_text_box_form()
        #     assert full_name == created_full_name, 'The full name does not match'
        #     assert email == created_email, 'The email does not match'
        #     assert current_address == created_current_address, 'The current_address does not match'
        #     assert permanent_address == created_permanent_address, 'The permanent_address does not match'

        def assert_text_box_result(self, person, result):
            if person.full_name:
                assert person.full_name == result[0], "Full name mismatch"
            if person.email:
                assert person.email == result[1], "Email mismatch"
            if person.current_address:
                assert person.current_address.replace("\n", " ") == result[2], "Current address mismatch"
            if person.permanent_address:
                assert person.permanent_address.replace("\n", " ") == result[3], "Permanent address mismatch"

        # Fill all fields
        @pytest.mark.positive
        def test_all_fields_filled(self, driver):
            person = person_all_fields()
            result = self.text_box_page_submit_and_validate(driver, person)
            self.assert_text_box_result(person, result)

        # Fill only one field
        @pytest.mark.positive
        @pytest.mark.parametrize("field", ["full_name", "email", "current_address", "permanent_address"])
        def test_single_field_filled(self, driver, field):
            person = person_partial(field)
            result = self.text_box_page_submit_and_validate(driver, person)
            self.assert_text_box_result(person, result)

        # Only one field is missing
        @pytest.mark.positive
        @pytest.mark.parametrize("missing_field", ["email", "full_name", "current_address", "permanent_address"])
        def test_one_field_missing(self, driver, missing_field):
            person = person_missing(missing_field)
            result = self.text_box_page_submit_and_validate(driver, person)
            self.assert_text_box_result(person, result)

        @pytest.mark.negative
        def test_text_box_page_all_fields_empty(self, driver):
            person = person_empty()
            page = self.text_box_page_create(driver)
            page.text_box_submit_form(person)

            # The form does not send and the block does not appear
            assert page.is_result_block_visible(), f"The Form was sent with empty fields."

    class TestTextBoxPageEmailField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_email", email_categories['valid'])
        def test_text_box_page_valid_email(self, driver, valid_email):
            person = person_email_validation(valid_email)
            page = self.text_box_page_create(driver)
            page.text_box_submit_form(person)

            assert not page.is_email_field_invalid(), f"The Email - {valid_email} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_email",
                                 [email for group in email_categories["invalid_cases"].values() for email in group])
        def test_text_box_page_invalid_email(self, driver, invalid_email):
            person = person_email_validation(invalid_email)
            page = self.text_box_page_create(driver)
            page.text_box_submit_form(person)

            # The email field should be highlighted (for ex., class 'field-error')
            assert page.is_email_field_invalid(), f"The Email - {invalid_email} was not processed as invalid."

    class TestTextBoxPageFullNameField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_full_name", full_name_categories['valid'] + full_name_categories['security'])
        def test_text_box_page_valid_full_name(self, driver, valid_full_name):
            person = person_full_name_validation(valid_full_name)
            page = self.text_box_page_create(driver)
            page.text_box_submit_form(person)

            assert page.is_result_full_name_visible(), f"The Full name - {valid_full_name} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_full_name", full_name_categories['invalid'])
        def test_text_box_page_invalid_full_name(self, driver, invalid_full_name):
            person = person_full_name_validation(invalid_full_name)
            page = self.text_box_page_create(driver)
            page.text_box_submit_form(person)

            assert not page.is_result_full_name_visible(), f"The Full name - {invalid_full_name} was not processed as invalid."

    class TestTextBoxPageCurrentAddressField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_current_address", address_cases['valid'] + address_cases['security'])
        def test_text_box_page_valid_current_address(self, driver, valid_current_address):
            person = person_current_address_validation(valid_current_address)
            page = self.text_box_page_create(driver)
            page.text_box_submit_form(person)

            assert page.is_result_current_address_visible(), f"The Current address - {valid_current_address} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_current_address", address_cases['invalid'])
        def test_text_box_page_invalid_current_address(self, driver, invalid_current_address):
            person = person_current_address_validation(invalid_current_address)
            page = self.text_box_page_create(driver)
            page.text_box_submit_form(person)

            assert not page.is_result_current_address_visible(), f"The Full name - {invalid_current_address} was not processed as invalid."

    class TestTextBoxPagePermanentAddressField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_permanent_address", address_cases['valid'] + address_cases['security'])
        def test_text_box_page_valid_permanent_address(self, driver, valid_permanent_address):
            person = person_permanent_address_validation(valid_permanent_address)
            page = self.text_box_page_create(driver)
            page.text_box_submit_form(person)

            assert page.is_result_permanent_address_visible(), f"The Current address - {valid_permanent_address} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_permanent_address", address_cases['invalid'])
        def test_text_box_page_invalid_permanent_address(self, driver, invalid_permanent_address):
            person = person_permanent_address_validation(invalid_permanent_address)
            page = self.text_box_page_create(driver)
            page.text_box_submit_form(person)

            assert not page.is_result_permanent_address_visible(), f"The Full name - {invalid_permanent_address} was not processed as invalid."
