from typing import List
from cmd_ui.control import Control
from os import system

class Interface:
    items = ['']
    title = ''
    item_focus_index = 0

    def __init__(self, items: List[str], title = ''):
        self.items = items
        self.title = title

        if self.title:
            print(self.title)

        system('cls')
        self.__create_menu()

        Control([
            {
                'key_name': 'w',
                'callback': lambda: self.__update_focus_index(self.__get_focus_index() - 1)
            },
            {
                'key_name': 's',
                'callback': lambda: self.__update_focus_index(self.__get_focus_index() + 1)
            },
        ])

    def __update_menu(self) -> None:
        system('cls')
        self.__create_menu()

    def __create_menu(self) -> None:
        buf = self.title + '\n'
        for i, item in enumerate(self.items):
            if i == self.item_focus_index:
                buf += f'\n{i + 1}. \u001b[4m\u001b[1m{item}\033[0m'
                continue

            buf += '\n' + f'{i + 1}. {item}'

        print(buf)

    def __set_focus_index(self, index) -> None:
        self.item_focus_index = index
        self.__update_menu()

    def __update_focus_index(self, index) -> None:
        if index < 0:
            self.__set_focus_index(len(self.items) - 1)
        elif index > len(self.items) - 1:
            self.__set_focus_index(0)
        else:
            self.__set_focus_index(index)

    def __get_focus_index(self) -> int:
        return self.item_focus_index