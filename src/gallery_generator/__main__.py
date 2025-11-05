"""
Gallery Generate Agent 主入口
支持作为模块运行: python -m gallery_generator
"""

from .gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("Gallery Generate Agent")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

