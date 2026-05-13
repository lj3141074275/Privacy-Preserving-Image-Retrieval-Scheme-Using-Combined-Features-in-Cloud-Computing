# -*- coding: utf-8 -*-
"""
分层索引构建模块
作用：构建双层索引：聚类中心层 + 哈希特征层
对应论文：Hierarchical Index Construction
"""
import os
import numpy as np
from sklearn.cluster import KMeans
from config import *

class HierarchicalIndex:
    def __init__(self, n_clusters=CLUSTER_NUM):
        self.n_clusters = n_clusters
        self.kmeans = None
        self.cluster_centers = None
        self.cluster_map = {}

    def build_cluster_index(self, cnn_features):
        """第一层：CNN特征聚类"""
        print(f"[聚类] K={self.n_clusters} 分层索引构建中...")
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=666)
        labels = self.kmeans.fit_predict(cnn_features)
        self.cluster_centers = self.kmeans.cluster_centers_

        for idx, label in enumerate(labels):
            if label not in self.cluster_map:
                self.cluster_map[label] = []
            self.cluster_map[label].append(idx)

        print(f"[聚类完成] 共 {self.n_clusters} 个簇，{len(labels)} 个图像")
        return labels, self.cluster_centers, self.cluster_map

    def save_index(self, save_path):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        np.save(save_path + "_centers.npy", self.cluster_centers)
        np.save(save_path + "_map.npy", self.cluster_map)
        print(f"[索引保存] {save_path}")

    def load_index(self, load_path):
        self.cluster_centers = np.load(load_path + "_centers.npy", allow_pickle=True)
        self.cluster_map = np.load(load_path + "_map.npy", allow_pickle=True).item()
        self.n_clusters = len(self.cluster_centers)
        print(f"[索引加载完成] 簇数={self.n_clusters}")

if __name__ == "__main__":
    cnn_feats = np.load(os.path.join(FEATURE_SAVE_DIR, "features_cnn.npy"))
    index = HierarchicalIndex()
    index.build_cluster_index(cnn_feats)
    index.save_index(os.path.join(INDEX_SAVE_DIR, "hierarchical_index"))