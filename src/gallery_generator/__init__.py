"""
Gallery Generate Agent - 智能图片分类与作品集生成工具

基于 AI 的图片自动识别、分类和作品集生成系统。
"""

__version__ = "1.0.0"
__author__ = "Gallery Generate Agent Team"
__license__ = "MIT"

from .core.image_analyzer import ImageAnalyzer
from .models.clip_model import CLIPFeatureExtractor

__all__ = [
    "ImageAnalyzer",
    "CLIPFeatureExtractor",
]

