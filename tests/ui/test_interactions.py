import pytest
import allure

from tests.base.base_test_page import BaseTestPage


# region important
# endregion

@allure.suite("Interactions")
class TestInteractionsPage:
    @allure.feature("Sortable")
    class TestSortablePage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigate to Sortable page")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Open Sortable page")
        def test_go_to_sortable_page(self, driver):
            self.get_sortable_page(driver)
            assert "sortable" in driver.current_url.lower(), 'The transition to the Sortable page failed'

        @pytest.mark.positive
        @pytest.mark.parametrize('locator_button, locator_items',
                                 (('list_button', 'list_item'), ('grid_button', 'grid_item')))
        @allure.story("Change order of items")
        @allure.severity(allure.severity_level.NORMAL)
        @allure.title("Change order on Sortable")
        def test_change_sortable_list(self, driver, locator_button, locator_items):
            sortable_page = self.get_sortable_page(driver)
            items_list_before, items_change, items_list_after = sortable_page.change_list_orders(
                locator_button,
                locator_items
            )
            assert items_list_after != items_list_before, 'The order of list was not changed'
            assert items_list_after.index(items_change[0].text) != items_list_before.index(
                items_change[0].text), 'The order of list was not changed'

    @allure.feature("Selectable")
    class TestSelectablePage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigate to Selectable page")
        @allure.severity(allure.severity_level.CRITICAL)
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
        @allure.story("Select items and validate active state")
        @allure.severity(allure.severity_level.NORMAL)
        def test_selected_items_match_active(self, driver, count, locator_button, locator_items, locator_items_active):
            allure.dynamic.title(f"Select {count} item(s) in {locator_button} and verify active state")
            selectable_page = self.get_selectable_page(driver)
            clicked_items = selectable_page.click_random_items(count, locator_button, locator_items)
            active_items = selectable_page.get_active_items(locator_items_active)
            assert clicked_items == active_items, 'Elements were not selected'

    @allure.feature("Resizable")
    class TestResizablePage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigate to Resizable page")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Open Resizable page")
        def test_go_to_resizable_page(self, driver):
            self.get_resizable_page(driver)
            assert "resizable" in driver.current_url.lower(), 'The transition to the Resizable page failed'

        @pytest.mark.positive
        @allure.story("Verify initial size")
        @allure.severity(allure.severity_level.MINOR)
        @allure.title("Resizable initial size is 200x200")
        def test_initial_size(self, driver):
            resizable_page = self.get_resizable_page(driver)
            width, height = resizable_page.get_size()
            assert (width, height) == (200, 200), "The initial size should be 200x200 px"

        @pytest.mark.positive
        @allure.story("Resize to maximum")
        @allure.severity(allure.severity_level.MINOR)
        @allure.title("Resize to the maximum size 500x300")
        def test_resize_to_maximum(self, driver):
            resizable_page = self.get_resizable_page(driver)
            width, height = resizable_page.resize_to_maximum()
            assert (width, height) == (500, 300), "The max size should be 500x300 px"

        @pytest.mark.positive
        @allure.story("Resize to minimum")
        @allure.severity(allure.severity_level.MINOR)
        @allure.title("Resize to the minimum size 150x150")
        def test_resize_to_minimum(self, driver):
            resizable_page = self.get_resizable_page(driver)
            width, height = resizable_page.resize_to_minimum()
            assert (width, height) == (150, 150), "The min size should be 150x150 px"

        @pytest.mark.positive
        @allure.story("Resize dynamically within constraints")
        @allure.severity(allure.severity_level.MINOR)
        @allure.title("Dynamic resize stays within limits")
        def test_resize_dynamic(self, driver):
            resizable_page = self.get_resizable_page(driver)
            resizable_page.resize(50, 50)
            width, height = resizable_page.get_size()
            assert 150 <= width <= 500 and 150 <= height <= 300, \
                "The size should stay within acceptable limits"

    @allure.feature("Droppable")
    class TestDroppablePage(BaseTestPage):
        @pytest.mark.positive
        @allure.story("Navigate to Droppable page")
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.title("Open Droppable page")
        def test_go_to_droppable_page(self, driver):
            self.get_droppable_page(driver)
            assert "droppable" in driver.current_url.lower(), 'The transition to the Droppable page failed'

        @pytest.mark.positive
        @allure.story("Simple droppable action")
        @allure.severity(allure.severity_level.MINOR)
        @allure.title("Drag-and-drop simple element")
        def test_simple_droppable(self, driver):
            droppable_page = self.get_droppable_page(driver)
            assert droppable_page.get_drop_simple_text() == 'dropped!', "The elements was dropped"

        @pytest.mark.positive
        @allure.story("Accept droppable with valid element only")
        @allure.severity(allure.severity_level.MINOR)
        @allure.title("Droppable accept: only acceptable element is dropped")
        def test_accept_droppable(self, driver):
            droppable_page = self.get_droppable_page(driver)
            not_accept = droppable_page.get_drop_not_accept_text()
            accept = droppable_page.get_drop_accept_text()
            assert not_accept == 'drop here', "The dropped element was accepted"
            assert accept == 'dropped!', "The dropped element was not accepted"
