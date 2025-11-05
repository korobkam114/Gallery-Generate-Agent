"""
Gallery Generate Agent 安装配置
"""

from setuptools import setup, find_packages
import os

# 读取 README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# 读取依赖
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="gallery-generate-agent",
    version="1.0.0",
    author="Gallery Generate Agent Team",
    author_email="your.email@example.com",
    description="基于 AI 的智能图片分类与作品集生成工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gallery-generate-agent",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/gallery-generate-agent/issues",
        "Documentation": "https://github.com/yourusername/gallery-generate-agent/blob/main/README.md",
        "Source Code": "https://github.com/yourusername/gallery-generate-agent",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gallery-generator=gallery_generator.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "gallery_generator": [
            "outputs/*.html",
            "outputs/*.css",
        ],
    },
    zip_safe=False,
)

