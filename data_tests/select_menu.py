from dataclasses import dataclass

@dataclass
class SelectMenu:
    value_options_list: list = None
    one_options_list: list = None
    old_select_menu_list: list = None
    multiselect_menu_list:list = None
    standard_select_menu_list:list = None