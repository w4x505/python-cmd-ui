from dataclasses import dataclass
from typing import Callable, List, Union
from msvcrt import getch

class ASCIKeysCode:
    esc = b'\x1b'
    eot = b'\x03' # End of Text (ctrl + c)
    special = 224
    up = 72
    down = 80
    left = 75
    right = 77

@dataclass
class Key:
    key: Union[str, int]
    callback: Callable

class Control:
    def __init__(self, keys_action: List[Key], exit_key = ASCIKeysCode.esc) -> None:
        self.keys_action = keys_action

        while True:
            key_code = ord(getch())
            if key_code.to_bytes() == exit_key or key_code.to_bytes() == ASCIKeysCode.eot:
                break

            if key_code == ASCIKeysCode.special:
                key_code = ord(getch())

                for arrow_key in self.keys_action:
                    if (
                        arrow_key.key == ASCIKeysCode.up and key_code == ASCIKeysCode.up or
                        arrow_key.key == ASCIKeysCode.down and key_code == ASCIKeysCode.down or
                        arrow_key.key == ASCIKeysCode.left and key_code == ASCIKeysCode.left or
                        arrow_key.key == ASCIKeysCode.right and key_code == ASCIKeysCode.right
                    ): arrow_key.callback()
            else:
                for key in self.keys_action:
                    if self.is_arrow_key(key.key):
                        continue

                    if not isinstance(key.key, int) and key_code != ord(key.key):
                        continue

                    if key_code != key.key:
                        continue

                    key.callback()

    def is_arrow_key(self, key: str | int) -> bool:
        if (
            key == 'up' or
            key == 'down' or
            key == 'left' or
            key == 'right' or
            key == ASCIKeysCode.up or
            key == ASCIKeysCode.down or
            key == ASCIKeysCode.left or
            key == ASCIKeysCode.right
        ): return True
        return False
