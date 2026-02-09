import pytest
import allure

from tests.base.base_test_page import BaseTestPage


@allure.suite("Widgets")
class TestWidgetsPage:
    @allure.feature("Accordion")
    class TestAccordionPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Accordion page")
        def test_go_to_accordion_page(self, driver):
            self.get_accordion_page(driver)
            assert "accordian" in driver.current_url.lower(), 'The transition to the Accordian page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize("section_name", ["first", "second", "third"])
        @allure.story("Accordion")
        @allure.severity(allure.severity_level.NORMAL)
        def test_check_accordion(self, driver, section_name):
            allure.dynamic.title(f"Toggle '{section_name}' section and verify content")
            accordion_page = self.get_accordion_page(driver)
            open_click_result, content, close_click_result, content_result = accordion_page.check_accordion(
                section_name)
            assert open_click_result == 'collapse show', 'The accordion is not opened'
            assert content_result in content, 'The accordion content is not present'
            assert close_click_result == 'collapse', 'The accordion is not closed'

    @allure.feature("Auto Complete")
    class TestAutoCompletePage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Auto Complete page")
        def test_go_to_auto_complete_page(self, driver):
            self.get_auto_complete_page(driver)
            assert "auto-complete" in driver.current_url.lower(), 'The transition to the Auto Complete page failed'

        @pytest.mark.parametrize('quantity_color', [1, 3, 5])
        @allure.story("Auto complete")
        @allure.severity(allure.severity_level.NORMAL)
        def test_check_fill_multi_input(self, driver, quantity_color):
            allure.dynamic.title(f"Fill multi input with {quantity_color} colors")
            auto_complete_page = self.get_auto_complete_page(driver)
            list_color_result, list_color_input = auto_complete_page.check_fill_multi_input(quantity_color)
            assert list_color_result == list_color_input, ('The colors of the input data do not match the colors of '
                                                           'the results.')

        @pytest.mark.positive
        @pytest.mark.parametrize('quantity_color, element', ((1, 'single'), (3, 'single'), (5, 'single'), (4, 'all')))
        @allure.story("Auto complete")
        @allure.severity(allure.severity_level.NORMAL)
        def test_check_delete_multi_input(self, driver, quantity_color, element):
            allure.dynamic.title(f"Delete '{element}' after {quantity_color} colors")
            auto_complete_page = self.get_auto_complete_page(driver)
            auto_complete_page.check_fill_multi_input(quantity_color)
            result = auto_complete_page.check_delete_multi_input(element)
            assert result is True, 'The colors were not deleted'

        @pytest.mark.positive
        @allure.story("Auto complete")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Fill single input")
        def test_check_fill_single_input(self, driver):
            auto_complete_page = self.get_auto_complete_page(driver)
            color_result, color = auto_complete_page.check_fill_single_input()
            assert color_result == color, 'The color was not input'

    @allure.feature("Date Picker")
    class TestDatePickerPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Date Picker page")
        def test_go_to_date_picker_page(self, driver):
            self.get_date_picker_page(driver)
            assert "date-picker" in driver.current_url.lower(), 'The transition to the Date Picker page failed'

        @pytest.mark.positive
        @allure.story("Date change")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Change date")
        def test_check_change_date(self, driver):
            date_picker_page = self.get_date_picker_page(driver)
            date_input_before, date_input_result = date_picker_page.check_change_date()
            assert date_input_before != date_input_result, 'The date has not been changed'

        @pytest.mark.positive
        @allure.story("Date-time change")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Change date and time")
        def test_check_change_date_time(self, driver):
            date_picker_page = self.get_date_picker_page(driver)
            date_input_before, date_input_result = date_picker_page.check_change_date_time()
            assert date_input_before != date_input_result, 'The date has not been changed'

    @allure.feature("Slider")
    class TestSliderPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Slider page")
        def test_get_slider_page(self, driver):
            self.get_slider_page(driver)
            assert "slider" in driver.current_url.lower(), 'The transition to the Slider page failed'

        @pytest.mark.positive
        @allure.story("Slider")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Change slider value")
        def test_check_change_slider_value(self, driver):
            slider_page = self.get_slider_page(driver)
            value_before, value_after = slider_page.check_change_slider_value()
            assert value_after != value_before, 'The slider value was not changed'

    @allure.feature("Progress Bar")
    class TestProgressBarPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Progress Bar page")
        def test_get_progress_bar_page(self, driver):
            self.get_progress_bar_page(driver)
            assert "progress-bar" in driver.current_url.lower(), 'The transition to the Progress bar page failed'

        @pytest.mark.positive
        @allure.story("Progress bar")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Change progress bar value")
        def test_check_change_progress_bar(self, driver):
            progress_bar_page = self.get_progress_bar_page(driver)
            value_before, value_after = progress_bar_page.check_change_progress_bar()
            assert value_after != value_before, 'The progress bar value was not changed'

    @allure.feature("Tabs")
    class TestTabsPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Tabs page")
        def test_get_tabs_page(self, driver):
            self.get_tabs_page(driver)
            assert "tabs" in driver.current_url.lower(), 'The transition to the Tabs page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize('tabs', ('what', 'origin', 'use', 'more'))
        @allure.story("Tabs")
        @allure.severity(allure.severity_level.NORMAL)
        def test_check_click_tab_and_get_text(self, driver, tabs):
            allure.dynamic.title(f"Open tab '{tabs}' and verify text")
            tabs_page = self.get_tabs_page(driver)
            tab_text, expected_text = tabs_page.check_click_tab_and_get_text(tabs)
            assert tab_text is not None, 'The Tab is not clickable'
            assert tab_text.startswith(expected_text), 'The Text does not match'

    @allure.feature("Tool Tips")
    class TestToolTipsPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Tool Tips page")
        def test_get_tool_tips_page(self, driver):
            self.get_tool_tips_page(driver)
            assert "tool-tips" in driver.current_url.lower(), 'The transition to the Tool Tips page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize('element', ('button', 'field', 'contrary', 'section'))
        @allure.story("Tool tips")
        @allure.severity(allure.severity_level.NORMAL)
        def test_get_tool_tip_text(self, driver, element):
            allure.dynamic.title(f"Show tooltip for '{element}'")
            tool_tips_page = self.get_tool_tips_page(driver)
            text, expected_text = tool_tips_page.get_tool_tip_text(element)
            assert text, 'The tool tip was not shown'
            assert expected_text == text, 'The tool tip text does not match'

    @allure.feature("Menu")
    class TestMenuPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Menu page")
        def test_get_menu_page(self, driver):
            self.get_menu_page(driver)
            assert "menu" in driver.current_url.lower(), 'The transition to the Menu page failed'

        @pytest.mark.positive
        @allure.story("Menu")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Get all menu texts")
        def test_get_menu_texts(self, driver):
            menu_page = self.get_menu_page(driver)
            length = len(menu_page.get_menu_texts())
            assert length == 8, 'Menu items do not exist or have not been selected'

    @allure.feature("Select Menu")
    class TestSelectMenuPage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigation")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Navigate to Select Menu page")
        def test_get_select_menu_page(self, driver):
            self.get_select_menu_page(driver)
            assert "select-menu" in driver.current_url.lower(), 'The transition to the Selectmenu page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize('type_meny, locator', (('value', 'select_value_menu'), ('one', 'select_one_menu')))
        @allure.story("Select menu")
        @allure.severity(allure.severity_level.NORMAL)
        def test_check_select_value_menu(self, driver, type_meny, locator):
            allure.dynamic.title(f"Select from {type_meny}")
            select_menu_page = self.get_select_menu_page(driver)
            choice_option_text, choice_option_list = select_menu_page.get_selected_texts_for_menu(type_meny, locator)
            assert choice_option_text == choice_option_list, 'The text does not match'

        @pytest.mark.positive
        @allure.story("Select menu")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Verify old select menu options")
        def test_check_old_select_menu(self, driver):
            select_menu_page = self.get_select_menu_page(driver)
            comparisons, pairs = select_menu_page.select_all_and_verify_texts()
            assert comparisons, 'The Select Menu was not presented'
            assert len(pairs) == len(comparisons), 'Some option was not presented in the dropdown'
            for actual_text, expected_text in comparisons:
                assert actual_text == expected_text, f"Expected '{expected_text}', does not match with '{actual_text}'"

        @pytest.mark.positive
        @allure.story("Select menu")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Multiselect dropdown menu displays selected items")
        def test_multiselect_dropdown_menu(self, driver, request):
            select_menu_page = self.get_select_menu_page(driver)
            choice_dropdown_text, choice_multiselect_list = select_menu_page.get_selected_text_for_multiselect_menu()
            assert choice_dropdown_text == choice_multiselect_list, f'The text does not match in {request.node.name}'

        @pytest.mark.positive
        @allure.story("Select menu")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Standard select dropdown displays selected items")
        def test_standard_select_dropdown_menu(self, driver, request):
            select_menu_page = self.get_select_menu_page(driver)
            choice_dropdown_text, choice_standard_select_list = select_menu_page.get_selected_text_for_select_menu()
            assert choice_dropdown_text == choice_standard_select_list, f'The text does not match in {request.node.name}'
