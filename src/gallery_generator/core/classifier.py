"""
图像分类和聚类模块
使用聚类算法将相似图片归类
"""

import json
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from typing import List, Dict, Tuple
from collections import defaultdict

from gallery_generator.models.clip_model import CLIPFeatureExtractor


class ImageClassifier:
    """图像分类器"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化分类器
        
        Args:
            config_path: 配置文件路径
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        clustering_config = self.config.get("clustering", {})
        self.algorithm = clustering_config.get("algorithm", "kmeans")
        self.n_clusters = clustering_config.get("n_clusters", "auto")
        self.auto_method = clustering_config.get("auto_cluster_method", "elbow")
        self.min_samples = clustering_config.get("min_samples", 5)
        
        # 初始化CLIP用于生成类别标签
        model_config = self.config.get("model", {})
        self.clip_extractor = CLIPFeatureExtractor(
            model_name=model_config.get("clip_model_name", "openai/clip-vit-base-patch32"),
            device=model_config.get("device", "auto")
        )
    
    def cluster_images(self, features: np.ndarray, image_paths: List[str]) -> Dict:
        """
        对图像进行聚类
        
        Args:
            features: 特征向量数组
            image_paths: 图片路径列表
            
        Returns:
            聚类结果字典，包含类别标签、类别信息等
        """
        if len(features) < 2:
            return {
                "labels": [0] * len(features),
                "clusters": {0: image_paths},
                "cluster_info": {0: {"name": "所有图片", "count": len(image_paths)}}
            }
        
        # 确定聚类数量
        if self.algorithm == "kmeans":
            n_clusters = self._determine_clusters(features) if self.n_clusters == "auto" else self.n_clusters
            labels = self._kmeans_cluster(features, n_clusters)
        else:
            labels = self._dbscan_cluster(features)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        
        # 组织聚类结果
        clusters = defaultdict(list)
        for idx, label in enumerate(labels):
            clusters[label].append(image_paths[idx])
        
        # 生成类别名称和描述
        cluster_info = self._generate_cluster_names(clusters, features, labels)
        
        return {
            "labels": labels.tolist() if isinstance(labels, np.ndarray) else labels,
            "clusters": dict(clusters),
            "cluster_info": cluster_info,
            "n_clusters": n_clusters
        }
    
    def _determine_clusters(self, features: np.ndarray) -> int:
        """
        自动确定最佳聚类数量
        
        Args:
            features: 特征向量数组
            
        Returns:
            最佳聚类数量
        """
        if len(features) < 2:
            return 1
        
        max_clusters = min(10, len(features) // 2)
        if max_clusters < 2:
            return 1
        
        if self.auto_method == "elbow":
            return self._elbow_method(features, max_clusters)
        else:
            return self._silhouette_method(features, max_clusters)
    
    def _elbow_method(self, features: np.ndarray, max_k: int) -> int:
        """肘部法则确定聚类数"""
        if max_k < 2:
            return 1
        
        inertias = []
        k_range = range(1, max_k + 1)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(features)
            inertias.append(kmeans.inertia_)
        
        # 简化版：选择中间值
        # 实际可以使用更复杂的肘部检测算法
        return max(2, max_k // 2)
    
    def _silhouette_method(self, features: np.ndarray, max_k: int) -> int:
        """轮廓系数法确定聚类数"""
        if len(features) < 3:
            return 1
        
        scores = []
        k_range = range(2, min(max_k + 1, len(features)))
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(features)
            if len(set(labels)) > 1:
                score = silhouette_score(features, labels)
                scores.append((k, score))
        
        if not scores:
            return 2
        
        # 返回轮廓系数最高的k值
        best_k, _ = max(scores, key=lambda x: x[1])
        return best_k
    
    def _kmeans_cluster(self, features: np.ndarray, n_clusters: int) -> np.ndarray:
        """KMeans聚类"""
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(features)
        return labels
    
    def _dbscan_cluster(self, features: np.ndarray) -> np.ndarray:
        """DBSCAN聚类"""
        # 自适应eps参数
        from sklearn.neighbors import NearestNeighbors
        neighbors = NearestNeighbors(n_neighbors=self.min_samples)
        neighbors_fit = neighbors.fit(features)
        distances, _ = neighbors_fit.kneighbors(features)
        distances = np.sort(distances, axis=0)
        distances = distances[:, self.min_samples - 1]
        eps = np.percentile(distances, 50)  # 使用中位数作为eps
        
        dbscan = DBSCAN(eps=eps, min_samples=self.min_samples)
        labels = dbscan.fit_predict(features)
        return labels
    
    def _generate_cluster_names(self, clusters: Dict, features: np.ndarray, labels: List) -> Dict:
        """
        为每个聚类生成名称和描述
        
        Args:
            clusters: 聚类结果字典
            features: 特征向量数组
            labels: 聚类标签列表
            
        Returns:
            聚类信息字典
        """
        cluster_info = {}
        
        # 预定义的类别关键词
        category_keywords = [
            "废墟", "建筑", "城市", "自然", "山", "海", "水", "森林", "天空",
            "人物", "肖像", "人文", "生活", "文化", "艺术", "抽象", "风景",
            "夜景", "日出", "日落", "动物", "植物", "花卉", "静物", "美食"
        ]
        
        for cluster_id, image_paths in clusters.items():
            if cluster_id == -1:  # DBSCAN的噪声点
                cluster_info[cluster_id] = {
                    "name": "未分类",
                    "count": len(image_paths),
                    "description": "未归类的图片"
                }
                continue
            
            # 计算该聚类的中心特征
            cluster_indices = [i for i, label in enumerate(labels) if label == cluster_id]
            if not cluster_indices:
                continue
            
            cluster_features = features[cluster_indices]
            centroid = np.mean(cluster_features, axis=0)
            
            # 使用CLIP匹配最相关的类别关键词
            try:
                text_features = self.clip_extractor.get_text_features(category_keywords)
                similarities = np.dot(centroid, text_features.T)
                best_match_idx = np.argmax(similarities)
                category_name = category_keywords[best_match_idx]
            except:
                category_name = f"类别 {cluster_id + 1}"
            
            cluster_info[cluster_id] = {
                "name": category_name,
                "count": len(image_paths),
                "description": f"包含 {len(image_paths)} 张相似图片"
            }
        
        return cluster_info

