import logging as log

import ctypes as c
import numpy as np
import psutil
import win32api

from ctypes import wintypes as w

open_process = c.windll.kernel32.OpenProcess
open_process.argtypes = [w.DWORD, w.BOOL, w.DWORD]
open_process.restype = w.BOOL

read_process_mem = c.WinDLL('kernel32', use_last_error=True).ReadProcessMemory
read_process_mem.argtypes = [w.HANDLE, w.LPCVOID, w.LPVOID,
                             c.c_size_t, c.POINTER(c.c_size_t)]
read_process_mem.restype = w.BOOL


PAA = 0x1F0FFF
BASE_ADDR = 0x140000000

AOB_X = [0x48, 0x8B, 0x05, 'xx', 'xx', 'xx', 'xx',
         0x48, 0x39, 0x48, 0x68, 0x0F, 0x94, 0xC0, 0xC3]
OFF_X = [0x120, 0x20, 0x50, 0x28, 0x18, 0x68]
OFF_Y = [0x128, 0x20, 0x50, 0x28, 0x18, 0x68]
OFF_Z = [0x124, 0x20, 0x50, 0x28, 0x18, 0x68]


def aob_match(arr, start, pattern):
    for idx, match in enumerate(pattern):
        if isinstance(match, int):
            if arr[start + idx] != match:
                return False
    print('Found pattern match:', start)
    return True


def aob_scan(arr, pattern):
    initial = pattern[0]
    starts = np.where(arr == initial)[0]

    for start in starts:
        if aob_match(arr, start, pattern):
            return int(start)

    return None


class DksState:
    def __init__(self, pid):
        log.debug('Setting up game state scanner for pid: %s', pid)
        self.pid = pid
        self.ph = win32api.OpenProcess(PAA, 0, int(self.pid))

        self.buffer = np.zeros(4, np.uint8)
        self.bytes_read = c.c_ulonglong(0)

        self.pos_x_addr = None
        self.pos_y_addr = None
        self.pos_z_addr = None

        self.ready = False

        self.scan_pointers()

    def read_int(self, addr):
        res = read_process_mem(self.ph.handle, addr, self.buffer.ctypes.data,
                               self.buffer.itemsize * self.buffer.size,
                               c.byref(self.bytes_read))
        ret = int(np.frombuffer(self.buffer, dtype=np.uint32))
        return ret

    def read_float(self, addr):
        res = read_process_mem(self.ph.handle, addr, self.buffer.ctypes.data,
                               self.buffer.itemsize * self.buffer.size,
                               c.byref(self.bytes_read))
        return float(np.frombuffer(self.buffer, dtype=np.float32))

    def resolve_nested_ptr(self, addr, offsets):
        while offsets:
            addr = self.read_int(addr) + offsets.pop()
        return addr

    def resolve_aob(self, mem, pattern, addr_offset, instr_size):
        base = BASE_ADDR + aob_scan(mem, pattern)
        base = base + self.read_int(base + addr_offset) + instr_size
        return base

    def scan_pointers(self):
        log.info('Scanning for pointers in process: %s', self.pid)
        full_len = psutil.Process(self.pid)
        full_len = 512 * 1024 * 32
        full = np.zeros(full_len, dtype=np.uint8)

        res = read_process_mem(self.ph.handle, BASE_ADDR, full.ctypes.data,
                               full.itemsize * full.size,
                               c.byref(self.bytes_read))

        base_x = self.resolve_aob(full, AOB_X, 3, 7)
        self.pos_x_addr = self.resolve_nested_ptr(base_x, OFF_X)
        self.pos_y_addr = self.resolve_nested_ptr(base_x, OFF_Y)
        self.pos_z_addr = self.resolve_nested_ptr(base_x, OFF_Z)
        log.debug('Determined X pointer: %s', hex(self.pos_x_addr))
        log.debug('Determined Y pointer: %s', hex(self.pos_y_addr))
        log.debug('Determined Z pointer: %s', hex(self.pos_z_addr))

        self.ready = True

        log.info('Done scanning pointers for process: %s', self.pid)

    def get_position(self):
        x = self.read_float(self.pos_x_addr)
        y = self.read_float(self.pos_y_addr)
        z = self.read_float(self.pos_z_addr)
        return x, y, z
