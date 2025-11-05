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
