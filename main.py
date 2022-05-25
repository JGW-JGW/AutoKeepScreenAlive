# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time  : 2022-05-25 11:49
# Author: jgw
from pprint import pprint
from typing import List, Dict, Union
import random as rd
import math
import datetime as dt
import re
from abc import ABCMeta, abstractmethod
import pyautogui
import win32con
import win32gui
from time import sleep
import logging
from sys import stdin

"""
给定句柄类和名称，在指定的窗口间进行切换，防止进入屏保
"""

pyautogui.FAILSAFE = False


def get_all_windows() -> Dict:
	res = {
		"windows": [],
		"max_text_len": 0,
		"max_cls_len": 0
	}

	def get_window_info(window_id: int, mouse):
		if win32gui.IsWindow(window_id) and win32gui.IsWindowEnabled(window_id) and win32gui.IsWindowVisible(window_id):
			cls = win32gui.GetClassName(window_id)
			text = win32gui.GetWindowText(window_id)
			res['windows'].append((cls, text))

			if len(cls) > res['max_cls_len']:
				res['max_cls_len'] = len(cls)

			if len(text) > res['max_text_len']:
				res['max_text_len'] = len(text)

	win32gui.EnumWindows(get_window_info, 0)

	return res


result = get_all_windows()
windows = result['windows']
max_cls_len = result['max_cls_len']
max_text_len = result['max_text_len']

n = len(windows)

width_no = max(int(math.log10(n)) + 1, 3)
width_cls = max(max_cls_len, 5)
width_text = max(max_text_len, 4)

head_col_1 = 'No.'
head_col_2 = 'Class'
head_col_3 = 'Text'

width_total = width_no + width_cls + width_text + 6

for i in range(width_total):
	print('=', end='')
print()

print(f"{head_col_1:>{width_no}} | {head_col_2:<{width_cls}} | {head_col_3:<{width_text}}")

for i in range(width_total):
	print('-', end='')
print()

for i in range(n):
	print(f"{i + 1:>{width_no}} | {windows[i][0]:<{width_cls}} | {windows[i][1]:<{width_text}}")

for i in range(width_total):
	print('=', end='')
print()

print('Please input numbers:')

user_input = stdin.readline().strip()
no_list = list(map(int, user_input.split()))

print('Your choices are:')
for no in no_list:
	print(f"{windows[no - 1][0]} | {windows[no - 1][1]}")

index = 0
while True:
	cls = windows[no_list[index] - 1][0]
	text = windows[no_list[index] - 1][1]

	print(f"INFO: Locate window: cls = \"{cls}\", text = \"{text}\"")

	window = win32gui.FindWindow(cls, text)

	if not window:
		print(f"ERROR: Can not locate window: cls = \"{cls}\", text = \"{text}\"")
		continue

	win32gui.SetActiveWindow(window)
	win32gui.ShowWindow(window, win32con.SW_SHOWMAXIMIZED)

	pyautogui.press('ctrl')

	win32gui.SetForegroundWindow(window)

	sleep(10)

	index = (index + 1) % len(no_list)

'''
pyinstaller --clean --noconfirm --collect-all setuptools -D main.py
'''