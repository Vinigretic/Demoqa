import random
import time

import allure
from selenium.common import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException, \
    NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from generator.auto_complete_generator import generator_color
from generator.date_picker_generator import generated_date_time
from generator.select_menu_generator import generator_menu
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

    @allure.step("Go to Accordion page")
    def go_to_accordion_page(self):
        self.element_is_clickable(self.AccordionButton).click()

    @allure.step("Click accordion header: {section_name}")
    def click_accordion(self, section_name):
        with allure.step("Click accordion header element"):
            self.safe_click(self.AccordionSections[section_name]['header'])
        with allure.step("Wait until animation completes"):
            WebDriverWait(self.driver, 10).until(
                lambda d: "collapsing" not in self.element_is_presence(
                    self.AccordionSections[section_name]['state']).get_attribute(
                    "class")
            )
        with allure.step("Read accordion state class"):
            click_result = self.element_is_presence(self.AccordionSections[section_name]['state']).get_attribute(
                "class")
        return click_result

    @allure.step("Check accordion section: {section_name}")
    def check_accordion(self, section_name):
        with allure.step("Read current accordion state"):
            state_accordion = self.element_is_presence(self.AccordionSections[section_name]['state']).get_attribute(
                "class")
        if state_accordion == 'collapse show':
            open_click_result = state_accordion
        else:
            with allure.step("Open accordion section"):
                open_click_result = self.click_accordion(section_name)
        with allure.step("Read accordion content text"):
            content = self.element_is_presence(self.AccordionSections[section_name]['content']).text
        with allure.step("Close accordion section"):
            close_click_result = self.click_accordion(section_name)
        with allure.step("Set expected content text"):
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

    @allure.step("Go to AutoComplete page")
    def go_to_auto_complete_page(self):
        with allure.step("Scroll to 'Auto Complete' button"):
            self.scroll_to_element(self.AutoCompleteButton)
        with allure.step("Click 'Auto Complete' button"):
            self.element_is_clickable(self.AutoCompleteButton).click()

    @allure.step("Fill multi input with {quantity_color} colors")
    def check_fill_multi_input(self, quantity_color):
        list_color_input = random.sample(generator_color().color_name, k=quantity_color)
        for color in list_color_input:
            with allure.step(f"Type color '{color}'"):
                self.element_is_visible(self.MultiInput).click()
                self.element_is_visible(self.MultiInput).send_keys(color)
            with allure.step("Confirm color"):
                self.element_is_visible(self.MultiInput).send_keys(Keys.ENTER)
        with allure.step("Collect selected colors from UI"):
            list_color = self.elements_are_visible(self.MULTI_VALUE)
            list_color_result = [color.text for color in list_color]
        return list_color_result, list_color_input

    @allure.step("Delete colors from multi input with mode '{mode}'")
    def check_delete_multi_input(self, mode):
        if mode == 'single':
            with allure.step("Remove colors one by one"):
                remove_list_color_button = self.elements_are_visible(self.MULTI_VALUE_REMOVE)
                for color in remove_list_color_button:
                    color.click()
        else:
            with allure.step("Remove all colors"):
                self.element_is_clickable(self.MULTI_VALUE_REMOVE_All).click()
        with allure.step("Verify colors container not visible"):
            result = self.element_is_not_visible(self.MULTI_VALUE)
        return result

    @allure.step("Fill single input with color")
    def check_fill_single_input(self):
        color = random.choice(generator_color().color_name)
        with allure.step("Focus single input"):
            self.safe_click(self.SingleInput)
        with allure.step(f"Type color '{color}' and confirm (ENTER)"):
            self.element_is_visible(self.SingleInput).send_keys(color)
            self.element_is_visible(self.SingleInput).send_keys(Keys.ENTER)
        with allure.step("Read selected color from UI"):
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
        with allure.step(f"Select '{date}' in dropdown"):
            dropdown = Select(self.element_is_presence(locator))
            dropdown.select_by_visible_text(date)
        return dropdown

    def select_month_or_year_list(self, date, locator):
        with allure.step("Choose option from list"):
            elements_list = self.elements_are_presence(locator)
            for element in elements_list:
                if element.text == date:
                    with allure.step(f"Scroll into view and click option '{date}'"):
                        self.driver.execute_script("arguments[0].scrollIntoView();", element)
                        element.click()
                    break

    @allure.step("Go to Date Picker page")
    def go_to_date_picker_page(self):
        self.scroll_to_element(self.DatePickerButton)
        self.element_is_clickable(self.DatePickerButton).click()

    @allure.step("Change date")
    def check_change_date(self):
        date = generated_date_time()
        with allure.step("Get current date from input"):
            date_input = self.element_is_clickable(self.DateInput)
            date_input_before = date_input.get_attribute('value')
        with allure.step("Open date picker"):
            date_input.click()
        with allure.step(f"Select month: {date.month}"):
            self.select_month_or_year(date.month, self.DateSelectMonth)
        with allure.step(f"Select year: {date.year}"):
            self.select_month_or_year(date.year, self.DateSelectYear)
        with allure.step(f"Select day: {date.day}"):
            self.element_is_clickable(self.get_date_selected_day_locator(date.day)).click()
        with allure.step("Read date from input after change"):
            date_input_result = date_input.get_attribute('value')
        return date_input_before, date_input_result

    @allure.step("Change date and time")
    def check_change_date_time(self):
        date = generated_date_time()
        with allure.step("Get current date-time from input"):
            date_input_before = self.element_is_presence(self.DateTimeInput).get_attribute('value')
        with allure.step("Open date-time picker"):
            self.safe_click(self.DateTimeInput)
        with allure.step("Open year selector"):
            self.element_is_clickable(self.DateTimeYear).click()
        with allure.step(f"Select year: {date.year}"):
            self.select_month_or_year_list(date.year, self.DateTimeYearList)
        with allure.step("Open month selector"):
            self.element_is_clickable(self.DateTimeMonth).click()
        with allure.step(f"Select month: {date.month}"):
            self.select_month_or_year_list(date.month, self.DateTimeMonthList)
        with allure.step(f"Select day: {date.day}"):
            self.element_is_clickable(self.get_date_selected_day_locator(date.day)).click()
        with allure.step(f"Select time: {date.time}"):
            self.select_month_or_year_list(date.time, self.DateTimeTimeList)
        with allure.step("Read date-time from input after change"):
            date_input_result = self.element_is_presence(self.DateTimeInput).get_attribute('value')
        return date_input_before, date_input_result


