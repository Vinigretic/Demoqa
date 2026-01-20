import pytest

from tests.base.base_test_page import BaseTestPage


# region important
# endregion

class TestInteractionsPage:
    class TestSortablePage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_sortable_page(self, driver):
            self.get_sortable_page(driver)
            assert "sortable" in driver.current_url.lower(), 'The transition to the Sortable page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize('locator_button, locator_items',
                                 (('list_button', 'list_item'), ('grid_button', 'grid_item')))
        def test_change_sortable_list(self, driver, locator_button, locator_items):
            sortable_page = self.get_sortable_page(driver)
            items_list_before, items_change, items_list_after = sortable_page.change_list_orders(locator_button,
                                                                                                 locator_items)
            assert items_list_after != items_list_before, 'The order of list was not changed'
            assert items_list_after.index(items_change[0].text) != items_list_before.index(
                items_change[0].text), 'The order of list was not changed'
