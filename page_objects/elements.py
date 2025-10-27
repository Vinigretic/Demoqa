import random
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from data_tests.text_box_data import PersonFactory
from generator.web_table_generator import generated_person_web_table
from page_objects.base_page import BasePage
from page_objects.main_page import MainPage


class TextBoxPage(BasePage):
    TextBoxButton = (By.XPATH, "//span[contains(text(), 'Text Box')]")
    FullName = (By.CSS_SELECTOR, "#userName")
    Email = (By.CSS_SELECTOR, "#userEmail")
    CurrentAddress = (By.CSS_SELECTOR, "#currentAddress")
    PermanentAddress = (By.CSS_SELECTOR, "#permanentAddress")
    SubmitTextBox = (By.CSS_SELECTOR, "#submit")

    CreatedName = (By.CSS_SELECTOR, "#name")
    CreatedEmail = (By.CSS_SELECTOR, "#email")
    CreatedCurrentAddress = (By.XPATH, "//p[@id='currentAddress']")
    CreatedPermanentAddress = (By.XPATH, "//p[@id='permanentAddress']")
    CratedTextBlock = (By.XPATH, "//div[@id='output']/div")

    def go_to_text_box(self):
        self.element_is_clickable(self.TextBoxButton).click()

    def text_box_submit_form(self, person_info: PersonFactory):
        full_name = person_info.full_name
        email = person_info.email
        current_address = person_info.current_address
        permanent_address = person_info.permanent_address

        if person_info.full_name:
            self.element_is_visible(self.FullName).send_keys(full_name)
        if person_info.email:
            self.element_is_visible(self.Email).send_keys(email)
        if person_info.current_address:
            self.element_is_visible(self.CurrentAddress).send_keys(current_address)
        if person_info.permanent_address:
            self.element_is_visible(self.PermanentAddress).send_keys(permanent_address)
        self.scroll_to_element(self.SubmitTextBox).click()

    def get_info_from_text_box_form(self):
        created_full_name = None
        created_email = None
        created_current_address = None
        created_permanent_address = None

        try:
            # created_full_name = self.element_is_presence(self.CreatedName).text.split(':')[1]
            created_full_name = self.driver.find_element(*self.CreatedName).text.split(':')[1]
        except (TimeoutException, NoSuchElementException):
            pass
        try:
            # created_email = self.element_is_presence(self.CreatedEmail).text.split(':')[1]
            created_email = self.driver.find_element(*self.CreatedEmail).text.split(':')[1]
        except (TimeoutException, NoSuchElementException):
            pass
        try:
            # created_current_address = self.element_is_visible(self.CreatedCurrentAddress).text.split(':')[1]
            created_current_address = self.driver.find_element(*self.CreatedCurrentAddress).text.split(':')[1]
        except (TimeoutException, NoSuchElementException):
            pass
        try:
            # created_permanent_address = self.element_is_presence(self.CreatedPermanentAddress).text.split(':')[1]
            created_permanent_address = self.driver.find_element(*self.CreatedPermanentAddress).text.split(':')[1]
        except (TimeoutException, NoSuchElementException):
            pass
        return created_full_name, created_email, created_current_address, created_permanent_address

        # if self.driver.find_elements(*self.CreatedName):
        #     created_full_name = self.driver.find_element(*self.CreatedName).text.split(':')[1]
        # if self.driver.find_elements(*self.CreatedEmail):
        #     created_email = self.driver.find_element(*self.CreatedEmail).text.split(':')[1]
        # if self.driver.find_elements(*self.CreatedCurrentAddress):
        #     created_current_address = self.driver.find_element(*self.CreatedCurrentAddress).text.split(':')[1]
        # if self.driver.find_elements(*self.CreatedPermanentAddress):
        #     created_permanent_address = self.driver.find_element(*self.CreatedPermanentAddress).text.split(':')[1]
        # return created_full_name, created_email, created_current_address, created_permanent_address

    def is_result_block_visible(self):
        created_text_block = self.driver.find_element(*self.CratedTextBlock)
        return 'border' not in created_text_block.get_attribute('class')

    def is_email_field_invalid(self):
        email = self.element_is_visible(self.Email)
        return "field-error" in email.get_attribute('class')

    def is_result_full_name_visible(self):
        try:
            self.driver.find_element(*self.CreatedName)
            return True
        except NoSuchElementException:
            return False

    def is_result_current_address_visible(self):
        try:
            self.driver.find_element(*self.CurrentAddress)
            return True
        except NoSuchElementException:
            return False

    def is_result_permanent_address_visible(self):
        try:
            self.driver.find_element(*self.PermanentAddress)
            return True
        except NoSuchElementException:
            return False


