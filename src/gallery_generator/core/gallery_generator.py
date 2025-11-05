"""
作品集生成模块
生成HTML、PDF和文件夹结构三种格式的作品集
"""

import json
import os
import shutil
from typing import List, Dict
from pathlib import Path
from jinja2 import Template
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class GalleryGenerator:
    """作品集生成器"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化作品集生成器
        
        Args:
            config_path: 配置文件路径
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        output_config = self.config.get("output", {})
        self.default_output_dir = output_config.get("default_output_dir", "outputs/gallery")
        self.html_template_path = output_config.get("html_template", "outputs/html_template.html")
        self.styles_path = output_config.get("styles", "outputs/styles.css")
    
    def generate_all(self, cluster_results: Dict, output_dir: str = None, 
                     formats: List[str] = None) -> Dict:
        """
        生成所有格式的作品集
        
        Args:
            cluster_results: 聚类结果字典
            output_dir: 输出目录
            formats: 要生成的格式列表 ['html', 'pdf', 'folder']
            
        Returns:
            生成结果字典
        """
        if output_dir is None:
            output_dir = self.default_output_dir
        
        if formats is None:
            formats = ['html', 'pdf', 'folder']
        
        os.makedirs(output_dir, exist_ok=True)
        
        results = {}
        
        if 'html' in formats:
            html_path = self.generate_html(cluster_results, output_dir)
            results['html'] = html_path
        
        if 'pdf' in formats:
            pdf_path = self.generate_pdf(cluster_results, output_dir)
            results['pdf'] = pdf_path
        
        if 'folder' in formats:
            folder_path = self.generate_folder_structure(cluster_results, output_dir)
            results['folder'] = folder_path
        
        return results
    
    def generate_html(self, cluster_results: Dict, output_dir: str) -> str:
        """
        生成HTML格式的作品集
        
        Args:
            cluster_results: 聚类结果字典
            output_dir: 输出目录
            
        Returns:
            HTML文件路径
        """
        # 创建图片目录
        images_dir = os.path.join(output_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # 准备数据
        clusters_data = []
        for cluster_id, image_paths in cluster_results['clusters'].items():
            cluster_info = cluster_results['cluster_info'].get(cluster_id, {})
            
            # 复制图片到输出目录
            cluster_images = []
            for img_path in image_paths[:20]:  # 限制每类最多20张
                img_name = os.path.basename(img_path)
                dest_path = os.path.join(images_dir, f"cluster_{cluster_id}_{img_name}")
                try:
                    shutil.copy2(img_path, dest_path)
                    cluster_images.append({
                        "src": f"images/cluster_{cluster_id}_{img_name}",
                        "alt": img_name
                    })
                except Exception as e:
                    print(f"复制图片失败 {img_path}: {e}")
            
            clusters_data.append({
                "id": cluster_id,
                "name": cluster_info.get("name", f"类别 {cluster_id}"),
                "description": cluster_info.get("description", ""),
                "count": cluster_info.get("count", len(image_paths)),
                "images": cluster_images
            })
        
        # 读取模板
        if os.path.exists(self.html_template_path):
            with open(self.html_template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        else:
            template_content = self._get_default_html_template()
        
        template = Template(template_content)
        html_content = template.render(
            clusters=clusters_data,
            title="图片作品集",
            generated_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # 保存HTML文件
        html_path = os.path.join(output_dir, "gallery.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 保存CSS文件
        css_path = os.path.join(output_dir, "styles.css")
        if os.path.exists(self.styles_path):
            shutil.copy2(self.styles_path, css_path)
        else:
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(self._get_default_css())
        
        return html_path
    
    def generate_pdf(self, cluster_results: Dict, output_dir: str) -> str:
        """
        生成PDF格式的作品集
        
        Args:
            cluster_results: 聚类结果字典
            output_dir: 输出目录
            
        Returns:
            PDF文件路径
        """
        pdf_path = os.path.join(output_dir, "gallery.pdf")
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#333333'),
            spaceAfter=30,
            alignment=1  # 居中
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#555555'),
            spaceAfter=20
        )
        
        # 标题
        story.append(Paragraph("图片作品集", title_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # 每个聚类
        for cluster_id, image_paths in cluster_results['clusters'].items():
            cluster_info = cluster_results['cluster_info'].get(cluster_id, {})
            
            # 类别标题
            story.append(PageBreak())
            story.append(Paragraph(
                cluster_info.get("name", f"类别 {cluster_id}"),
                heading_style
            ))
            story.append(Paragraph(
                cluster_info.get("description", ""),
                styles['Normal']
            ))
            story.append(Spacer(1, 0.2*inch))
            
            # 添加图片（限制数量）
            for img_path in image_paths[:6]:  # 每类最多6张
                try:
                    # 先用PIL获取原始尺寸，保持宽高比
                    from PIL import Image as PILImage
                    pil_img = PILImage.open(img_path)
                    img_width, img_height = pil_img.size
                    pil_img.close()
                    
                    # 计算缩放比例，保持宽高比
                    max_width = 5 * inch
                    max_height = 4 * inch
                    
                    width_ratio = max_width / img_width
                    height_ratio = max_height / img_height
                    ratio = min(width_ratio, height_ratio)
                    
                    new_width = img_width * ratio
                    new_height = img_height * ratio
                    
                    # 创建RLImage时使用计算后的尺寸
                    img = RLImage(img_path, width=new_width, height=new_height)
                    story.append(img)
                    story.append(Spacer(1, 0.1*inch))
                except Exception as e:
                    print(f"添加PDF图片失败 {img_path}: {e}")
                    # 添加错误提示
                    story.append(Paragraph(
                        f"图片加载失败: {os.path.basename(img_path)}",
                        styles['Normal']
                    ))
                    story.append(Spacer(1, 0.1*inch))
        
        doc.build(story)
        return pdf_path
    
    def generate_folder_structure(self, cluster_results: Dict, output_dir: str) -> str:
        """
        生成文件夹结构
        
        Args:
            cluster_results: 聚类结果字典
            output_dir: 输出目录
            
        Returns:
            文件夹路径
        """
        folders_dir = os.path.join(output_dir, "folders")
        os.makedirs(folders_dir, exist_ok=True)
        
        for cluster_id, image_paths in cluster_results['clusters'].items():
            cluster_info = cluster_results['cluster_info'].get(cluster_id, {})
            cluster_name = cluster_info.get("name", f"类别_{cluster_id}")
            
            # 清理文件夹名称（移除非法字符）
            safe_name = "".join(c for c in cluster_name if c.isalnum() or c in (' ', '-', '_')).strip()
            cluster_folder = os.path.join(folders_dir, safe_name)
            os.makedirs(cluster_folder, exist_ok=True)
            
            # 复制图片
            for img_path in image_paths:
                img_name = os.path.basename(img_path)
                dest_path = os.path.join(cluster_folder, img_name)
                try:
                    shutil.copy2(img_path, dest_path)
                except Exception as e:
                    print(f"复制图片失败 {img_path}: {e}")
        
        return folders_dir
    
    def _get_default_html_template(self) -> str:
        """获取默认HTML模板"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ title }}</h1>
            <p class="subtitle">生成时间: {{ generated_time }}</p>
        </header>
        
        <nav class="categories">
            {% for cluster in clusters %}
            <a href="#cluster-{{ cluster.id }}" class="category-link">{{ cluster.name }} ({{ cluster.count }})</a>
            {% endfor %}
        </nav>
        
        <main>
            {% for cluster in clusters %}
            <section id="cluster-{{ cluster.id }}" class="cluster-section">
                <h2>{{ cluster.name }}</h2>
                <p class="cluster-description">{{ cluster.description }}</p>
                <div class="image-grid">
                    {% for image in cluster.images %}
                    <div class="image-item">
                        <img src="{{ image.src }}" alt="{{ image.alt }}" loading="lazy">
                    </div>
                    {% endfor %}
                </div>
            </section>
            {% endfor %}
        </main>
        
        <footer>
            <p>Gallery Generate Agent</p>
        </footer>
    </div>
</body>
</html>"""
    
    def _get_default_css(self) -> str:
        """获取默认CSS样式"""
        return """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    text-align: center;
    margin-bottom: 40px;
    padding: 30px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
}

header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 0.9em;
    opacity: 0.9;
}

.categories {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 30px;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.category-link {
    padding: 8px 16px;
    background: #667eea;
    color: white;
    text-decoration: none;
    border-radius: 20px;
    transition: background 0.3s;
}

.category-link:hover {
    background: #764ba2;
}

.cluster-section {
    margin-bottom: 50px;
    padding: 30px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.cluster-section h2 {
    color: #667eea;
    margin-bottom: 10px;
    font-size: 2em;
}

.cluster-description {
    color: #666;
    margin-bottom: 20px;
}

.image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
    margin-top: 20px;
}

.image-item {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.image-item:hover {
    transform: scale(1.05);
}

.image-item img {
    width: 100%;
    height: auto;
    display: block;
    transition: opacity 0.3s;
}

.image-item:hover img {
    opacity: 0.9;
}

footer {
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    color: #666;
}

@media (max-width: 768px) {
    .image-grid {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    }
    
    header h1 {
        font-size: 2em;
    }
}"""

