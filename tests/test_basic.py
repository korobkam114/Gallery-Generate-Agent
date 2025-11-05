"""
基础测试用例
"""

import pytest
from gallery_generator import __version__


def test_version():
    """测试版本号"""
    assert __version__ == "1.0.0"


def test_imports():
    """测试核心模块导入"""
    from gallery_generator import ImageAnalyzer, CLIPFeatureExtractor
    
    assert ImageAnalyzer is not None
    assert CLIPFeatureExtractor is not None

