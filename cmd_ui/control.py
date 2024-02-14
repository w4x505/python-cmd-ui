from dataclasses import dataclass
from typing import Callable, TypedDict, List, NewType, Iterable
from msvcrt import getch

@dataclass
class KeyAction(TypedDict):
    key: str
    callback: Callable

class Control:
    keys_action: List[KeyAction]

    def __init__(self, keys_action: List[KeyAction], exit_key = b'\x1b') -> None:
        self.keys_action = keys_action
        self.special_key_code = 0

        while True:
            key_index = ord(getch())
            if key_index == ord(exit_key) or key_index == ord('\003'):
                break

            for key in self.keys_action:
                if len(key['key']) <= 1 and ord(key['key']) == key_index:
                    key['callback']()
                    continue

                if key_index == self.special_key_code:
                    key_index = ord(getch())

                    if key_index == self.get_arrow_key_code(key['key']):
                        key['callback']()

    def get_arrow_key_code(self, key: str) -> int:
        if key == 'up':
            return 72
        
        if key == 'down':
            return 80
        
        if key == 'left':
            return 75
        
        if key == 'right':
            return 77
            
        return -1
    