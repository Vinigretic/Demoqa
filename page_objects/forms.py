from typing import List

import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from data_tests.forms_data import StudentFormFactory
from page_objects.base_page import BasePage
from utils.logger import ui_logger


class FormsPage(BasePage):
    """Page object for the Practice Form page."""
    PracticeFormButton = (By.XPATH, "//span[contains(text(), 'Practice Form')]")
    FirstName = (By.CSS_SELECTOR, "#firstName")
    LastName = (By.CSS_SELECTOR, "#lastName")
    Email = (By.XPATH, "//input[@id='userEmail']")
    Gender = {
        'male': (By.XPATH, "//label[@for='gender-radio-1']"),
        'female': (By.XPATH, "//label[@for='gender-radio-2']"),
        'other': (By.XPATH, "//label[@for='gender-radio-3']")
    }
    PhoneNumber = (By.XPATH, "//input[@id='userNumber']")
    DataBirthday = (By.XPATH, "//input[@id='dateOfBirthInput']")
    Subjects = (By.XPATH, "//input[@id='subjectsInput']")
    Hobbies = {
        'sport': (By.XPATH, "//label[@for='hobbies-checkbox-1']"),
        'reading': (By.XPATH, "//label[@for='hobbies-checkbox-2']"),
        'music': (By.XPATH, "//label[@for='hobbies-checkbox-3']"),
    }
    Picture = (By.XPATH, "//input[@id='uploadPicture']")
    CurrentAddress = (By.XPATH, "//textarea[@id='currentAddress']")
    State = (By.CSS_SELECTOR, 'input[id="react-select-3-input"]')
    City = (By.CSS_SELECTOR, 'input[id="react-select-4-input"]')
    SubmitButton = (By.XPATH, "//button[@id='submit']")
    ModalTableField = (By.XPATH, "//table[contains(@class, 'table')]//td[2]")

    @allure.step("Go to Forms page")
    def go_to_practice_form(self) -> None:
        """Navigate to Practice Form page."""
        ui_logger.log("STEP", "Navigate to Practice Form")
        self.element_is_clickable(self.PracticeFormButton).click()

    @allure.step("Fill and submit student form")
    def full_student_form(self, person: StudentFormFactory) -> None:
        """Fill the student form with provided data and submit."""

        ui_logger.log("STEP", "Start filling student form")

        with allure.step("Input first name"):
            ui_logger.debug(f"Input first name: {person.first_name}")
            self.element_is_visible(self.FirstName).send_keys(person.first_name)
        with allure.step("Input last name"):
            ui_logger.debug(f"Input last name: {person.last_name}")
            self.element_is_visible(self.LastName).send_keys(person.last_name)
        with allure.step("Input email"):
            ui_logger.debug(f"Input email: {person.email}")
            self.element_is_visible(self.Email).send_keys(person.email)
        with allure.step("Select gender"):
            ui_logger.debug(f"Select gender: {person.gender}")
            self.safe_click(self.Gender[person.gender])
        with allure.step("Input phone number"):
            ui_logger.debug(f"Input phone number: {person.phone_number}")
            self.element_is_visible(self.PhoneNumber).send_keys(person.phone_number)
        with allure.step("Set date of birth"):
            ui_logger.debug(f"Setting date of birth: {person.data_birthday}")
            data_birthday_field = self.element_is_visible(self.DataBirthday)
            self.driver.execute_script("arguments[0].value = arguments[1];", data_birthday_field,
                                       person.data_birthday)  # set up value directly
        with allure.step("Add subject"):
            ui_logger.debug(f"Input subject: {person.subjects}")
            self.element_is_visible(self.Subjects).send_keys(person.subjects)
        with allure.step("Confirm subject"):
            ui_logger.debug("Confirming subject with ENTER")
            self.element_is_visible(self.Subjects).send_keys(Keys.ENTER)
        with allure.step("Select hobby"):
            ui_logger.debug(f"Select hobby: {person.hobbies}")
            self.safe_click(self.Hobbies[person.hobbies])
        with allure.step("Upload picture"):
            ui_logger.debug(f"Upload picture: {person.picture}")
            self.element_is_presence(self.Picture).send_keys(person.picture)
        with allure.step("Input current address"):
            ui_logger.debug(f"Input current address: {person.current_address}")
            self.element_is_visible(self.CurrentAddress).send_keys(person.current_address)
        with allure.step("Select state"):
            ui_logger.debug(f"Select state: {person.state}")
            self.element_is_visible(self.State).send_keys(person.state)
        with allure.step("Confirm state"):
            ui_logger.debug("Confirming state with ENTER")
            self.element_is_visible(self.State).send_keys(Keys.ENTER)
        with allure.step("Select city"):
            ui_logger.debug(f"Select city: {person.city}")
            self.element_is_visible(self.City).send_keys(person.city)
        with allure.step("Confirm city"):
            ui_logger.debug("Confirm city with ENTER")
            self.element_is_visible(self.City).send_keys(Keys.ENTER)
        with allure.step("Submit form"):
            ui_logger.log("STEP", "Submit form")
            self.safe_click(self.SubmitButton)

    @allure.step("Get result from modal window")
    def form_result(self) -> List[str]:
        """Get results from modal window after form submission."""

        ui_logger.debug("Get results from modal window")
        result_list_field = self.elements_are_visible(self.ModalTableField)
        return [res.text for res in result_list_field]