class SliderPage(BasePage):
    SliderButton = (By.XPATH, "//span[contains(text(), 'Slider')]")
    SliderInput = (By.XPATH, "//input[@class='range-slider range-slider--primary']")
    SliderValue = (By.ID, "sliderValue")

    @allure.step("Go to Slider page")
    def go_to_slider_page(self):
        self.scroll_to_element(self.SliderButton)
        self.element_is_clickable(self.SliderButton).click()

    @allure.step("Change slider value")
    def check_change_slider_value(self):
        with allure.step("Read slider value before change"):
            value_before = self.element_is_presence(self.SliderValue).get_attribute('value')
        slider_input = self.element_is_visible(self.SliderInput)
        offset = random.randint(0, 100)
        with allure.step(f"Drag slider by offset: {offset}"):
            self.action_drag_and_drop_by_offset(slider_input, offset, 0)
        with allure.step("Read slider value after change"):
            value_after = self.element_is_presence(self.SliderValue).get_attribute('value')
        return value_before, value_after


class ProgressBarPage(BasePage):
    ProgressBarButton = (By.XPATH, "//span[contains(text(), 'Progress Bar')]")
    ProgressBarValue = (By.XPATH, "//div[@class='progress-bar bg-info']")
    ProgressBarStart = (By.ID, "startStopButton")

    @allure.step("Go to Progress Bar page")
    def go_to_progress_bar_page(self):
        self.scroll_to_element(self.ProgressBarButton)
        self.element_is_clickable(self.ProgressBarButton).click()

    @allure.step("Change progress bar value")
    def check_change_progress_bar(self):
        with allure.step("Read progress value before change"):
            value_before = self.element_is_presence(self.ProgressBarValue).text
        with allure.step("Start progress bar"):
            self.element_is_clickable(self.ProgressBarStart).click()
        wait_sec = random.randint(2, 8)
        with allure.step(f"Wait for {wait_sec} seconds"):
            time.sleep(wait_sec)
        with allure.step("Stop progress bar"):
            self.element_is_clickable(self.ProgressBarStart).click()
        with allure.step("Read progress value after change"):
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

    @allure.step("Go to Tabs page")
    def go_to_tabs_page(self):
        self.scroll_to_element(self.TabsButton)
        self.element_is_clickable(self.TabsButton).click()

    @allure.step("Open tab: {tabs} and get text")
    def check_click_tab_and_get_text(self, tabs):
        tab_text = None
        try:
            with allure.step(f"Click tab '{tabs}'"):
                self.element_is_clickable(self.Tabs[tabs]['tab']).click()
            with allure.step("Read tab text"):
                tab_text = self.element_is_presence(self.Tabs[tabs]['text']).text
        except (TimeoutException, ElementClickInterceptedException):
            pass
        return tab_text, self.Tabs[tabs]['expected_text']


