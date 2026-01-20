import random
import time

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
