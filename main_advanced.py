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
import json

"""
给定句柄类和名称，在指定的窗口间进行切换，防止进入屏保，升级版，允许根据配置文件进行任务
json配置文件为 utf-8 编码
"""

pyautogui.FAILSAFE = False


def move_and_click(x: int, y: int):
	pyautogui.moveTo(x, y)
	pyautogui.click()


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

for i in range(n):
	for _ in range(width_total):
		print('-', end='')
	print()
	print(f"{i + 1:>{width_no}} | {windows[i][0]:<{width_cls}} | {windows[i][1]:<{width_text}}")

for i in range(width_total):
	print('=', end='')
print()

print('Please input numbers:')

user_input = stdin.readline().strip()

for i in range(width_total):
	print('=', end='')
print()

no_list = list(map(int, user_input.split()))

print('Your choices are:')
for no in no_list:
	print(f"{windows[no - 1][0]}||{windows[no - 1][1]}")

for i in range(width_total):
	print('=', end='')
print()

conf = "plan.json"

with open(conf, mode="r", encoding="utf-8") as f:
	plan = json.load(f)

index = 0
while True:
	cls = windows[no_list[index] - 1][0]
	text = windows[no_list[index] - 1][1]

	# 定位窗口，如果定位不到就继续下一个
	print(f"INFO: locate window: cls = \"{cls}\", text = \"{text}\"")

	window = win32gui.FindWindow(cls, text)

	if not window:
		print(f"ERROR: can not locate window: cls = \"{cls}\", text = \"{text}\"")
		continue

	# 最大化窗口
	win32gui.SetActiveWindow(window)
	win32gui.ShowWindow(window, win32con.SW_SHOWMAXIMIZED)

	pyautogui.press('ctrl')

	win32gui.SetForegroundWindow(window)

	# 拼接键
	key = f"{cls}||{text}"

	# 如果有配置
	if key in plan:
		# 获取配置的值
		click_flag = plan[key]['click_flag']
		click_coordinates = plan[key]['click_coordinates']
		time_before_each_click = plan[key]['time_before_each_click']
		time_after_final_click = plan[key]['time_after_final_click']

		# 判定是否进行点击操作
		if not click_flag:
			print(f"SKIP: click is forbidden: cls = \"{cls}\", text = \"{text}\"")
			# 最终等待
			sleep(time_after_final_click)
			continue

		# 获取总点击次数
		total_click_num = len(click_coordinates)

		# 根据每个点击的配置进行操作
		for index in range(total_click_num):
			x = click_coordinates[index]['x']
			y = click_coordinates[index]['y']
			time_before_click = time_before_each_click[index]

			# 点击前等待
			sleep(time_before_click)

			# 点击动作
			move_and_click(x, y)

			print(f"INFO: click [{index + 1:d}]: x = {x:4d}, y = {y:4d}")

		# 最终等待
		sleep(time_after_final_click)

	else:  # 没找到配置，等待10秒钟后继续
		sleep(10)

	index = (index + 1) % len(no_list)

'''
pyinstaller --clean --noconfirm -D main_advanced.py
'''