class ToolTipsPage(BasePage):
    ToolTipsButton = (By.XPATH, "//span[contains(text(), 'Tool Tips')]")
    ToolTipText = (By.CSS_SELECTOR, 'div[class="tooltip-inner"]')
    Elements = {
        'button': (By.ID, 'toolTipButton'),
        'field': (By.ID, 'toolTipTextField'),
        'contrary': (By.XPATH, '//*[.="Contrary"]'),
        'section': (By.XPATH, '//*[.="1.10.32"]'),
        'expected_text': {
            'button': 'You hovered over the Button',
            'field': 'You hovered over the text field',
            'contrary': 'You hovered over the Contrary',
            'section': 'You hovered over the 1.10.32',
        }

    }

    @allure.step("Go to Tool Tips page")
    def go_to_tool_tips_page(self):
        self.scroll_to_element(self.ToolTipsButton)
        self.element_is_clickable(self.ToolTipsButton).click()

    @allure.step("Show tooltip for '{element}' and get text")
    def get_tool_tip_text(self, element):
        try:
            with allure.step("Scroll to target element"):
                self.scroll_to_element(self.Elements[element])
            with allure.step("Find target element"):
                target = self.element_is_presence(self.Elements[element])
            with allure.step("Hover over target to show tooltip"):
                self.action_move_to_element(target)
            with allure.step("Read tooltip text"):
                text = self.element_is_visible(self.ToolTipText).text
            return text, self.Elements['expected_text'][element]
        except TimeoutException:
            return None, None


class MenuPage(BasePage):
    MenuButton = (By.XPATH, "//span[text()='Menu']")
    MenuLinks = (By.XPATH, "//ul[@id='nav']//li")

    @allure.step("Go to Menu page")
    def go_to_menu_page(self):
        self.scroll_to_element(self.MenuButton)
        self.element_is_clickable(self.MenuButton).click()

    @allure.step("Get all menu texts")
    def get_menu_texts(self):
        try:
            with allure.step("Read and hover all menu items"):
                menu_links = self.elements_are_presence(self.MenuLinks)
                text_links = []
                for link in menu_links:
                    self.driver.execute_script("arguments[0].scrollIntoView();", link)
                    self.action_move_to_element(link)
                    text_links.append(link.text)
            return text_links
        except (TimeoutException, ElementNotInteractableException):
            return []


