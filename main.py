#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gallery Generate Agent - 主程序入口

使用方法:
    python main.py
"""

import sys
import os

# 将 src 目录添加到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gallery_generator.__main__ import main

if __name__ == "__main__":
    main()
