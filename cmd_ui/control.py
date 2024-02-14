from typing import Callable, TypedDict, List
from msvcrt import getch

class KeysAction(TypedDict):
    key_name: str
    callback: Callable

class Control:
    keys_action_data: List[KeysAction]

    def __init__(self, keys_action_data: List[KeysAction], exit_key = b'\x1b') -> None:
        self.keys_action_data = keys_action_data

        while True:
            key = ord(getch())
            if key == ord(exit_key) or key == ord('\003'):
                break

            for key_index in self.keys_action_data:
                if ord(key_index['key_name']) == key:
                    key_index['callback']()