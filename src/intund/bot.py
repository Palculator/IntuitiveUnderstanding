import time

from . import controller


class DksBot:
    def __init__(self):
        self.ctrl = controller.DksController()

    def play(self):
        time.sleep(5.0)
        self.ctrl.parry()
        time.sleep(5.0)
        self.ctrl.roll()
        time.sleep(5.0)
        self.ctrl.block_beg()
        time.sleep(1.0)
        self.ctrl.roll()
        time.sleep(5.0)
        self.ctrl.block_end()
        time.sleep(5.0)
        self.ctrl.parry()
        time.sleep(5.0)
        self.ctrl.forward_beg()
        time.sleep(5.0)
        self.ctrl.forward_end()
        time.sleep(1.0)
