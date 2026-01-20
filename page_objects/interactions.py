import random

from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage


class SortablePage(BasePage):
    SortableButton = (By.XPATH, "//span[contains(text(), 'Sortable')]")
    Locators = {
        'list_button': (By.ID, "demo-tab-list"),
        'grid_button': (By.ID, "demo-tab-grid"),
        'list_item': (By.XPATH,
                      "//div[@class='vertical-list-container mt-4']/div[@class='list-group-item list-group-item-action']"),
        'grid_item': (By.XPATH,
                      "//div[@class='grid-container mt-4']//div[@class='list-group-item list-group-item-action']"),
    }

    def go_to_sortable_page(self):
        self.safe_click(self.SortableButton)

    def get_items_text(self, locator_button, locator_items):
        self.element_is_visible(self.Locators[locator_button]).click()
        sortable_items = self.elements_are_presence(self.Locators[locator_items])
        return [item.text for item in sortable_items]

    def change_list_orders(self, locator_button, locator_items):
        items_list_before = self.get_items_text(locator_button, locator_items)
        items_change = random.sample(self.elements_are_presence(self.Locators[locator_items]), k=2)
        self.action_drag_and_drop_to_element(items_change[0], items_change[1])
        items_list_after = self.get_items_text(locator_button, locator_items)
        return items_list_before, items_change, items_list_after


class SelectablePage(BasePage):
    SelectableButton = (By.XPATH, "//span[contains(text(), 'Selectable')]")

    def go_to_selectable_page(self):
        self.safe_click(self.SelectableButton)

    Locators = {
        'list_button': (By.ID, "demo-tab-list"),
        'grid_button': (By.ID, "demo-tab-grid"),
        'list_item': (By.XPATH, "//li[@class='mt-2 list-group-item list-group-item-action']"),
        'grid_item': (By.XPATH, "//li[@class='list-group-item list-group-item-action']"),
        'list_item_active': (By.XPATH, "//li[@class='mt-2 list-group-item active list-group-item-action']"),
        'grid_item_active': (By.XPATH, "//li[@class='list-group-item active list-group-item-action']"),
    }

    def click_random_items(self, count, locator_button, locator_items):
        try:
            self.element_is_visible(self.Locators[locator_button]).click()
        except Exception as e:
            raise RuntimeError(f"Failed to click item: {e}")

        all_items = self.elements_are_presence(self.Locators[locator_items])
        if len(all_items) < count:
            raise ValueError(f"Requested {count} items, but only {len(all_items)} found")
        list_items = random.sample(all_items, k=count)

        clicked_items = []
        for item in list_items:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                           item)
                self.element_is_clickable(item).click()
                clicked_items.append(item.text)
            except Exception as e:
                raise RuntimeError(f"Failed to click item {item.text}: {e}")
        return sorted(clicked_items)

    def get_active_items(self, locator_items_active):
        list_items = self.elements_are_presence(self.Locators[locator_items_active])
        active_items = [item.text for item in list_items]
        return sorted(active_items)
