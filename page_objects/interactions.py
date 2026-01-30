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


class ResizablePage(BasePage):
    ResizableButton = (By.XPATH, "//span[contains(text(), 'Resizable')]")
    ResizableBox = (By.ID, "resizableBoxWithRestriction")
    ResizableBoxHandle = (By.XPATH,
                          "//div[@id='resizableBoxWithRestriction']//span[@class='react-resizable-handle react-resizable-handle-se']")
    Resizable = (By.ID, "resizable")
    ResizableHandle = (By.XPATH,
                       "//div[@id='resizable']//span[@class='react-resizable-handle react-resizable-handle-se']")

    def go_to_resizable_page(self):
        self.safe_click(self.ResizableButton)

    def get_size(self):
        element = self.element_is_presence(self.ResizableBox)
        size = element.size
        print(size)
        return size['width'], size['height']

    def resize(self, x_offset, y_offset):
        handle = self.scroll_to_element(self.ResizableBoxHandle)
        self.action_drag_and_drop_by_offset(handle, x_offset, y_offset)

    def resize_to_maximum(self):
        self.resize(500, 300)
        return self.get_size()

    def resize_to_minimum(self):
        handle = self.scroll_to_element(self.ResizableBoxHandle)
        while True:
            width, height = self.get_size()
            print(width, height)
            if width <= 150 and height <= 150:
                break
            try:
                self.action_drag_and_drop_by_offset(handle, -10, -10)
            except Exception:
                break

        return self.get_size()


class Droppable(BasePage):
    DroppableButton = (By.XPATH, "//span[contains(text(), 'Droppable')]")
    # Simple
    SimpleTab = (By.CSS_SELECTOR, "a[id='droppableExample-tab-simple']")
    DragMeSimple = (By.CSS_SELECTOR, 'div[id="draggable"]')
    DropHereSimple = (By.CSS_SELECTOR, '#simpleDropContainer #droppable')

    # Accept
    AcceptTab = (By.CSS_SELECTOR, "a[id='droppableExample-tab-accept']")
    Acceptable = (By.CSS_SELECTOR, 'div[id="acceptable"]')
    NotAcceptable = (By.CSS_SELECTOR, 'div[id="notAcceptable"]')
    DropHereAccept = (By.CSS_SELECTOR, '#acceptDropContainer #droppable')

    # Prevent Propogation
    PreventTab = (By.CSS_SELECTOR, "a[id='droppableExample-tab-preventPropogation']")
    NotGreedyDropBoxText = (By.CSS_SELECTOR, 'div[id="notGreedyDropBox"] p:nth-child(1)')
    NotGreedyInnerBox = (By.CSS_SELECTOR, 'div[id="notGreedyInnerDropBox"]')
    GreedyDropBoxText = (By.CSS_SELECTOR, 'div[id="greedyDropBox"] p:nth-child(1)')
    GreedyInerBox = (By.CSS_SELECTOR, 'div[id="greedyDropBoxInner"]')
    DragMePrevent = (By.CSS_SELECTOR, '#ppDropContainer #dragBox')

    # Revert Draggable
    RevertTab = (By.CSS_SELECTOR, "a[id='droppableExample-tab-revertable']")
    WillRevert = (By.CSS_SELECTOR, 'div[id="revertable"]')
    NotRevert = (By.CSS_SELECTOR, 'div[id="notRevertable"]')
    DropHereRevert = (By.CSS_SELECTOR, '#revertableDropContainer #droppable')

    def go_to_droppable_page(self):
        self.safe_click(self.DroppableButton)

    def get_drop_simple_text(self):
        self.element_is_visible(self.SimpleTab).click()
        drag_div = self.element_is_visible(self.DragMeSimple)
        drop_div = self.element_is_visible(self.DropHereSimple)
        self.action_drag_and_drop_to_element(drag_div, drop_div)
        return drop_div.text.lower().strip()

    def get_drop_not_accept_text(self):
        self.element_is_visible(self.AcceptTab).click()
        not_acceptable_div = self.element_is_visible(self.NotAcceptable)
        drop_div = self.element_is_visible(self.DropHereAccept)
        self.action_drag_and_drop_to_element(not_acceptable_div, drop_div)
        return drop_div.text.lower().strip()

    def get_drop_accept_text(self):
        self.element_is_visible(self.AcceptTab).click()
        acceptable_div = self.element_is_visible(self.Acceptable)
        drop_div = self.element_is_visible(self.DropHereAccept)
        self.action_drag_and_drop_to_element(acceptable_div, drop_div)
        return drop_div.text.lower().strip()
