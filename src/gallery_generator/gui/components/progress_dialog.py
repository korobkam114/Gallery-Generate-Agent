"""
进度对话框组件
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal


class ProgressDialog(QDialog):
    """进度对话框"""
    
    cancelled = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("处理进度")
        self.setModal(True)
        self.setFixedSize(400, 180)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        self.status_label = QLabel("准备开始...")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        
        # 添加取消按钮
        button_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.on_cancel)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def on_cancel(self):
        """取消按钮点击事件"""
        self.cancel_btn.setEnabled(False)
        self.status_label.setText("正在取消...")
        self.cancelled.emit()
    
    def update_progress(self, current: int, total: int, message: str = ""):
        """
        更新进度
        
        Args:
            current: 当前进度
            total: 总数
            message: 状态消息
        """
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)
        
        if message:
            self.status_label.setText(message)
        
        # 刷新界面
        self.repaint()


