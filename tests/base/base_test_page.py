from page_objects.elements import TextBoxPage


class BaseTestPage:
    def text_box_page_create(self, driver):
        text_box_page = TextBoxPage(driver, "https://demoqa.com/elements")
        text_box_page.open()
        text_box_page.go_to_text_box()
        return text_box_page

    def text_box_page_submit_and_validate(self, driver, person):
        page = self.text_box_page_create(driver)
        page.text_box_submit_form(person)
        return page.get_info_from_text_box_form()
