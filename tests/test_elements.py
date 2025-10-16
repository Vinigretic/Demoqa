from data_tests.main_page import MainPage


class TestMainPage:

    def test_go_to_elements(self, driver):
        elements = MainPage(driver, "https://demoqa.com/")
        elements.open()
        elements.go_to_elements()
        assert "elements" in driver.current_url.lower()
