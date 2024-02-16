from typing import List
from os import system
from cmd_ui.control import Control, Key, ASCIKeysCode

class Interface:
    def __init__(self, items: List[str], title = ''):
        self.__items = items
        self.__title = title
        self.__item_focus_index = 0

        system('cls')
        self.__create_menu()

        Control([
            Key(key=ASCIKeysCode.up, callback=self.__user_key_press_down),
            Key(key=ASCIKeysCode.down, callback=self.__user_key_press_up),
            Key(key='w', callback=self.__user_key_press_down),
            Key(key='s', callback=self.__user_key_press_up),
        ])

    def __user_key_press_down(self) -> None:
        self.__update_focus_index(self.__get_focus_index() - 1)

    def __user_key_press_up(self) -> None:
        self.__update_focus_index(self.__get_focus_index() + 1)

    def __update_menu(self) -> None:
        system('cls')
        self.__create_menu()

    def __create_menu(self) -> None:
        buf = ''

        if len(self.__title) > 0:
            buf += self.__title + '\n'

        for i, item in enumerate(self.__items):
            if i == self.__item_focus_index:
                buf += f'{i + 1}. \u001b[4m\u001b[1m{item}\033[0m'

                if i != len(self.__items) - 1:
                    buf += '\n'

                continue

            item_str = f'{i + 1}. {item}'
            buf += item_str + '\n' if i != len(self.__items) - 1 else item_str

        print(buf)

    def __set_focus_index(self, index) -> None:
        self.__item_focus_index = index
        self.__update_menu()

    def __update_focus_index(self, index) -> None:
        if index < 0:
            self.__set_focus_index(len(self.__items) - 1)
        elif index > len(self.__items) - 1:
            self.__set_focus_index(0)
        else:
            self.__set_focus_index(index)

    def __get_focus_index(self) -> int:
        return self.__item_focus_index