import time

from pynput import keyboard
from pynput import mouse

FRAME = 1. / 60.


class DksController:
    def __init__(self):
        self.board = keyboard.Controller()
        self.mouse = mouse.Controller()

    def wait(self):
        time.sleep(FRAME)

    def forward_beg(self):
        self.board.press('w')

    def forward_end(self):
        self.board.release('w')

    def backward_beg(self):
        self.board.press('s')

    def backward_end(self):
        self.board.release('s')

    def left_beg(self):
        self.board.press('a')

    def left_end(self):
        self.board.release('a')

    def right_beg(self):
        self.board.press('d')

    def right_end(self):
        self.board.release('d')

    def roll(self):
        self.board.press(keyboard.Key.space)
        self.wait()
        self.board.release(keyboard.Key.space)

    def sprint_beg(self):
        self.board.press(keyboard.Key.space)

    def spring_end(self):
        self.board.release(keyboard.Key.space)

    def right_light(self):
        self.mouse.press(mouse.Button.left)
        self.wait()
        self.mouse.release(mouse.Button.left)

    def right_strong(self):
        with self.board.pressed(keyboard.Key.shift):
            self.right_light()

    def parry(self):
        with self.board.pressed(keyboard.Key.shift):
            self.mouse.press(mouse.Button.right)
            self.wait()
            self.mouse.release(mouse.Button.right)

    def block_beg(self):
        self.mouse.press(mouse.Button.right)

    def block_end(self):
        self.mouse.release(mouse.Button.right)

    def use_item(self):
        self.board.press('r')
        self.wait()
        self.board.release('r')

    def two_hand_toggle(self):
        self.board.press('f')
        self.wait()
        self.board.release('f')

    def activate(self):
        self.board.press('e')
        self.wait()
        self.board.release('e')

    def switch_right(self):
        with self.board.pressed(keyboard.Key.shift):
            self.mouse.scroll(0, 5)

    def switch_left(self):
        with self.board.pressed(keyboard.Key.shift):
            self.mouse.scroll(0, -5)

    def switch_spell(self):
        self.mouse.scroll(0, 5)

    def switch_item(self):
        self.mouse.scroll(0, -5)

    def lockon(self):
        self.mouse.press(mouse.Button.middle)
        self.wait()
        self.mouse.release(mouse.Button.middle)
