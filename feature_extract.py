# -*- coding: utf-8 -*-
"""
特征提取模块
作用：提取CNN特征 + 深度哈希特征，生成论文组合特征
对应论文：Feature Extraction & Feature Combination
"""
import os
import torch
import numpy as np
from PIL import Image
import torchvision.models as models
import torchvision.transforms as T
from config import *

class FeatureExtractor:
    def __init__(self):
        self.cnn_model = self._load_cnn_model()
        self.transform = self._build_transform()

    def _load_cnn_model(self):
        """加载ResNet50提取CNN特征"""
        model = models.resnet50(pretrained=True)
        feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])
        feature_extractor.to(DEVICE)
        feature_extractor.eval()
        return feature_extractor

    def _build_transform(self):
        """图像预处理"""
        return T.Compose([
            T.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            T.ToTensor(),
            T.Normalize(mean=MEAN, std=STD)
        ])

    def preprocess_image(self, image_path):
        img = Image.open(image_path).convert("RGB")
        return self.transform(img).unsqueeze(0).to(DEVICE)

    def extract_cnn_feature(self, image_tensor):
        """提取CNN高维语义特征"""
        with torch.no_grad():
            feat = self.cnn_model(image_tensor)
        return feat.squeeze().cpu().numpy()

    def extract_deep_hash_feature(self, cnn_feature):
        """生成深度哈希二值特征"""
        hash_seed = int(np.sum(cnn_feature) % 100000)
        np.random.seed(hash_seed)
        random_proj = np.random.randn(CNN_FEATURE_DIM, HASH_FEATURE_DIM)
        hash_raw = np.dot(cnn_feature, random_proj)
        hash_binary = np.sign(hash_raw)
        hash_binary[hash_binary == 0] = 1
        return hash_binary.astype(np.float32)

    def get_combined_feature(self, image_path):
        """组合特征：CNN + Hash（论文核心）"""
        tensor = self.preprocess_image(image_path)
        cnn_feat = self.extract_cnn_feature(tensor)
        hash_feat = self.extract_deep_hash_feature(cnn_feat)
        combined = np.concatenate([cnn_feat, hash_feat], axis=0)
        return combined, cnn_feat, hash_feat

    def batch_extract(self, img_dir, save_path):
        """批量提取特征并保存"""
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        img_list = sorted([f for f in os.listdir(img_dir) if f.endswith(('jpg','png'))])

        features_combined = []
        features_cnn = []
        features_hash = []

        for idx, img_name in enumerate(img_list):
            img_path = os.path.join(img_dir, img_name)
            com_feat, cnn_feat, hash_feat = self.get_combined_feature(img_path)
            features_combined.append(com_feat)
            features_cnn.append(cnn_feat)
            features_hash.append(hash_feat)

            if (idx + 1) % 100 == 0:
                print(f"[特征提取] {idx + 1}/{len(img_list)}")

        np.save(save_path + "_combined.npy", np.array(features_combined))
        np.save(save_path + "_cnn.npy", np.array(features_cnn))
        np.save(save_path + "_hash.npy", np.array(features_hash))

        print(f"[特征保存完成] {save_path}")
        return features_combined, features_cnn, features_hash

if __name__ == "__main__":
    extractor = FeatureExtractor()
    extractor.batch_extract(DATASET_DIR, os.path.join(FEATURE_SAVE_DIR, "features"))