class CheckBoxPage(BasePage):
    CheckBoxButton = (By.XPATH, "//span[contains(text(), 'Check Box')]")
    CheckBoxList = (By.XPATH, "//span[@class='rct-title']")
    ExpandAllButton = (By.XPATH, "//button[@class='rct-option rct-option-expand-all']")
    ClickedCheckBoxList = (By.CSS_SELECTOR, "svg[class='rct-icon rct-icon-check']")
    ClickedCheckBoxTitle = (By.XPATH, ".//ancestor::span[@class='rct-text']")
    # ClickedCheckBoxTitle = (By.XPATH, ".//ancestor::span[@class='rct-text']//span[@class='rct-title']")
    OutputResult = (By.XPATH, "//span[@class='text-success']")

    def go_to_check_box(self):
        self.element_is_clickable(self.CheckBoxButton).click()

    def open_checkboxes_list(self):
        self.element_is_visible(self.ExpandAllButton).click()

    def click_checkbox_random(self):
        checkboxes_list = self.elements_are_visible(self.CheckBoxList)
        for i in range(20):
            checkbox = checkboxes_list[random.randint(1, len(checkboxes_list) - 1)]
            self.driver.execute_script("arguments[0].scrollIntoView();", checkbox)
            checkbox.click()

    def get_clicked_checkbox(self):
        clicked_list = self.elements_are_visible(self.ClickedCheckBoxList)
        title_lists = [title_item.find_element(*self.ClickedCheckBoxTitle).text for title_item in clicked_list]
        return str(title_lists).replace(' ', '').replace('.doc', '').lower()

    def get_output_result(self):
        results = self.elements_are_visible(self.OutputResult)
        title_results = [item.text for item in results]
        return str(title_results).replace(' ', '').lower()


class RadioButtonPage(BasePage):
    RadioButton = (By.XPATH, "//span[contains(text(), 'Radio Button')]")
    YesRadio = (By.CSS_SELECTOR, "label[for='yesRadio']")
    ImpressiveRadio = (By.CSS_SELECTOR, "label[for='impressiveRadio']")
    NoRadio = (By.CSS_SELECTOR, "label[for='noRadio']")
    ResultText = (By.XPATH, "//p[@class='mt-3']")

    def go_to_radio_button(self):
        self.element_is_clickable(self.RadioButton).click()

    def click_radio_button(self, locator):
        self.safe_click(locator)

    def get_result_text(self):
        try:
            result = self.element_is_visible(self.ResultText).text
            return result.split()[-1]
        except (TimeoutException):
            return ''


class WebTablePage(BasePage):
    WebTableButton = (By.XPATH, "//span[contains(text(), 'Web Tables')]")
    AddPersonButton = (By.ID, "addNewRecordButton")
    FirstName = (By.XPATH, "//input[@id='firstName']")
    LastName = (By.XPATH, "//input[@id='lastName']")
    Email = (By.XPATH, "//input[@id='userEmail']")
    Age = (By.XPATH, "//input[@id='age']")
    Salary = (By.XPATH, "//input[@id='salary']")
    Department = (By.XPATH, "//input[@id='department']")
    RegisterFormSubmitButton = (By.XPATH, "//button[@id='submit']")
    FullPeopleList = (By.XPATH, "//div[@class='rt-tr-group']")
    SearchField = (By.XPATH, "//input[@id='searchBox']")
    EditButton = (By.XPATH, "//span[@title='Edit']")
    DeleteButton = (By.XPATH, "//span[@title='Delete']")
    NoRowsFound = (By.XPATH, "//div[@class='rt-noData']")
    DropdownPage = (By.XPATH, "//select[@aria-label='rows per page']")

    def go_to_web_table_page(self):
        self.scroll_to_element(self.WebTableButton)
        self.element_is_clickable(self.WebTableButton).click()

    def click_add_person_button(self):
        self.safe_click(self.AddPersonButton)

    def add_person_form_submit(self):
        person = generated_person_web_table()
        self.element_is_visible(self.FirstName).send_keys(person.first_name)
        self.element_is_visible(self.LastName).send_keys(person.last_name)
        self.element_is_visible(self.Email).send_keys(person.email)
        self.element_is_visible(self.Age).send_keys(person.age)
        self.element_is_visible(self.Salary).send_keys(person.salary)
        self.element_is_visible(self.Department).send_keys(person.department)
        self.safe_click(self.RegisterFormSubmitButton)

        return [person.first_name, person.last_name, str(person.age), person.email, str(person.salary),
                person.department.strip()]

    def add_several_people(self, count=3):
        people_list = []
        for i in range(count):
            self.click_add_person_button()
            people_list.append(self.add_person_form_submit())
        return people_list

    def search_person(self, person_field):
        self.element_is_clickable(self.SearchField).click()
        self.element_is_visible(self.SearchField).send_keys(person_field)

    def update_person_info(self, new_value_field, field_name):
        fields_name = {
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Email': self.Email,
            'Age': self.Age,
            'Salary': self.Salary,
            'Department': self.Department
        }

        self.element_is_visible(self.EditButton).click()
        self.element_is_visible(fields_name[field_name]).clear()
        self.element_is_visible(fields_name[field_name]).send_keys(new_value_field)
        self.safe_click(self.RegisterFormSubmitButton)

    def check_person(self):
        full_people_list = self.elements_are_visible(self.FullPeopleList)
        return [person.text.splitlines() for person in full_people_list]

    def get_field_from_filtered_row(self, field_index):
        rows = self.elements_are_visible(self.FullPeopleList)
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, "div.rt-td")
            values = [cell.text.strip() for cell in cells if cell.text.strip()]
            if values:
                return values[field_index]
        return ""

    def is_person_present(self, value):
        people = self.check_person()
        for person in people:
            if value in person:
                return person
        return None

    def delete_person(self):
        self.element_is_clickable(self.DeleteButton).click()

    def check_delete_person(self):
        return self.element_is_presence(self.NoRowsFound).text

    def select_count_rows(self, count=5):
        self.scroll_to_element(self.DropdownPage)
        dropdown = Select(self.element_is_visible(self.DropdownPage))
        dropdown.select_by_value(str(count))

    def check_selected_rows(self):
        return len(self.check_person())
