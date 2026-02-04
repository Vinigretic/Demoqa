import os
import random

import allure
import pytest

from data_tests.text_box_data import *
from generator.text_box_generator import *
from generator.upload_download_generator import FileFactory
from page_objects.elements import RadioButtonPage, LinksPage
from tests.base.base_test_page import BaseTestPage


@allure.suite("Elements")
class TestElementsPage:
    @allure.feature("TextBox fill form")
    class TestTextBoxPageFillForm(BaseTestPage):
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to TextBox page")
        def test_go_to_text_box(self, driver):
            self.text_box_get_page(driver)
            assert "text-box" in driver.current_url.lower(), "The transition to the Text Box page failed"

            # def test_text_box_submit_form(self, driver):
            #     text_box = self.text_box_get_page(driver)
            #     full_name, email, current_address, permanent_address = text_box.text_box_submit_form()
            #     created_full_name, created_email, created_current_address, created_permanent_address = text_box.get_info_from_text_box_form()
            #     assert full_name == created_full_name, 'The full name does not match'
            #     assert email == created_email, 'The email does not match'
            #     assert current_address == created_current_address, 'The current_address does not match'
            #     assert permanent_address == created_permanent_address, 'The permanent_address does not match'

        @allure.step("Check the result of filling the form field")
        def assert_text_box_result(self, person, result):
            with allure.step("Check the result of filling the full name field"):
                if person.full_name:
                    assert person.full_name == result[0], "Full name mismatch"
            with allure.step("Check the result of filling the email field"):
                if person.email:
                    assert person.email == result[1], "Email mismatch"
            with allure.step("Check the result of filling the current address field"):
                if person.current_address:
                    assert person.current_address.replace("\n", " ") == result[2], "Current address mismatch"
            with allure.step("Check the result of filling the permanent address field"):
                if person.permanent_address:
                    assert person.permanent_address.replace("\n", " ") == result[3], "Permanent address mismatch"

            # Fill all fields

        @pytest.mark.positive
        @allure.story("Form filling")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Fill in all form fields")
        def test_all_fields_filled(self, driver):
            person = person_all_fields()
            result = self.text_box_page_submit_and_validate(driver, person)
            self.assert_text_box_result(person, result)

        # Fill only one field
        @pytest.mark.positive
        @pytest.mark.parametrize("field", ["full_name", "email", "current_address", "permanent_address"])
        @allure.story("Form filling")
        @allure.severity(allure.severity_level.CRITICAL)
        def test_single_field_filled(self, driver, field):
            allure.dynamic.title(f"Fill in only {field} field")
            person = person_partial(field)
            result = self.text_box_page_submit_and_validate(driver, person)
            self.assert_text_box_result(person, result)

        # Only one field is missing
        @pytest.mark.positive
        @pytest.mark.parametrize("missing_field", ["email", "full_name", "current_address", "permanent_address"])
        @allure.story("Form filling")
        @allure.severity(allure.severity_level.CRITICAL)
        def test_one_field_missing(self, driver, missing_field):
            allure.dynamic.title(f"Skip {missing_field} when filling the form")
            person = person_missing(missing_field)
            result = self.text_box_page_submit_and_validate(driver, person)
            self.assert_text_box_result(person, result)

        @pytest.mark.negative
        @allure.story("Negative scenarios form filling")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Submit an empty TextBox form")
        def test_text_box_page_all_fields_empty(self, driver):
            person = person_empty()
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            # The form does not send and the block does not appear
            assert page.is_result_block_visible(), f"The Form was sent with empty fields."

    @allure.feature("TextBox email field")
    class TestTextBoxPageEmailField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_email", email_categories['valid'])
        @allure.story("Valid email input")
        @allure.severity(allure.severity_level.NORMAL)
        def test_text_box_page_valid_email(self, driver, valid_email):
            allure.dynamic.title(f"{valid_email} should be accepted")
            person = person_email_validation(valid_email)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert not page.is_email_field_invalid(), f"The Email - {valid_email} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_email",
                                 [email for group in email_categories["invalid_cases"].values() for email in group])
        @allure.story("Invalid email input")
        @allure.severity(allure.severity_level.CRITICAL)
        def test_text_box_page_invalid_email(self, driver, invalid_email):
            allure.dynamic.title(f"{invalid_email} should be rejected")
            person = person_email_validation(invalid_email)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            # The email field should be highlighted (for ex., class 'field-error')
            assert page.is_email_field_invalid(), f"The Email - {invalid_email} was not processed as invalid."

    @allure.feature("TextBox full name field")
    class TestTextBoxPageFullNameField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_full_name", full_name_categories['valid'] + full_name_categories['security'])
        @allure.story("Valid input")
        @allure.severity(allure.severity_level.NORMAL)
        def test_text_box_page_valid_full_name(self, driver, valid_full_name):
            allure.dynamic.title(f"Valid full name {valid_full_name} should be accepted")
            person = person_full_name_validation(valid_full_name)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert page.is_result_full_name_visible(), f"The Full name - {valid_full_name} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_full_name", full_name_categories['invalid'])
        @allure.story("Invalid full name input")
        @allure.severity(allure.severity_level.CRITICAL)
        def test_text_box_page_invalid_full_name(self, driver, invalid_full_name):
            allure.dynamic.title(f"Invalid full name {invalid_full_name} should be rejected")
            person = person_full_name_validation(invalid_full_name)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert not page.is_result_full_name_visible(), \
                f"The Full name - {invalid_full_name} was not processed as invalid."

    @allure.feature("TextBox current address field")
    class TestTextBoxPageCurrentAddressField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_current_address", address_cases['valid'] + address_cases['security'])
        @allure.story("Valid current address input")
        @allure.severity(allure.severity_level.NORMAL)
        def test_text_box_page_valid_current_address(self, driver, valid_current_address):
            allure.dynamic.title(f"Valid current address {valid_current_address} should be accepted")
            person = person_current_address_validation(valid_current_address)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert page.is_result_current_address_visible(), \
                f"The Current address - {valid_current_address} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_current_address", address_cases['invalid'])
        @allure.story("Invalid current address input")
        @allure.severity(allure.severity_level.NORMAL)
        def test_text_box_page_invalid_current_address(self, driver, invalid_current_address):
            allure.dynamic.title(f"Invalid current address {invalid_current_address} should be rejected")
            person = person_current_address_validation(invalid_current_address)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert not page.is_result_current_address_visible(), \
                f"The Current address - {invalid_current_address} was not processed as invalid."

    @allure.feature("TextBox permanent address field")
    class TestTextBoxPagePermanentAddressField(BaseTestPage):
        @pytest.mark.positive
        @pytest.mark.parametrize("valid_permanent_address", address_cases['valid'] + address_cases['security'])
        @allure.story("Valid permanent address input")
        @allure.severity(allure.severity_level.NORMAL)
        def test_text_box_page_valid_permanent_address(self, driver, valid_permanent_address):
            allure.dynamic.title(f"Valid permanent address {valid_permanent_address} should be accepted")
            person = person_permanent_address_validation(valid_permanent_address)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert page.is_result_permanent_address_visible(), \
                f"The Permanent address - {valid_permanent_address} was not processed as valid."

        @pytest.mark.negative
        @pytest.mark.parametrize("invalid_permanent_address", address_cases['invalid'])
        @allure.story("Invalid permanent address input")
        @allure.severity(allure.severity_level.NORMAL)
        def test_text_box_page_invalid_permanent_address(self, driver, invalid_permanent_address):
            allure.dynamic.title(f"Invalid permanent address {invalid_permanent_address} should be rejected")
            person = person_permanent_address_validation(invalid_permanent_address)
            page = self.text_box_get_page(driver)
            page.text_box_submit_form(person)

            assert not page.is_result_permanent_address_visible(), \
                f"The Permanent address - {invalid_permanent_address} was not processed as invalid."

    @allure.feature("Check box page")
    class TestCheckBoxPageTransition(BaseTestPage):
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigation to the check box page")
        def test_go_to_check_box(self, driver):
            self.check_box_get_page(driver)
            assert "checkbox" in driver.current_url.lower()

    @allure.feature("Check box page")
    class TestCheckBoxPageCheckboxClick(BaseTestPage):
        @allure.story("Checkbox selection")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Click random checkbox and verify it is selected")
        def test_click_random_checkbox_verify_it_is_selected(self, driver):
            checkbox = self.check_box_get_page(driver)
            checkbox.open_checkboxes_list()
            checkbox.click_checkbox_random()

            assert checkbox.get_clicked_checkbox() == checkbox.get_output_result(), "The checkboxes are not clicked"

    @allure.feature("Radio button page")
    class TestRadioButtonPage(BaseTestPage):
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigation to the radio button page")
        def test_go_to_radio_button(self, driver):
            self.radio_button_get_page(driver)
            assert "radio-button" in driver.current_url.lower(), 'The transition to the Radio button page did not occur'

        @pytest.mark.parametrize("radio_locator, expected_text", [
            (RadioButtonPage.YesRadio, "Yes"),
            (RadioButtonPage.ImpressiveRadio, "Impressive"),
            (RadioButtonPage.NoRadio, "No"),
        ])
        @allure.story("Radio button selection")
        @allure.severity(allure.severity_level.NORMAL)
        def test_radio_button_click(self, driver, radio_locator, expected_text):
            allure.dynamic.title(f"Click radiobutton {expected_text} and verify it is selected")
            radio_button = self.radio_button_get_page(driver)
            radio_button.click_radio_button(radio_locator)
            result = radio_button.get_result_text()
            assert result == expected_text, f'Expected {expected_text}, but got {result}'

    @allure.feature("Web table page")
    class TestWebTablePage(BaseTestPage):
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigation to the Web table page")
        def test_go_to_web_table_page(self, driver):
            self.web_table_get_page(driver)
            assert "webtables" in driver.current_url.lower(), 'The transition to the web tables page failed'

        @allure.story("Add records")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Adding one person to the web table")
        def test_web_table_add_person(self, driver):
            web_table_page = self.web_table_get_page(driver)
            web_table_page.click_add_person_button()
            new_person = web_table_page.add_person_form_submit()
            result_table_people = web_table_page.check_person()
            assert new_person in result_table_people, f"The person - {new_person} was not added to the web table"

        @allure.story("Add records")
        @allure.severity(allure.severity_level.NORMAL)
        @pytest.mark.parametrize("count", [1, 3, 7])
        def test_web_table_several_people(self, driver, count):
            allure.dynamic.title(f"Adding a different number of people to the web table - {count}")
            web_table_page = self.web_table_get_page(driver)
            new_people = web_table_page.add_several_people(count)
            result_table_persons = web_table_page.check_person()
            for person in new_people:
                assert person in result_table_persons, f"The person - {person} was not added to the web table"

        @allure.story("Search")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Searching info in the web table")
        def test_web_table_search_person(self, driver):
            web_table_page = self.web_table_get_page(driver)
            web_table_page.click_add_person_button()
            new_person = web_table_page.add_person_form_submit()
            web_table_page.search_person(random.choice(new_person))
            result_search_person = web_table_page.check_person()
            assert new_person in result_search_person, f"The person {new_person} was not found"

        @allure.story("Update info")
        @allure.severity(allure.severity_level.NORMAL)
        @pytest.mark.parametrize("new_value_field, field_name, field_index",
                                 [('47', 'Age', 2), ('Sally', 'FirstName', 0)])
        def test_web_table_update_person_info(self, driver, new_value_field, field_name, field_index):
            allure.dynamic.title(f"Update {field_name} in the web table")
            web_table_page = self.web_table_get_page(driver)
            web_table_page.click_add_person_button()
            new_person = web_table_page.add_person_form_submit()
            new_person_last_name = new_person[1]
            web_table_page.search_person(new_person_last_name)
            web_table_page.update_person_info(new_value_field, field_name)
            updated_value = web_table_page.get_field_from_filtered_row(field_index)
            assert updated_value == new_value_field, f"Expected {new_value_field}, but got {updated_value}"

        @allure.story("Delete info")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Delete info from the web table")
        def test_web_table_delete_person(self, driver):
            web_table_page = self.web_table_get_page(driver)
            web_table_page.click_add_person_button()
            new_person = web_table_page.add_person_form_submit()
            new_person_last_name = new_person[1]
            web_table_page.search_person(new_person_last_name)
            web_table_page.delete_person()
            assert web_table_page.check_delete_person() == "No rows found", f"The person{new_person} has not been deleted"

        @allure.story("Rows per page")
        @allure.severity(allure.severity_level.NORMAL)
        @pytest.mark.parametrize("count", [10, 20, 25, 50, 100])
        def test_web_table_change_count_row(self, driver, count):
            allure.dynamic.title(f"Checking the display of {count} of table rows")
            web_table_page = self.web_table_get_page(driver)
            web_table_page.select_count_rows(str(count))
            assert count == web_table_page.check_selected_rows(), "The numbers rows in the table has not been changed."

    @allure.feature("Buttons page")
    class TestButtonsPage(BaseTestPage):
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigation to the Buttons page")
        def test_go_to_buttons_page(self, driver):
            self.buttons_get_page(driver)
            assert "buttons" in driver.current_url.lower(), 'The transition to the buttons page failed'

        @allure.story("Double click action")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Check the double click button")
        def test_double_click_button(self, driver):
            buttons_page = self.buttons_get_page(driver)
            buttons_page.double_click_button()
            assert buttons_page.get_message_after_click(
                'double') == 'You have done a double click', "The double click button was not pressed"

        @allure.story("Right click action")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Check the right click button")
        def test_right_click_button(self, driver):
            buttons_page = self.buttons_get_page(driver)
            buttons_page.right_click_button()
            assert buttons_page.get_message_after_click(
                'right') == 'You have done a right click', "The right click button was not pressed"

        @allure.story("Single click action")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Check the single click button")
        def test_click_button(self, driver):
            buttons_page = self.buttons_get_page(driver)
            buttons_page.click_button()
            assert buttons_page.get_message_after_click(
                'click') == 'You have done a dynamic click', "The click button was not pressed"

    @allure.feature("Links page")
    class TestLinksPage(BaseTestPage):
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigation to the Links page")
        def test_go_to_links_page(self, driver):
            self.links_get_page(driver)
            assert "links" in driver.current_url.lower(), 'The transition to the links page failed'

        @allure.story("Open in new tab")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Check that links open in a new tab")
        @pytest.mark.parametrize('locator', (LinksPage.LinkHome, LinksPage.LinkDynamicHome))
        def test_check_link_open_new_tab(self, driver, locator):
            links_page = self.links_get_page(driver)
            statuscode, link_url = links_page.check_link_open_new_tab(locator)
            assert statuscode == 200, f"Expected status 200, but got {statuscode}"
            assert link_url.lower() == driver.current_url.lower(), 'The transition to the home page failed'

        @allure.story("Status code")
        @allure.severity(allure.severity_level.NORMAL)
        @pytest.mark.parametrize('locator, expected_status',
                                 (("created", "201"), ("no_content", "204"), ("moved", "301"), ("bad_request", "400"),
                                  ("unauthorized", "401"), ("forbidden", "403"), ("not_found", "404")))
        def test_check_api_links(self, driver, locator, expected_status):
            allure.dynamic.title(f"Check that links get {expected_status} status code")
            links_page = self.links_get_page(driver)
            response_text = links_page.get_text_api_link(locator).lower()
            # staus due to website error
            assert f"staus {expected_status}" in response_text, \
                f"Expected status {expected_status} in response, but got: {response_text}"

    @allure.feature("Upload Download page")
    class TestUploadDownloadPage(BaseTestPage):
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigation to Upload Download page")
        def test_go_to_upload_download_page(self, driver):
            self.upload_download_get_page(driver)
            assert "upload-download" in driver.current_url.lower(), 'The transition to the Upload and Download page failed'

        @allure.story("Upload file")
        @allure.severity(allure.severity_level.NORMAL)
        @pytest.mark.parametrize("method_name", ("create_temp_txt", "create_temp_json", "create_temp_csv"))
        def test_upload_file(self, driver, method_name):
            allure.dynamic.title(f"Upload {method_name} file and check the file name")
            upload_download_page = self.upload_download_get_page(driver)
            create_method = getattr(FileFactory, method_name)
            file_name = create_method()
            try:
                # uploaded_file_path = upload_download_page.upload_file(file_name).split("\\")[-1]
                # assert uploaded_file_path == file_name.split("\\")[-1], f"The file {file_name} was not uploaded"
                uploaded_file_path = upload_download_page.upload_file(file_name)
                assert os.path.basename(uploaded_file_path) == os.path.basename(file_name), \
                    f"The file {file_name} was not uploaded"

            finally:
                FileFactory.delete_file(file_name)

        @allure.story("Download file")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Download file and check the file name")
        def test_download_file(self, driver_for_download_file):
            driver_f, download_dir = driver_for_download_file
            upload_download_page = self.upload_download_get_page(driver_f)
            upload_download_page.download_file()
            downloaded_file = upload_download_page.wait_for_file(download_dir)

            assert downloaded_file, f"File was not downloaded to {download_dir}"

            file_path = os.path.join(download_dir,
                                     downloaded_file)  # C:\Users\vbaka\AppData\Local\Temp\tmpofl9clj2\sampleFile.jpeg
            assert os.path.exists(file_path), f"File {downloaded_file} was not found in {download_dir}"

    @allure.feature("Dynamic properties page")
    class TestDynamicProperties(BaseTestPage):
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigation to Dynamic properties page")
        def test_go_to_dynamic_properties_page(self, driver):
            self.dynamic_properties_get_page(driver)
            assert "dynamic-properties" in driver.current_url.lower(), 'The transition to the Dynamic Properties page failed'

        @allure.story("Button color change")
        @allure.severity(allure.severity_level.MINOR)
        @allure.title("Check the button color change")
        def test_check_color_change_button(self, driver):
            dynamic_properties_page = self.dynamic_properties_get_page(driver)
            color_before, color_after = dynamic_properties_page.check_color_change_button()
            assert color_before != color_after, "The color button was not changed."

        @allure.story("Button is enabled")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Check the button is enabled")
        def test_check_enable_button(self, driver):
            dynamic_properties_page = self.dynamic_properties_get_page(driver)
            assert dynamic_properties_page.check_enable_button(), "The enable button was not clickable."

        @allure.story("Button is visible")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Check the button is visible")
        def test_check_visible_button(self, driver):
            dynamic_properties_page = self.dynamic_properties_get_page(driver)
            assert dynamic_properties_page.check_visible_button(), "The visible button was not visible."
