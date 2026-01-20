from page_objects.alerts_frame_windows import *
from page_objects.elements import *
from page_objects.forms import *
from page_objects.interactions import SortablePage
from page_objects.main_page import MainPage
from page_objects.widgets import *


class BaseTestPage:
    ElementsPageUrl = "https://demoqa.com/elements"
    FormsPageUrl = "https://demoqa.com/forms"
    AlertsFrameWindowsPageUrl = "https://demoqa.com/alertsWindows"
    MainPageUrl = "https://demoqa.com/"
    WidgetsPageUrl = "https://demoqa.com/widgets"
    InteractionsPageUrl = "https://demoqa.com/interaction"

    # region important
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
    # endregion
    def get_main_page(self, driver):
        page = MainPage(driver, self.MainPageUrl)
        page.open()
        return page

    # Elements Page
    def get_elements_page(self, page_class, driver):
        page = page_class(driver, self.ElementsPageUrl)
        page.open()
        return page

    def radio_button_get_page(self, driver):
        radio_button_page = self.get_elements_page(RadioButtonPage, driver)
        radio_button_page.go_to_radio_button()
        return radio_button_page

    def check_box_get_page(self, driver):
        check_box_page = self.get_elements_page(CheckBoxPage, driver)
        check_box_page.go_to_check_box()
        return check_box_page

    def text_box_get_page(self, driver):
        text_box_page = self.get_elements_page(TextBoxPage, driver)
        text_box_page.go_to_text_box()
        return text_box_page

    def text_box_page_submit_and_validate(self, driver, person):
        page = self.text_box_get_page(driver)
        page.text_box_submit_form(person)
        return page.get_info_from_text_box_form()

    def web_table_get_page(self, driver):
        web_table_page = self.get_elements_page(WebTablePage, driver)
        web_table_page.go_to_web_table_page()
        return web_table_page

    def buttons_get_page(self, driver):
        buttons_page = self.get_elements_page(ButtonsPage, driver)
        buttons_page.go_to_buttons_page()
        return buttons_page

    def links_get_page(self, driver):
        links_page = self.get_elements_page(LinksPage, driver)
        links_page.go_to_links_page()
        return links_page

    def upload_download_get_page(self, driver):
        upload_download_page = self.get_elements_page(UploadDownloadPage, driver)
        upload_download_page.go_to_upload_download_page()
        return upload_download_page

    def dynamic_properties_get_page(self, driver):
        dynamic_properties_page = self.get_elements_page(DynamicPropertiesPage, driver)
        dynamic_properties_page.go_to_dynamic_properties_page()
        return dynamic_properties_page

    # Forms Page
    def get_forms_page(self, page_class, driver):
        page = page_class(driver, self.FormsPageUrl)
        page.open()
        return page

    def practice_form_get_page(self, driver):
        forms_page = self.get_forms_page(FormsPage, driver)
        forms_page.go_to_practice_form()
        return forms_page

    # AlertsFrameWindows Page
    def get_alerts_frame_windows_page(self, page_class, driver):
        page = page_class(driver, self.AlertsFrameWindowsPageUrl)
        page.open()
        return page

    def browser_windows_get_page(self, driver):
        browser_windows_page = self.get_alerts_frame_windows_page(BrowserWindowsPage, driver)
        browser_windows_page.go_to_browser_windows_page()
        return browser_windows_page

    def alerts_get_page(self, driver):
        alerts_page = self.get_alerts_frame_windows_page(AlertsPage, driver)
        alerts_page.go_to_alerts_page()
        return alerts_page

    def frames_get_page(self, driver):
        frames_page = self.get_alerts_frame_windows_page(FramesPage, driver)
        frames_page.go_to_frames_page()
        return frames_page

    def nested_frames_get_page(self, driver):
        nested_frames_page = self.get_alerts_frame_windows_page(NestedFramesPage, driver)
        nested_frames_page.go_to_nested_frames_page()
        return nested_frames_page

    def modal_dialogs_get_page(self, driver):
        nested_frames_page = self.get_alerts_frame_windows_page(ModalDialogsPage, driver)
        nested_frames_page.go_to_modal_dialogs_page()
        return nested_frames_page

    # Widgets
    def get_widgets_page(self, page_class, driver):
        page = page_class(driver, self.WidgetsPageUrl)
        page.open()
        return page

    def get_accordion_page(self, driver):
        accordion_page = self.get_widgets_page(AccordionPage, driver)
        accordion_page.go_to_accordion_page()
        return accordion_page

    def get_auto_complete_page(self, driver):
        auto_complete_page = self.get_widgets_page(AutoCompletePage, driver)
        auto_complete_page.go_to_auto_complete_page()
        return auto_complete_page

    def get_date_picker_page(self, driver):
        date_picker_page = self.get_widgets_page(DatePickerPage, driver)
        date_picker_page.go_to_date_picker_page()
        return date_picker_page

    def get_slider_page(self, driver):
        slider_page = self.get_widgets_page(SliderPage, driver)
        slider_page.go_to_slider_page()
        return slider_page

    def get_progress_bar_page(self, driver):
        progress_bar_page = self.get_widgets_page(ProgressBarPage, driver)
        progress_bar_page.go_to_progress_bar_page()
        return progress_bar_page

    def get_tabs_page(self, driver):
        tabs_page = self.get_widgets_page(TabsPage, driver)
        tabs_page.go_to_tabs_page()
        return tabs_page

    def get_tool_tips_page(self, driver):
        tool_tips_page = self.get_widgets_page(ToolTipsPage, driver)
        tool_tips_page.go_to_tool_tips_page()
        return tool_tips_page

    def get_menu_page(self, driver):
        menu_page = self.get_widgets_page(MenuPage, driver)
        menu_page.go_to_menu_page()
        return menu_page

    def get_select_menu_page(self, driver):
        select_menu_page = self.get_widgets_page(SelectMenuPage, driver)
        select_menu_page.go_to_select_menu_page()
        return select_menu_page

    # Interactions
    def get_interactions_page(self, page_class, driver):
        page = page_class(driver, self.InteractionsPageUrl)
        page.open()
        return page

    def get_sortable_page(self, driver):
        sortable_page = self.get_interactions_page(SortablePage, driver)
        sortable_page.go_to_sortable_page()
        return sortable_page
