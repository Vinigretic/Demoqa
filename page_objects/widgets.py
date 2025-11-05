from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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
