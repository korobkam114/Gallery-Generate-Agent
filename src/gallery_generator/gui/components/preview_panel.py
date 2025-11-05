"""
预览面板组件
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
import os


class PreviewPanel(QWidget):
    """预览面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        title = QLabel("处理结果")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        
        self.open_folder_btn = QPushButton("打开输出文件夹")
        self.open_folder_btn.setEnabled(False)
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        
        layout.addWidget(title)
        layout.addWidget(self.preview_text)
        layout.addWidget(self.open_folder_btn)
        
        self.setLayout(layout)
        self.output_dir = None
    
    def show_results(self, results: dict):
        """
        显示处理结果
        
        Args:
            results: 处理结果字典
        """
        text = ""
        
        if results.get("success"):
            text += f"✓ 处理成功！\n\n"
            text += f"扫描图片数量: {results.get('image_count', 0)}\n"
            text += f"识别类别数量: {results.get('cluster_count', 0)}\n\n"
            
            cluster_results = results.get("cluster_results", {})
            cluster_info = cluster_results.get("cluster_info", {})
            
            text += "识别到的类别:\n"
            for cluster_id, info in cluster_info.items():
                text += f"  • {info.get('name', '未知')}: {info.get('count', 0)} 张图片\n"
            
            text += "\n生成的作品集:\n"
            gallery_paths = results.get("gallery_paths", {})
            if "html" in gallery_paths:
                text += f"  • HTML: {gallery_paths['html']}\n"
            if "pdf" in gallery_paths:
                text += f"  • PDF: {gallery_paths['pdf']}\n"
            if "folder" in gallery_paths:
                text += f"  • 文件夹: {gallery_paths['folder']}\n"
            
            self.output_dir = results.get("output_dir")
            self.open_folder_btn.setEnabled(True)
        else:
            text = f"✗ 处理失败: {results.get('message', '未知错误')}"
            self.open_folder_btn.setEnabled(False)
        
        self.preview_text.setPlainText(text)
    
    def open_output_folder(self):
        """打开输出文件夹"""
        if self.output_dir and os.path.exists(self.output_dir):
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                os.startfile(self.output_dir)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", self.output_dir])
            else:
                subprocess.Popen(["xdg-open", self.output_dir])


