"""
图像特征提取模块
结合本地CLIP模型和在线API提取图像特征
"""

import json
import os
from typing import List, Dict, Tuple, Optional
import numpy as np
from PIL import Image
import cv2
from datetime import datetime

from gallery_generator.models.clip_model import CLIPFeatureExtractor


class ImageFeatureExtractor:
    """图像特征提取器"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化特征提取器
        
        Args:
            config_path: 配置文件路径
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 初始化CLIP模型
        model_config = self.config.get("model", {})
        self.clip_extractor = CLIPFeatureExtractor(
            model_name=model_config.get("clip_model_name", "openai/clip-vit-base-patch32"),
            device=model_config.get("device", "auto")
        )
        
        self.batch_size = model_config.get("batch_size", 32)
        self.use_online_api = self.config.get("api", {}).get("use_online_api", False)
    
    def extract_image_features(self, image_paths: List[str]) -> Tuple[np.ndarray, List[str], List[Dict]]:
        """
        提取图像特征
        
        Args:
            image_paths: 图片路径列表
            
        Returns:
            (特征向量数组, 有效路径列表, 元数据列表)
        """
        # 提取CLIP特征
        features, valid_paths = self.clip_extractor.extract_features_from_paths(
            image_paths, self.batch_size
        )
        
        # 提取元数据
        metadata_list = []
        for path in valid_paths:
            metadata = self._extract_metadata(path)
            metadata_list.append(metadata)
        
        # 如果启用在线API，可以在这里添加补充特征
        if self.use_online_api:
            # TODO: 集成在线API特征提取
            pass
        
        return features, valid_paths, metadata_list
    
    def _extract_metadata(self, image_path: str) -> Dict:
        """
        提取图像元数据
        
        Args:
            image_path: 图片路径
            
        Returns:
            元数据字典
        """
        metadata = {
            "path": image_path,
            "filename": os.path.basename(image_path),
            "size": 0,
            "format": "",
            "width": 0,
            "height": 0,
            "modification_time": None
        }
        
        try:
            # 获取文件信息
            stat = os.stat(image_path)
            metadata["size"] = stat.st_size
            metadata["modification_time"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
            
            # 获取图片信息
            with Image.open(image_path) as img:
                metadata["format"] = img.format
                metadata["width"], metadata["height"] = img.size
                
                # 提取EXIF信息（如果有）
                if hasattr(img, '_getexif') and img._getexif() is not None:
                    exif = img._getexif()
                    if exif:
                        metadata["exif"] = self._parse_exif(exif)
        
        except Exception as e:
            print(f"提取元数据失败 {image_path}: {e}")
        
        return metadata
    
    def _parse_exif(self, exif: Dict) -> Dict:
        """解析EXIF数据"""
        exif_data = {}
        # EXIF标签映射
        exif_tags = {
            271: "make",
            272: "model",
            306: "datetime",
            33434: "exposure_time",
            33437: "f_number",
            34855: "iso",
        }
        
        for tag_id, tag_name in exif_tags.items():
            if tag_id in exif:
                exif_data[tag_name] = str(exif[tag_id])
        
        return exif_data
    
    def analyze_composition(self, image_path: str) -> Dict:
        """
        分析图像构图特征
        
        Args:
            image_path: 图片路径
            
        Returns:
            构图特征字典
        """
        composition = {
            "rule_of_thirds": False,
            "center_composition": False,
            "symmetry": False,
            "aspect_ratio": 1.0
        }
        
        try:
            img = cv2.imread(image_path)
            if img is None:
                return composition
            
            height, width = img.shape[:2]
            composition["aspect_ratio"] = width / height if height > 0 else 1.0
            
            # 转换为灰度图进行构图分析
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 检测对称性（简化版）
            left_half = gray[:, :width//2]
            right_half = cv2.flip(gray[:, width//2:], 1)
            right_half = right_half[:, :left_half.shape[1]]
            
            if left_half.shape == right_half.shape:
                diff = cv2.absdiff(left_half, right_half)
                symmetry_score = 1 - (np.mean(diff) / 255.0)
                composition["symmetry"] = symmetry_score > 0.7
            
            # 中心构图检测（简化版）
            center_region = gray[int(height*0.4):int(height*0.6), int(width*0.4):int(width*0.6)]
            edge_region = np.concatenate([
                gray[:int(height*0.3), :].flatten(),
                gray[int(height*0.7):, :].flatten(),
                gray[:, :int(width*0.3)].flatten(),
                gray[:, int(width*0.7):].flatten()
            ])
            
            if len(edge_region) > 0 and len(center_region) > 0:
                center_brightness = np.mean(center_region)
                edge_brightness = np.mean(edge_region)
                composition["center_composition"] = center_brightness > edge_brightness * 1.2
            
            # 三分法检测（简化版）
            # 检查是否有明显的主体在三分线附近
            third_points = [width//3, width*2//3, height//3, height*2//3]
            composition["rule_of_thirds"] = True  # 简化实现
        
        except Exception as e:
            print(f"构图分析失败 {image_path}: {e}")
        
        return composition


