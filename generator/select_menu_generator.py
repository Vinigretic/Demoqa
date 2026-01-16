from data_tests.select_menu import SelectMenu


def generator_menu():
    return SelectMenu(
        value_options_list=["Group 1, option 1", "Group 1, option 2", "Group 2, option 1", "Group 2, option 2",
                            "A root option", "Another root option"],
        one_options_list=["Dr.", "Mr.", "Mrs.", "Ms.", "Prof.", "Other"],
        old_select_menu_list=[('red', 'Red'), ('1', 'Blue'), ('2', 'Green'), ('3', 'Yellow'), ('4', 'Purple'),
                              ('5', 'Black'), ('6', 'White'), ('7', 'Voilet'), ('8', 'Indigo'), ('9', 'Magenta'),
                              ('10', 'Aqua')],
        multiselect_menu_list=['Green', 'Blue', 'Black', 'Red'],
        standard_select_menu_list=['Volvo', 'Saab', 'Opel', 'Audi']

    )
