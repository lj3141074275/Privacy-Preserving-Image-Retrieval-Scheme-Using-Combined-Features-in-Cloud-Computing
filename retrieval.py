# -*- coding: utf-8 -*-
"""
安全检索模块
作用：密文域双层检索：聚类匹配 → 哈希匹配 → 返回Top-K
对应论文：Search 算法
"""
import os
import numpy as np
from config import *
from feature_extract import FeatureExtractor
from feature_encrypt import FeatureEncryptor
from index_build import HierarchicalIndex

class SecureRetrieval:
    def __init__(self):
        self.extractor = FeatureExtractor()
        self.feat_enc = FeatureEncryptor()
        self.index = HierarchicalIndex()
        self.index.load_index(os.path.join(INDEX_SAVE_DIR, "hierarchical_index"))
        self.hash_feats = np.load(os.path.join(FEATURE_SAVE_DIR, "enc_hash.npy"))
        self.img_list = sorted([f for f in os.listdir(DATASET_DIR) if f.endswith(('jpg','png'))])

    def hamming_distance(self, a, b):
        """汉明距离（哈希特征相似度）"""
        return np.sum(a != b)

    def search_best_cluster(self, query_cnn):
        """第一层：匹配聚类中心"""
        distances = [np.linalg.norm(query_cnn - center) for center in self.index.cluster_centers]
        best_label = np.argmin(distances)
        candidate_ids = self.index.cluster_map[best_label]
        print(f"[检索] 最佳簇: {best_label}, 候选数: {len(candidate_ids)}")
        return candidate_ids

    def search_in_cluster(self, query_hash, candidate_ids, top_k=TOP_K):
        """第二层：哈希特征检索"""
        distances = []
        for idx in candidate_ids:
            d = self.hamming_distance(query_hash, self.hash_feats[idx])
            distances.append((idx, d))
        distances.sort(key=lambda x: x[1])
        return distances[:top_k]

    def retrieve(self, query_img_path, top_k=TOP_K):
        """完整检索流程"""
        print(f"[查询图像] {query_img_path}")

        # 1. 提取特征
        _, cnn_q, hash_q = self.extractor.get_combined_feature(query_img_path)

        # 2. 加密特征
        _, enc_hash_q = self.feat_enc.encrypt_combined_feature(cnn_q, hash_q)

        # 3. 双层检索
        candidates = self.search_best_cluster(cnn_q)
        top_results = self.search_in_cluster(enc_hash_q, candidates, top_k)

        # 4. 输出结果
        print("\n===== 检索结果（Top-%d）=====" % top_k)
        result_imgs = []
        for rank, (idx, dist) in enumerate(top_results):
            img_name = self.img_list[idx]
            print(f"第{rank+1}名: {img_name} | 汉明距离: {dist}")
            result_imgs.append(img_name)

        return result_imgs, top_results

if __name__ == "__main__":
    retrieval = SecureRetrieval()
    query_img = os.path.join(DATASET_DIR, os.listdir(DATASET_DIR)[0])
    retrieval.retrieve(query_img)