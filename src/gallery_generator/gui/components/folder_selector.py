"""
文件夹选择组件
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QHBoxLayout, QFileDialog


class FolderSelector(QWidget):
    """文件夹选择器组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout()
        
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("请选择包含图片的文件夹...")
        self.path_edit.setReadOnly(True)
        
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.clicked.connect(self.browse_folder)
        
        layout.addWidget(self.path_edit)
        layout.addWidget(self.browse_btn)
        
        self.setLayout(layout)
    
    def browse_folder(self):
        """浏览文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择包含图片的文件夹",
            ""
        )
        if folder:
            self.path_edit.setText(folder)
    
    def get_path(self) -> str:
        """获取选择的文件夹路径"""
        return self.path_edit.text()
    
    def set_path(self, path: str):
        """设置文件夹路径"""
        self.path_edit.setText(path)


