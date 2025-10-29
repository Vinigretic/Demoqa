from page_objects.elements import *


class BaseTestPage:
    ElementsPageUrl = "https://demoqa.com/elements"
    # def text_box_page_create(self, driver):
    #     text_box_page = TextBoxPage(driver, self.ElementsPageUrl)
    #     text_box_page.open()
    #     text_box_page.go_to_text_box()
    #     return text_box_page
    #
    # def text_box_page_submit_and_validate(self, driver, person):
    #     page = self.text_box_page_create(driver)
    #     page.text_box_submit_form(person)
    #     return page.get_info_from_text_box_form()

    # def check_box_page_create(self, driver):
    #     check_box_page = CheckBoxPage(driver, self.ElementsPageUrl)
    #     check_box_page.open()
    #     check_box_page.go_to_check_box()
    #     return check_box_page

    def get_page(self, page_class, driver):
        page =  page_class(driver, self.ElementsPageUrl)
        page.open()
        return page

    def radio_button_get_page(self, driver):
        radio_button_page = self.get_page(RadioButtonPage, driver)
        radio_button_page.go_to_radio_button()
        return radio_button_page

    def check_box_get_page(self, driver):
        check_box_page = self.get_page(CheckBoxPage, driver)
        check_box_page.go_to_check_box()
        return check_box_page

    def text_box_get_page(self, driver):
        text_box_page = self.get_page(TextBoxPage, driver)
        text_box_page.go_to_text_box()
        return text_box_page

    def text_box_page_submit_and_validate(self, driver, person):
        page = self.text_box_get_page(driver)
        page.text_box_submit_form(person)
        return page.get_info_from_text_box_form()

    def web_table_get_page(self, driver):
        web_table_page = self.get_page(WebTablePage, driver)
        web_table_page.go_to_web_table_page()
        return web_table_page

    def buttons_get_page(self, driver):
        buttons_page = self.get_page(ButtonsPage, driver)
        buttons_page.go_to_buttons_page()
        return buttons_page

    def links_get_page(self, driver):
        links_page = self.get_page(LinksPage, driver)
        links_page.go_to_links_page()
        return links_page