from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from data_tests.forms_data import StudentFormFactory
from page_objects.base_page import BasePage


class FormsPage(BasePage):
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

    def go_to_practice_form(self):
        self.element_is_clickable(self.PracticeFormButton).click()

    def full_student_form(self, person: StudentFormFactory):
        self.element_is_visible(self.FirstName).send_keys(person.first_name)
        self.element_is_visible(self.LastName).send_keys(person.last_name)
        self.element_is_visible(self.Email).send_keys(person.email)
        self.safe_click(self.Gender[person.gender])
        self.element_is_visible(self.PhoneNumber).send_keys(person.phone_number)
        data_birthday_field = self.element_is_visible(self.DataBirthday)
        self.driver.execute_script("arguments[0].value = arguments[1];", data_birthday_field,
                                   person.data_birthday)  # set up value directly
        self.element_is_visible(self.Subjects).send_keys(person.subjects)
        self.element_is_visible(self.Subjects).send_keys(Keys.ENTER)
        self.safe_click(self.Hobbies[person.hobbies])
        self.element_is_presence(self.Picture).send_keys(person.picture)
        self.element_is_visible(self.CurrentAddress).send_keys(person.current_address)
        self.element_is_visible(self.State).send_keys(person.state)
        self.element_is_visible(self.State).send_keys(Keys.ENTER)
        self.element_is_visible(self.City).send_keys(person.city)
        self.element_is_visible(self.City).send_keys(Keys.ENTER)
        self.safe_click(self.SubmitButton)

    def form_result(self):
        result_list_field = self.elements_are_visible(self.ModalTableField)
        return [res.text for res in result_list_field]

