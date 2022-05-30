# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time  : 2022-05-30 19:18
# Author: jgw
from pprint import pprint
from typing import List, Dict, Union
import random as rd
import math
import datetime as dt
import re
from abc import ABCMeta, abstractmethod
import pyautogui
import os

"""
执行时获取鼠标的位置
"""

print(pyautogui.position())

os.system("pause")

'''
pyinstaller --clean --noconfirm --collect-all setuptools -D get_mouse_position.py
'''
