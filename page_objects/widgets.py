import random

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from generator.auto_complete_generator import generator_color
from page_objects.base_page import BasePage


class AccordionPage(BasePage):
    AccordionButton = (By.XPATH, "//span[contains(text(), 'Accordian')]")
    AccordionSections = {
        'first': {
            'header': (By.ID, "section1Heading"),
            'state': (By.XPATH, "//div[@id='section1Heading']/following-sibling::div"),
            'content': (By.XPATH, "//div[@id='section1Content']/p"),
            'content_result': 'Lorem Ipsum is simply dummy text'
        },
        'second': {
            'header': (By.ID, "section2Heading"),
            'state': (By.XPATH, "//div[@id='section2Heading']/following-sibling::div"),
            'content': (By.XPATH, "//div[@id='section2Content']/p"),
            'content_result': 'Contrary to popular belief'
        },
        'third': {
            'header': (By.ID, "section3Heading"),
            'state': (By.XPATH, "//div[@id='section3Heading']/following-sibling::div"),
            'content': (By.XPATH, "//div[@id='section3Content']/p"),
            'content_result': 'It is a long established'
        }
    }

    def go_to_accordion_page(self):
        self.element_is_clickable(self.AccordionButton).click()

    def click_accordion(self, section_name):
        self.safe_click(self.AccordionSections[section_name]['header'])
        WebDriverWait(self.driver, 10).until(
            lambda d: "collapsing" not in self.element_is_presence(
                self.AccordionSections[section_name]['state']).get_attribute(
                "class")
        )
        click_result = self.element_is_presence(self.AccordionSections[section_name]['state']).get_attribute("class")
        return click_result

    def check_accordion(self, section_name):
        state_accordion = self.element_is_presence(self.AccordionSections[section_name]['state']).get_attribute("class")
        if state_accordion == 'collapse show':
            open_click_result = state_accordion
        else:
            open_click_result = self.click_accordion(section_name)
        content = self.element_is_presence(self.AccordionSections[section_name]['content']).text
        close_click_result = self.click_accordion(section_name)
        content_result = self.AccordionSections[section_name]['content_result']
        return open_click_result, content, close_click_result, content_result


class AutoCompletePage(BasePage):
    AutoCompleteButton = (By.XPATH, "//span[contains(text(), 'Auto Complete')]")
    MultiInput = (By.ID, "autoCompleteMultipleInput")
    MULTI_VALUE = (By.CSS_SELECTOR, 'div[class="css-1rhbuit-multiValue auto-complete__multi-value"]')
    MULTI_VALUE_REMOVE = (By.CSS_SELECTOR, 'div[class="css-1rhbuit-multiValue auto-complete__multi-value"] svg path')
    MULTI_VALUE_REMOVE_All = (By.CSS_SELECTOR, 'div[class="auto-complete__indicators css-1wy0on6"] svg path')
    SingleInput = (By.ID, "autoCompleteSingleInput")
    SINGLE_VALUE = (By.CSS_SELECTOR, 'div[class="auto-complete__single-value css-1uccc91-singleValue"]')

    def go_to_auto_complete_page(self):
        self.scroll_to_element(self.AutoCompleteButton)
        self.element_is_clickable(self.AutoCompleteButton).click()

    def check_fill_multi_input(self, quantity_color):
        list_color_input = random.sample(generator_color().color_name, k=quantity_color)
        for color in list_color_input:
            self.element_is_visible(self.MultiInput).click()
            self.element_is_visible(self.MultiInput).send_keys(color)
            self.element_is_visible(self.MultiInput).send_keys(Keys.ENTER)
        list_color = self.elements_are_visible(self.MULTI_VALUE)
        list_color_result = [color.text for color in list_color]
        return list_color_result, list_color_input

    def check_delete_multi_input(self, mode):
        if mode == 'single':
            remove_list_color_button = self.elements_are_visible(self.MULTI_VALUE_REMOVE)
            for color in remove_list_color_button:
                color.click()
        else:
            self.element_is_clickable(self.MULTI_VALUE_REMOVE_All).click()
        result = WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.MULTI_VALUE))
        return result

    def check_fill_single_input(self):
        color = random.choice(generator_color().color_name)
        self.safe_click(self.SingleInput)
        self.element_is_visible(self.SingleInput).send_keys(color)
        self.element_is_visible(self.SingleInput).send_keys(Keys.ENTER)
        color_result = self.element_is_visible(self.SINGLE_VALUE).text
        return color_result, color
