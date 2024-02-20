from dataclasses import dataclass
from typing import Callable, TypeAlias, Union, List
from msvcrt import getch

ascii_special_key_codes = {
    'esc' : 27,
    'etx' : 3,
    'enter' : 13,
    'tab' : 9,
    'backspace' : 8,
    'space' : 32,
    'up' : 72,
    'down' : 80,
    'left' : 75,
    'right' : 77,
    'f1' : 59,
    'f2' : 60,
    'f3' : 61,
    'f4' : 62,
    'f5' : 63,
    'f6' : 64,
    'f7' : 65,
    'f8' : 66,
    'f9' : 67,
    'f10' : 68,
    'f11' : 133,
    'f12' : 134,
    'special_key' : 224
}

ascii_key_codes = {
    '!' : 33,
    '"' : 34,
    '#' : 35,
    '$' : 36,
    '%' : 37,
    '&' : 38,
    "'" : 39,
    '(' : 40,
    ')' : 41,
    '*' : 42,
    '+' : 43,
    ',' : 44,
    '-' : 45,
    '.' : 46,
    '/' : 47,
    '0' : 48,
    '1' : 49,
    '2' : 50,
    '3' : 51,
    '4' : 52,
    '5' : 53,
    '6' : 54,
    '7' : 55,
    '8' : 56,
    '9' : 57,
    ':' : 58,
    ';' : 59,
    '<' : 60,
    '=' : 61,
    '>' : 62,
    '?' : 63,
    '@' : 64,
    'A' : 65,
    'B' : 66,
    'C' : 67,
    'D' : 68,
    'E' : 69,
    'F' : 70,
    'G' : 71,
    'H' : 72,
    'I' : 73,
    'J' : 74,
    'K' : 75,
    'L' : 76,
    'M' : 77,
    'N' : 78,
    'O' : 79,
    'P' : 80,
    'Q' : 81,
    'R' : 82,
    'S' : 83,
    'T' : 84,
    'U' : 85,
    'V' : 86,
    'W' : 87,
    'X' : 88,
    'Y' : 89,
    'Z' : 90,
    '[' : 91,
    '\\' : 92,
    ']' : 93,
    '^' : 94,
    '_' : 95,
    '`' : 96,
    'a' : 97,
    'b' : 98,
    'c' : 99,
    'd' : 100,
    'e' : 101,
    'f' : 102,
    'g' : 103,
    'h' : 104,
    'i' : 105,
    'j' : 106,
    'k' : 107,
    'l' : 108,
    'm' : 109,
    'n' : 110,
    'o' : 111,
    'p' : 112,
    'q' : 113,
    'r' : 114,
    's' : 115,
    't' : 116,
    'u' : 117,
    'v' : 118,
    'w' : 119,
    'x' : 120,
    'y' : 121,
    'z' : 122,
    '{' : 123,
    '|' : 124,
    '}' : 125,
    '~' : 126
}

KeyIdentifierType: TypeAlias = Union[str, int]

class KeyAddingError(Exception):
    pass

@dataclass
class Key:
    identifier: KeyIdentifierType
    """ButtonName | ButtonCode"""
    callback: Callable
    is_special_key: bool = False

class KeyHandler:
    available_keys: List[Key] | None
    tracking_state = False

    def __init__(self,
        available_keys: List[Key] | None = None,
        exit_key: KeyIdentifierType = ascii_special_key_codes['esc'],
    ) -> None:
        self.available_keys = None
        if available_keys is not None:
            for key in sorted(available_keys, key=lambda _key: not _key.is_special_key):
                self.add_key(key)

        self.exit_key = exit_key if isinstance(exit_key, int) else ascii_special_key_codes[exit_key]

    def start_tracking_keys(self):
        self.__start_tracking_keys()

    def __start_tracking_keys(self):
        self.tracking_state = True

        def handle_pressed_key(pressed_key):
            for key in self.available_keys:
                if pressed_key != key.identifier:
                    continue

                key.callback()

        while self.tracking_state:
            pressed_key_code = ord(getch())

            if (
                pressed_key_code == self.exit_key or
                pressed_key_code == ascii_special_key_codes['etx']
            ): self.stop_tracking_keys()

            if self.available_keys is None:
                continue

            if pressed_key_code == ascii_special_key_codes['special_key']:
                pressed_key_code = ord(getch())

                for key in self.available_keys:
                    if pressed_key_code != key.identifier:
                        continue

                    handle_pressed_key(pressed_key_code)
                continue

            handle_pressed_key(pressed_key_code)

    def stop_tracking_keys(self):
        self.set_tracking_keys_state(False)

    def set_tracking_keys_state(self, state: bool):
        self.tracking_state = state

    def add_key(self, key: Key):
        if self.available_keys is None:
            self.available_keys = []

        if key in self.available_keys:
            raise KeyAddingError(f"Key '{key.identifier} is not unique.'")

        text_error = ""
        if key.is_special_key:
            text_error = f"Unknown special key '{key.identifier}'"
        else:
            text_error = f"Unknown key '{key.identifier}'"

        if not self.is_ascii_key_exists(key.identifier, key.is_special_key):
            raise KeyAddingError(text_error)

        key_code: int | None
        if isinstance(key.identifier, str):
            key_code = self.get_ascii_key_code(key.identifier, special_key=key.is_special_key)

            if key_code is None:
                raise KeyAddingError(f"An unknown error occurred while adding the key '{key.identifier}'")

            key.identifier = key_code

        self.available_keys.append(key)
        self.available_keys.sort(key=lambda key: not key.is_special_key)

    @staticmethod
    def is_ascii_key_exists(key_identifier: str | int, special_key=False) -> bool:
        if isinstance(key_identifier, int):
            if KeyHandler.get_ascii_key_by_value(key_identifier, special_key) is not None:
                return True
        else:
            if KeyHandler.get_ascii_key_code(key_identifier, special_key) is not None:
                return True
        return False

    @staticmethod
    def get_ascii_key_code(key_name: str, special_key=False) -> int | None:
        ascii_key_obj = ascii_key_codes if not special_key else ascii_special_key_codes
        try:
            return ascii_key_obj[key_name]
        except KeyError:
            pass

        return None

    @staticmethod
    def get_ascii_key_by_value(key_code: int, special_key=False) -> str | None:
        ascii_key_obj = ascii_key_codes if not special_key else ascii_special_key_codes

        for key, value in ascii_key_obj.items():
            if value != key_code:
                continue

            return key
        return None