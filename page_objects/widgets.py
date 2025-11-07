import random
import time

from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from generator.auto_complete_generator import generator_color
from generator.date_picker_generator import generated_date_time
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


class DatePickerPage(BasePage):
    DatePickerButton = (By.XPATH, "//span[contains(text(), 'Date Picker')]")
    DateInput = (By.ID, "datePickerMonthYearInput")
    DateSelectMonth = (By.XPATH, "//select[@class='react-datepicker__month-select']")
    DateSelectYear = (By.XPATH, "//select[@class='react-datepicker__year-select']")
    # DateSelectDay = (By.XPATH, f"//div[contains(@class, 'react-datepicker__day react-datepicker__day')]") # --026

    DateTimeInput = (By.ID, "dateAndTimePickerInput")
    DateTimeMonth = (By.XPATH, "//div[@class='react-datepicker__month-read-view']")
    DateTimeYear = (By.XPATH, "//div[@class='react-datepicker__year-read-view']")
    DateTimeMonthList = (By.XPATH, "//div[@class='react-datepicker__month-option']")
    DateTimeYearList = (By.XPATH, "//div[@class='react-datepicker__year-option']")
    DateTimeTimeList = (By.XPATH, "//li[@class='react-datepicker__time-list-item ']")

    @staticmethod
    def get_date_selected_day_locator(day):
        day_str = f"{int(day):03d}"  # formats 1 → '001', 26 → '026'
        return (By.XPATH, f"//div[contains(@class, 'react-datepicker__day--{day_str}')]")

    def select_month_or_year(self, date, locator):
        dropdown = Select(self.element_is_presence(locator))
        dropdown.select_by_visible_text(date)
        return dropdown

    def select_month_or_year_list(self, date, locator):
        elements_list = self.elements_are_presence(locator)
        for element in elements_list:
            if element.text == date:
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                element.click()
                break

    def go_to_date_picker_page(self):
        self.scroll_to_element(self.DatePickerButton)
        self.element_is_clickable(self.DatePickerButton).click()

    def check_change_date(self):
        date = generated_date_time()
        date_input = self.element_is_clickable(self.DateInput)
        date_input_before = date_input.get_attribute('value')
        date_input.click()
        # dropdown_month = Select(self.element_is_presence(self.DateSelectMonth))
        # dropdown_month.select_by_visible_text(date.month)
        # dropdown_year = Select(self.element_is_presence(self.DateSelectYear))
        # dropdown_year.select_by_visible_text(date.year)
        self.select_month_or_year(date.month, self.DateSelectMonth)
        self.select_month_or_year(date.year, self.DateSelectYear)
        self.element_is_clickable(self.get_date_selected_day_locator(date.day)).click()
        date_input_result = date_input.get_attribute('value')
        return date_input_before, date_input_result

    def check_change_date_time(self):
        date = generated_date_time()
        date_input_before = self.element_is_presence(self.DateTimeInput).get_attribute('value')
        self.safe_click(self.DateTimeInput)
        self.element_is_clickable(self.DateTimeYear).click()
        self.select_month_or_year_list(date.year, self.DateTimeYearList)
        self.element_is_clickable(self.DateTimeMonth).click()
        self.select_month_or_year_list(date.month, self.DateTimeMonthList)
        self.element_is_clickable(self.get_date_selected_day_locator(date.day)).click()
        self.select_month_or_year_list(date.time, self.DateTimeTimeList)
        date_input_result = self.element_is_presence(self.DateTimeInput).get_attribute('value')
        return date_input_before, date_input_result


class SliderPage(BasePage):
    SliderButton = (By.XPATH, "//span[contains(text(), 'Slider')]")
    SliderInput = (By.XPATH, "//input[@class='range-slider range-slider--primary']")
    SliderValue = (By.ID, "sliderValue")

    def go_to_slider_page(self):
        self.scroll_to_element(self.SliderButton)
        self.element_is_clickable(self.SliderButton).click()

    def check_change_slider_value(self):
        value_before = self.element_is_presence(self.SliderValue).get_attribute('value')
        slider_input = self.element_is_visible(self.SliderInput)
        self.action_drag_and_drop_by_offset(slider_input, random.randint(0, 100), 0)
        value_after = self.element_is_presence(self.SliderValue).get_attribute('value')
        return value_before, value_after


class ProgressBarPage(BasePage):
    ProgressBarButton = (By.XPATH, "//span[contains(text(), 'Progress Bar')]")
    ProgressBarValue = (By.XPATH, "//div[@class='progress-bar bg-info']")
    ProgressBarStart = (By.ID, "startStopButton")

    def go_to_progress_bar_page(self):
        self.scroll_to_element(self.ProgressBarButton)
        self.element_is_clickable(self.ProgressBarButton).click()

    def check_change_progress_bar(self):
        value_before = self.element_is_presence(self.ProgressBarValue).text
        self.element_is_clickable(self.ProgressBarStart).click()
        time.sleep(random.randint(2, 8))
        self.element_is_clickable(self.ProgressBarStart).click()
        value_after = self.element_is_presence(self.ProgressBarValue).text
        return value_before, value_after

class TabsPage(BasePage):
    TabsButton = (By.XPATH, "//span[contains(text(), 'Tabs')]")
    Tabs = {
        'what': {
            'tab': (By.ID, "demo-tab-what"),
            'text': (By.XPATH, "//div[@id='demo-tabpane-what']/p"),
            'expected_text': 'Lorem Ipsum'
        },
        'origin': {
            'tab': (By.ID, "demo-tab-origin"),
            'text': (By.XPATH, "//div[@id='demo-tabpane-origin']/p"),
            'expected_text': 'Contrary to popular belief'
        },
        'use': {
            'tab': (By.ID, "demo-tab-use"),
            'text': (By.XPATH, "//div[@id='demo-tabpane-use']/p"),
            'expected_text': 'It is a long established fact'
        },
        'more': {
            'tab': (By.ID, "demo-tab-more"),
            'text': (By.XPATH, "//div[@id='demo-tabpane-more']/p"),
            'expected_text': 'The more the better'
        }
    }


    def go_to_tabs_page(self):
        self.scroll_to_element(self.TabsButton)
        self.element_is_clickable(self.TabsButton).click()

    def check_click_tab_and_get_text(self, tabs):
        tab_text = None
        try:
            self.element_is_clickable(self.Tabs[tabs]['tab']).click()
            tab_text = self.element_is_presence(self.Tabs[tabs]['text']).text
        except (TimeoutException, ElementClickInterceptedException):
            pass
        return tab_text, self.Tabs[tabs]['expected_text']






















