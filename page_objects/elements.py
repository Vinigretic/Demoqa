import random

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from data_tests.text_box_data import PersonFactory
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