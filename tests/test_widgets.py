import pytest

from tests.base.base_test_page import BaseTestPage


class TestWidgetsPage:
    class TestAccordionPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_accordion_page(self, driver):
            self.get_accordion_page(driver)
            assert "accordian" in driver.current_url.lower(), 'The transition to the Accordian page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize("section_name", ["first", "second", "third"])
        def test_check_accordion(self, driver, section_name):
            accordion_page = self.get_accordion_page(driver)
            open_click_result, content, close_click_result, content_result = accordion_page.check_accordion(
                section_name)
            assert open_click_result == 'collapse show', 'The accordion is not opened'
            assert content_result in content, 'The accordion content is not present'
            assert close_click_result == 'collapse', 'The accordion is not closed'

    class TestAutoCompletePage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_auto_complete_page(self, driver):
            self.get_auto_complete_page(driver)
            assert "auto-complete" in driver.current_url.lower(), 'The transition to the Auto Complete page failed'

        @pytest.mark.parametrize('quantity_color', [1, 3, 5])
        def test_check_fill_multi_input(self, driver, quantity_color):
            auto_complete_page = self.get_auto_complete_page(driver)
            list_color_result, list_color_input = auto_complete_page.check_fill_multi_input(quantity_color)
            assert list_color_result == list_color_input, ('The colors of the input data do not match the colors of '
                                                           'the results.')

        @pytest.mark.positive
        @pytest.mark.parametrize('quantity_color, element', ((1, 'single'), (3, 'single'), (5, 'single'), (4, 'all')))
        def test_check_delete_multi_input(self, driver, quantity_color, element):
            auto_complete_page = self.get_auto_complete_page(driver)
            auto_complete_page.check_fill_multi_input(quantity_color)
            result = auto_complete_page.check_delete_multi_input(element)
            assert result is True, 'The colors were not deleted'

        @pytest.mark.positive
        def test_check_fill_single_input(self, driver):
            auto_complete_page = self.get_auto_complete_page(driver)
            color_result, color = auto_complete_page.check_fill_single_input()
            assert color_result == color, 'The color was not input'

    class TestDatePickerPage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_date_picker_page(self, driver):
            self.get_date_picker_page(driver)
            assert "date-picker" in driver.current_url.lower(), 'The transition to the Date Picker page failed'

        @pytest.mark.positive
        def test_check_change_date(self, driver):
            date_picker_page = self.get_date_picker_page(driver)
            date_input_before, date_input_result = date_picker_page.check_change_date()
            assert date_input_before != date_input_result, 'The date has not been changed'

        @pytest.mark.positive
        def test_check_change_date_time(self, driver):
            date_picker_page = self.get_date_picker_page(driver)
            date_input_before, date_input_result = date_picker_page.check_change_date_time()
            assert date_input_before != date_input_result, 'The date has not been changed'

    class TestSliderPage(BaseTestPage):
        @pytest.mark.positive
        def test_get_slider_page(self, driver):
            self.get_slider_page(driver)
            assert "slider" in driver.current_url.lower(), 'The transition to the Slider page failed'

        @pytest.mark.positive
        def test_check_change_slider_value(self, driver):
            slider_page = self.get_slider_page(driver)
            value_before, value_after = slider_page.check_change_slider_value()
            assert value_after != value_before, 'The slider value was not changed'

    class TestProgressBarPage(BaseTestPage):
        @pytest.mark.positive
        def test_get_progress_bar_page(self, driver):
            self.get_progress_bar_page(driver)
            assert "progress-bar" in driver.current_url.lower(), 'The transition to the Progress bar page failed'

        @pytest.mark.positive
        def test_check_change_progress_bar(self, driver):
            progress_bar_page = self.get_progress_bar_page(driver)
            value_before, value_after = progress_bar_page.check_change_progress_bar()
            assert value_after != value_before, 'The progress bar value was not changed'