class SelectMenuPage(BasePage):
    SelectMenuButton = (By.XPATH, "//span[text()='Select Menu']")
    SelectMenu = {
        'select_value_menu': {
            'input': (By.XPATH, "//input[@id='react-select-2-input']"),
            'text': (By.XPATH, "//div[@id='withOptGroup']//div[@class=' css-1uccc91-singleValue']")
        },
        'select_one_menu': {
            'input': (By.XPATH, "//input[@id='react-select-3-input']"),
            'text': (By.XPATH, "//div[@id='selectOne']//div[@class=' css-1uccc91-singleValue']")
        }

    }

    OldStyleSelectMenu = (By.XPATH, "//select[@id='oldSelectMenu']")

    MultiSelectDropDown = (By.XPATH, "//input[@id='react-select-4-input']")
    MultiSelectDropDownText = (By.XPATH, "//div[@class='css-12jo7m5']")
    StandardMultiSelect = (By.ID, "cars")

    @allure.step("Go to Select Menu page")
    def go_to_select_menu_page(self):
        try:
            with allure.step("Scroll to 'Select Menu' button"):
                self.scroll_to_element(self.SelectMenuButton)
            with allure.step("Click 'Select Menu' button"):
                self.element_is_clickable(self.SelectMenuButton).click()
        except TimeoutException:
            pass

    @allure.step("Select menu options from {type_menu}/{locator}")
    def get_selected_texts_for_menu(self, type_menu, locator):
        menu_list = generator_menu()
        type = {
            'value': menu_list.value_options_list,
            'one': menu_list.one_options_list
        }
        choice_option_list = type[type_menu]
        choice_option_text = []
        for option in choice_option_list:
            try:
                with allure.step(f"Select option '{option}' in {locator}"):
                    self.element_is_presence(self.SelectMenu[locator]['input']).send_keys(option)
                    self.element_is_presence(self.SelectMenu[locator]['input']).send_keys(Keys.ENTER)
                with allure.step("Read selected text from field"):
                    choice_option_text.append(self.element_is_visible(self.SelectMenu[locator]['text']).text)
            except TimeoutException:
                pass
        return choice_option_text, choice_option_list

    @allure.step("Verify old select menu options")
    def select_all_and_verify_texts(self):
        # pairs = [(opt.get_attribute("value"), opt.text) for opt in dropdown.options] # get all select pairs from dom
        pairs = generator_menu().old_select_menu_list
        comparisons = []
        try:
            with allure.step("Open old select menu"):
                dropdown = Select(self.element_is_presence(self.OldStyleSelectMenu))
            for value, expected_text in pairs:
                try:
                    with allure.step(f"Select value '{value}' and verify text"):
                        dropdown.select_by_value(value)
                        comparisons.append((dropdown.first_selected_option.text, expected_text))
                except NoSuchElementException:
                    pass
        except TimeoutException:
            pass
        return comparisons, pairs

    @allure.step("Select multiselect options and verify")
    def get_selected_text_for_multiselect_menu(self):
        choice_multiselect_list = generator_menu().multiselect_menu_list
        dropdown = self.element_is_presence(self.MultiSelectDropDown)
        for item in choice_multiselect_list:
            try:
                with allure.step(f"Select multiselect option '{item}'"):
                    dropdown.send_keys(item)
                    dropdown.send_keys(Keys.ENTER)
            except (TimeoutException, NoSuchElementException) as exc:
                with allure.step(
                        f"[INFO] In multiselect menu an {item} was not chose"
                        f"({type(exc).__name__}: {exc})"
                ):
                    pass

        with allure.step("Read selected texts from multiselect UI"):
            choice_dropdown_list = self.elements_are_presence(self.MultiSelectDropDownText)
            choice_dropdown_text = [item.text for item in choice_dropdown_list]
        return choice_dropdown_text, choice_multiselect_list

    @allure.step("Select standard options and verify")
    def get_selected_text_for_select_menu(self):
        choice_standard_select_list = generator_menu().standard_select_menu_list
        dropdown = Select(self.element_is_presence(self.StandardMultiSelect))
        for item in choice_standard_select_list:
            try:
                with allure.step(f"Select '{item}' in standard select"):
                    dropdown.select_by_value(item.lower())
            except (TimeoutException, NoSuchElementException) as exc:
                with allure.step(
                        f"[INFO] In standard multiselect menu an {item} was not chose"
                        f"({type(exc).__name__}: {exc})"
                ):
                    pass

        with allure.step("Read selected texts from standard select UI"):
            choice_dropdown_text = [item.text for item in dropdown.all_selected_options]
        return choice_dropdown_text, choice_standard_select_list
