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

    class TestSelectablePage(BaseTestPage):
        @pytest.mark.positive
        def test_go_to_selectable_page(self, driver):
            self.get_selectable_page(driver)
            assert "selectable" in driver.current_url.lower(), 'The transition to the Selectable page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize(
            "count, locator_button, locator_items, locator_items_active",
            [
                (1, 'list_button', 'list_item', 'list_item_active'),
                (2, 'list_button', 'list_item', 'list_item_active'),
                (3, 'list_button', 'list_item', 'list_item_active'),
                (1, 'grid_button', 'grid_item', 'grid_item_active'),
                (2, 'grid_button', 'grid_item', 'grid_item_active'),
                (3, 'grid_button', 'grid_item', 'grid_item_active'),
            ]
        )
        def test_selected_items_match_active(self, driver, count, locator_button, locator_items, locator_items_active):
            selectable_page = self.get_selectable_page(driver)
            clicked_items = selectable_page.click_random_items(count, locator_button, locator_items)
            active_items = selectable_page.get_active_items(locator_items_active)
            assert clicked_items == active_items, 'Elements were not selected'

    class TestResizablePage(BaseTestPage):
        @pytest.mark.positive
        def test_initial_size(self, driver):
            resizable_page = self.get_resizable_page(driver)
            width, height = resizable_page.get_size()
            assert (width, height) == (200, 200), "The initial size should be 200x200 px"

        @pytest.mark.positive
        def test_resize_to_maximum(self, driver):
            resizable_page = self.get_resizable_page(driver)
            width, height = resizable_page.resize_to_maximum()
            assert (width, height) == (500, 300), "The max size should be 500x300 px"

        @pytest.mark.positive
        def test_resize_to_minimum(self, driver):
            resizable_page = self.get_resizable_page(driver)
            width, height = resizable_page.resize_to_minimum()
            assert (width, height) == (150, 150), "The min size should be 150x150 px"

        @pytest.mark.positive
        def test_resize_dynamic(self, driver):
            resizable_page = self.get_resizable_page(driver)
            resizable_page.resize(50, 50)
            width, height = resizable_page.get_size()
            assert 150 <= width <= 500 and 150 <= height <= 300, \
                "The size should stay within acceptable limits"
