"""
主窗口GUI
"""

import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QSpinBox, QCheckBox, QGroupBox,
                             QMessageBox, QFileDialog, QLineEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from gallery_generator.gui.components.folder_selector import FolderSelector
from gallery_generator.gui.components.progress_dialog import ProgressDialog
from gallery_generator.gui.components.preview_panel import PreviewPanel
from gallery_generator.core.image_analyzer import ImageAnalyzer


class ProcessingThread(QThread):
    """处理线程"""
    
    progress_updated = pyqtSignal(int, int, str)
    finished = pyqtSignal(dict)
    
    def __init__(self, analyzer, folder_path, output_dir, formats, n_clusters):
        super().__init__()
        self.analyzer = analyzer
        self.folder_path = folder_path
        self.output_dir = output_dir
        self.formats = formats
        self.n_clusters = n_clusters
        self._stop_flag = False
    
    def stop(self):
        """停止处理"""
        self._stop_flag = True
    
    def run(self):
        """运行处理"""
        try:
            # 直接设置分类器的聚类数量，不修改配置文件（修复线程安全问题）
            if self.n_clusters and self.n_clusters > 0:
                self.analyzer.classifier.n_clusters = self.n_clusters
            
            def progress_callback(current, total, message):
                if self._stop_flag:
                    raise InterruptedError("用户取消操作")
                self.progress_updated.emit(current, total, message)
            
            results = self.analyzer.process_folder(
                self.folder_path,
                self.output_dir,
                self.formats,
                progress_callback
            )
            
            self.finished.emit(results)
        except InterruptedError:
            self.finished.emit({
                "success": False,
                "message": "操作已取消"
            })
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"处理错误详情:\n{error_details}")
            self.finished.emit({
                "success": False,
                "message": f"处理出错: {str(e)}"
            })


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gallery Generate Agent - 图片自动识别归类工具")
        self.setMinimumSize(800, 600)
        self.init_ui()
        
        # 初始化分析器
        try:
            self.analyzer = ImageAnalyzer()
        except Exception as e:
            QMessageBox.critical(self, "初始化错误", f"无法初始化分析器: {str(e)}")
            sys.exit(1)
        
        self.processing_thread = None
    
    def init_ui(self):
        """初始化UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 标题
        title = QLabel("Gallery Generate Agent")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #667eea; padding: 20px;")
        main_layout.addWidget(title)
        
        # 文件夹选择
        folder_group = QGroupBox("选择图片文件夹")
        folder_layout = QVBoxLayout()
        self.folder_selector = FolderSelector()
        folder_layout.addWidget(self.folder_selector)
        folder_group.setLayout(folder_layout)
        main_layout.addWidget(folder_group)
        
        # 参数配置
        config_group = QGroupBox("处理参数")
        config_layout = QVBoxLayout()
        
        # 聚类数量
        cluster_layout = QHBoxLayout()
        cluster_layout.addWidget(QLabel("聚类数量:"))
        self.n_clusters_spin = QSpinBox()
        self.n_clusters_spin.setMinimum(1)
        self.n_clusters_spin.setMaximum(50)
        self.n_clusters_spin.setValue(5)
        self.n_clusters_spin.setToolTip("设置为0将自动确定聚类数量")
        cluster_layout.addWidget(self.n_clusters_spin)
        cluster_layout.addStretch()
        config_layout.addLayout(cluster_layout)
        
        # 输出格式选择
        format_layout = QVBoxLayout()
        format_layout.addWidget(QLabel("输出格式:"))
        self.html_check = QCheckBox("HTML网页")
        self.html_check.setChecked(True)
        self.pdf_check = QCheckBox("PDF文档")
        self.pdf_check.setChecked(True)
        self.folder_check = QCheckBox("文件夹结构")
        self.folder_check.setChecked(True)
        format_layout.addWidget(self.html_check)
        format_layout.addWidget(self.pdf_check)
        format_layout.addWidget(self.folder_check)
        config_layout.addLayout(format_layout)
        
        # 输出目录选择
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("outputs/gallery (默认)")
        self.output_path_edit.setReadOnly(True)
        self.output_path_edit.setStyleSheet("border: 1px solid #ddd; padding: 5px;")
        output_browse_btn = QPushButton("浏览...")
        output_browse_btn.clicked.connect(self.browse_output_folder)
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(output_browse_btn)
        config_layout.addLayout(output_layout)
        
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始处理")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 10px 30px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #764ba2;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        self.start_btn.clicked.connect(self.start_processing)
        button_layout.addStretch()
        button_layout.addWidget(self.start_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # 预览面板
        self.preview_panel = PreviewPanel()
        main_layout.addWidget(self.preview_panel)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
    
    def browse_output_folder(self):
        """浏览输出文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择输出文件夹",
            ""
        )
        if folder:
            self.output_path_edit.setText(folder)
    
    def get_output_dir(self) -> str:
        """获取输出目录"""
        output_text = self.output_path_edit.text().strip()
        if not output_text or output_text == "":
            return None
        return output_text
    
    def get_output_formats(self) -> list:
        """获取选中的输出格式"""
        formats = []
        if self.html_check.isChecked():
            formats.append("html")
        if self.pdf_check.isChecked():
            formats.append("pdf")
        if self.folder_check.isChecked():
            formats.append("folder")
        return formats if formats else ["html"]
    
    def start_processing(self):
        """开始处理"""
        folder_path = self.folder_selector.get_path()
        if not folder_path or not os.path.isdir(folder_path):
            QMessageBox.warning(self, "警告", "请先选择包含图片的文件夹！")
            return
        
        output_dir = self.get_output_dir()
        formats = self.get_output_formats()
        n_clusters = self.n_clusters_spin.value()
        
        if not formats:
            QMessageBox.warning(self, "警告", "请至少选择一种输出格式！")
            return
        
        # 显示进度对话框
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.cancelled.connect(self.on_cancel_processing)
        self.progress_dialog.show()
        
        # 禁用开始按钮
        self.start_btn.setEnabled(False)
        self.statusBar().showMessage("正在处理...")
        
        # 创建处理线程
        self.processing_thread = ProcessingThread(
            self.analyzer,
            folder_path,
            output_dir,
            formats,
            n_clusters if n_clusters > 0 else None
        )
        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.start()
    
    def on_cancel_processing(self):
        """取消处理"""
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.stop()
            self.statusBar().showMessage("正在取消...")
    
    def update_progress(self, current: int, total: int, message: str):
        """更新进度"""
        self.progress_dialog.update_progress(current, total, message)
    
    def on_processing_finished(self, results: dict):
        """处理完成"""
        self.progress_dialog.close()
        self.start_btn.setEnabled(True)
        
        if results.get("success"):
            self.statusBar().showMessage("处理完成！")
            self.preview_panel.show_results(results)
            QMessageBox.information(
                self,
                "完成",
                f"处理完成！\n\n识别了 {results.get('cluster_count', 0)} 个类别\n共处理 {results.get('image_count', 0)} 张图片"
            )
        else:
            self.statusBar().showMessage("处理失败")
            self.preview_panel.show_results(results)
            QMessageBox.critical(self, "错误", results.get("message", "处理失败"))
        
        # 清理线程
        if self.processing_thread:
            self.processing_thread.quit()
            self.processing_thread.wait()
            self.processing_thread = None

