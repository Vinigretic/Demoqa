import random
import time

import pytest

from data_tests.text_box_data import *
from generator.text_box_generator import *
from page_objects.elements import RadioButtonPage
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
        def test_go_to_text_box(self, driver):
            self.text_box_get_page(driver)
            assert "text-box" in driver.current_url.lower()

        # def test_text_box_submit_form(self, driver):
        #     text_box = self.text_box_get_page(driver)
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
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            # The form does not send and the block does not appear
            assert page.is_result_block_visible(), f"The Form was sent with empty fields."

    class TestTextBoxPageEmailField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_email", email_categories['valid'])
        def test_text_box_page_valid_email(self, driver, valid_email):
            person = person_email_validation(valid_email)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert not page.is_email_field_invalid(), f"The Email - {valid_email} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_email",
                                 [email for group in email_categories["invalid_cases"].values() for email in group])
        def test_text_box_page_invalid_email(self, driver, invalid_email):
            person = person_email_validation(invalid_email)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            # The email field should be highlighted (for ex., class 'field-error')
            assert page.is_email_field_invalid(), f"The Email - {invalid_email} was not processed as invalid."

    class TestTextBoxPageFullNameField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_full_name", full_name_categories['valid'] + full_name_categories['security'])
        def test_text_box_page_valid_full_name(self, driver, valid_full_name):
            person = person_full_name_validation(valid_full_name)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert page.is_result_full_name_visible(), f"The Full name - {valid_full_name} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_full_name", full_name_categories['invalid'])
        def test_text_box_page_invalid_full_name(self, driver, invalid_full_name):
            person = person_full_name_validation(invalid_full_name)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert not page.is_result_full_name_visible(), f"The Full name - {invalid_full_name} was not processed as invalid."

    class TestTextBoxPageCurrentAddressField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_current_address", address_cases['valid'] + address_cases['security'])
        def test_text_box_page_valid_current_address(self, driver, valid_current_address):
            person = person_current_address_validation(valid_current_address)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert page.is_result_current_address_visible(), f"The Current address - {valid_current_address} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_current_address", address_cases['invalid'])
        def test_text_box_page_invalid_current_address(self, driver, invalid_current_address):
            person = person_current_address_validation(invalid_current_address)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert not page.is_result_current_address_visible(), f"The Full name - {invalid_current_address} was not processed as invalid."

    class TestTextBoxPagePermanentAddressField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_permanent_address", address_cases['valid'] + address_cases['security'])
        def test_text_box_page_valid_permanent_address(self, driver, valid_permanent_address):
            person = person_permanent_address_validation(valid_permanent_address)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert page.is_result_permanent_address_visible(), f"The Current address - {valid_permanent_address} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_permanent_address", address_cases['invalid'])
        def test_text_box_page_invalid_permanent_address(self, driver, invalid_permanent_address):
            person = person_permanent_address_validation(invalid_permanent_address)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert not page.is_result_permanent_address_visible(), f"The Full name - {invalid_permanent_address} was not processed as invalid."

    class TestCheckBoxPageTransition(BaseTestPage):
        def test_go_to_check_box(self, driver):
            self.check_box_get_page(driver)
            assert "checkbox" in driver.current_url.lower()

    class TestCheckBoxPageCheckboxClick(BaseTestPage):
        def test_get_all_checkboxes(self, driver):
            checkbox = self.check_box_get_page(driver)
            checkbox.open_checkboxes_list()
            checkbox.click_checkbox_random()
            checkbox.get_clicked_checkbox()
            checkbox.get_output_result()

            assert checkbox.get_clicked_checkbox() == checkbox.get_output_result(), "The checkboxes are not clicked"

    class TestRadioButtonPage(BaseTestPage):
        def test_go_to_radio_button(self, driver):
            self.radio_button_get_page(driver)
            assert "radio-button" in driver.current_url.lower(), 'The transition to the Radio button page did not occur'

        @pytest.mark.parametrize("radio_locator, expected_text", [
            (RadioButtonPage.YesRadio, "Yes"),
            (RadioButtonPage.ImpressiveRadio, "Impressive"),
            (RadioButtonPage.NoRadio, "No"),
        ])
        def test_radio_button_click(self, driver, radio_locator, expected_text):
            radio_button = self.radio_button_get_page(driver)
            radio_button.click_radio_button(radio_locator)
            result = radio_button.get_result_text()
            assert result == expected_text, 'The radio button NO is not clicked'

    class TestWebTablePage(BaseTestPage):
        def test_go_to_web_table_page(self, driver):
            self.web_table_get_page(driver)
            assert "webtables" in driver.current_url.lower(), 'The transition to the web tables page failed'

        def test_web_table_add_person(self, driver):
            web_table_page = self.web_table_get_page(driver)
            web_table_page.click_add_person_button()
            new_person = web_table_page.add_person_form_submit()
            result_table_people = web_table_page.check_person()
            assert new_person in result_table_people, f"The person - {new_person} was not added to the web table"

        @pytest.mark.parametrize("count", [1, 3, 7])
        def test_web_table_several_people(self, driver, count):
            web_table_page = self.web_table_get_page(driver)
            new_people = web_table_page.add_several_people(count)
            result_table_persons = web_table_page.check_person()
            for person in new_people:
                assert person in result_table_persons, f"The person - {person} was not added to the web table"

        def test_web_table_search_person(self, driver):
            web_table_page = self.web_table_get_page(driver)
            web_table_page.click_add_person_button()
            new_person = web_table_page.add_person_form_submit()
            web_table_page.search_person(random.choice(new_person))
            result_search_person = web_table_page.check_person()
            assert new_person in result_search_person, f"The person {new_person} was not found"

        @pytest.mark.parametrize("new_value_field, field_name, field_index",
                                 [('47', 'Age', 2), ('Sally', 'FirstName', 0)])
        def test_web_table_update_person_info(self, driver, new_value_field, field_name, field_index):
            web_table_page = self.web_table_get_page(driver)
            web_table_page.click_add_person_button()
            new_person = web_table_page.add_person_form_submit()
            new_person_last_name = new_person[1]
            web_table_page.search_person(new_person_last_name)
            web_table_page.update_person_info(new_value_field, field_name)
            updated_value = web_table_page.get_field_from_filtered_row(field_index)
            assert updated_value == new_value_field, f"Expected {new_value_field}, but got {updated_value}"

        def test_web_table_delete_person(self, driver):
            web_table_page = self.web_table_get_page(driver)
            web_table_page.click_add_person_button()
            new_person = web_table_page.add_person_form_submit()
            new_person_last_name = new_person[1]
            web_table_page.search_person(new_person_last_name)
            web_table_page.delete_person()
            assert web_table_page.check_delete_person() == "No rows found", f"The person{new_person} has not been deleted"

        @pytest.mark.parametrize("count", [10, 20, 25, 50, 100])
        def test_web_table_change_cound_row(self, driver, count):
            web_table_page = self.web_table_get_page(driver)
            web_table_page.select_count_rows(str(count))
            assert count == web_table_page.check_selected_rows(), "The numbers rows in the table has not been changed."

    class TestButtonPage(BaseTestPage):
        def test_go_to_buttons_page(self, driver):
            self.buttons_get_page(driver)
            assert "buttons" in driver.current_url.lower(), 'The transition to the buttons page failed'

        def test_double_click_button(self, driver):
            buttons_page = self.buttons_get_page(driver)
            buttons_page.double_click_button()
            assert buttons_page.get_message_after_click(
                'double') == 'You have done a double click', "The double click button was not pressed"

        def test_right_click_button(self, driver):
            buttons_page = self.buttons_get_page(driver)
            buttons_page.right_click_button()
            assert buttons_page.get_message_after_click(
                'right') == 'You have done a right click', "The right click button was not pressed"

        def test_click_button(self, driver):
            buttons_page = self.buttons_get_page(driver)
            buttons_page.click_button()
            assert buttons_page.get_message_after_click(
                'click') == 'You have done a dynamic click', "The click button was not pressed"
