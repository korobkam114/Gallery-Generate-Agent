"""
图像分析核心逻辑模块
整合特征提取、分类和作品集生成功能
"""

import os
import json
from typing import List, Dict, Optional
from pathlib import Path

from gallery_generator.core.feature_extractor import ImageFeatureExtractor
from gallery_generator.core.classifier import ImageClassifier
from gallery_generator.core.gallery_generator import GalleryGenerator


class ImageAnalyzer:
    """图像分析器主类"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化图像分析器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 初始化各个模块
        self.feature_extractor = ImageFeatureExtractor(config_path)
        self.classifier = ImageClassifier(config_path)
        self.gallery_generator = GalleryGenerator(config_path)
        
        # 支持的图片格式
        self.supported_formats = set(
            self.config.get("supported_formats", [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"])
        )
    
    def scan_images(self, folder_path: str) -> List[str]:
        """
        扫描文件夹中的图片
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            图片路径列表
        """
        image_paths = []
        
        if not os.path.isdir(folder_path):
            return image_paths
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in self.supported_formats:
                    image_paths.append(file_path)
        
        return image_paths
    
    def analyze_and_cluster(self, image_paths: List[str], 
                          progress_callback=None) -> Dict:
        """
        分析图片并进行聚类
        
        Args:
            image_paths: 图片路径列表
            progress_callback: 进度回调函数 (current, total, message)
            
        Returns:
            聚类结果字典
        """
        if not image_paths:
            return {
                "labels": [],
                "clusters": {},
                "cluster_info": {},
                "n_clusters": 0
            }
        
        # 提取特征
        if progress_callback:
            progress_callback(0, len(image_paths), "正在提取图像特征...")
        
        features, valid_paths, metadata_list = self.feature_extractor.extract_image_features(
            image_paths
        )
        
        if progress_callback:
            progress_callback(len(image_paths), len(image_paths), "特征提取完成，正在进行聚类...")
        
        # 聚类
        cluster_results = self.classifier.cluster_images(features, valid_paths)
        
        # 添加元数据
        cluster_results['metadata'] = metadata_list
        
        if progress_callback:
            progress_callback(len(image_paths), len(image_paths), "分析完成！")
        
        return cluster_results
    
    def generate_gallery(self, cluster_results: Dict, output_dir: str = None,
                        formats: List[str] = None) -> Dict:
        """
        生成作品集
        
        Args:
            cluster_results: 聚类结果字典
            output_dir: 输出目录
            formats: 输出格式列表 ['html', 'pdf', 'folder']
            
        Returns:
            生成结果字典
        """
        if formats is None:
            formats = ['html', 'pdf', 'folder']
        
        return self.gallery_generator.generate_all(cluster_results, output_dir, formats)
    
    def process_folder(self, folder_path: str, output_dir: str = None,
                      formats: List[str] = None, progress_callback=None) -> Dict:
        """
        处理整个文件夹的完整流程
        
        Args:
            folder_path: 输入文件夹路径
            output_dir: 输出目录
            formats: 输出格式列表
            progress_callback: 进度回调函数
            
        Returns:
            处理结果字典
        """
        # 扫描图片
        if progress_callback:
            progress_callback(0, 100, "正在扫描图片...")
        
        image_paths = self.scan_images(folder_path)
        
        if not image_paths:
            return {
                "success": False,
                "message": "未找到支持的图片文件",
                "image_count": 0
            }
        
        # 分析和聚类
        cluster_results = self.analyze_and_cluster(image_paths, progress_callback)
        
        # 生成作品集
        if progress_callback:
            progress_callback(100, 100, "正在生成作品集...")
        
        if output_dir is None:
            output_dir = self.config.get("output", {}).get("default_output_dir", "outputs/gallery")
        
        if formats is None:
            formats = ['html', 'pdf', 'folder']
        
        gallery_results = self.generate_gallery(cluster_results, output_dir, formats)
        
        return {
            "success": True,
            "image_count": len(image_paths),
            "cluster_count": cluster_results.get("n_clusters", 0),
            "cluster_results": cluster_results,
            "gallery_paths": gallery_results,
            "output_dir": output_dir
        }


