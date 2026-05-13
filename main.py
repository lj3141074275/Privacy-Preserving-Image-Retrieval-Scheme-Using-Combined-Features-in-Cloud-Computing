# -*- coding: utf-8 -*-
"""
项目主入口
作用：一键运行：AES加密 → 特征提取 → 特征加密 → 建索引 → 密文检索 → AES解密
"""
from aes_image_encrypt import AesImageEncryptor
from aes_image_decrypt import AesImageDecryptor
from feature_extract import FeatureExtractor
from feature_encrypt import FeatureEncryptor
from index_build import HierarchicalIndex
from retrieval import SecureRetrieval
from config import *
import os

def main():
    print("=" * 70)
    print("  Privacy-Preserving Image Retrieval Scheme Using Combined Features")
    print("  基于组合特征的云计算隐私保护图像检索方案（AES加密版）")
    print("=" * 70)

    # 1 AES图像加密
    print("\n[1/6] AES 图像加密...")
    encryptor = AesImageEncryptor()
    encryptor.batch_encrypt(DATASET_DIR, ENCRYPTED_IMG_DIR)

    # 2 组合特征提取
    print("\n[2/6] 组合特征提取...")
    extractor = FeatureExtractor()
    com_feat, cnn_feat, hash_feat = extractor.batch_extract(DATASET_DIR, os.path.join(FEATURE_SAVE_DIR, "features"))

    # 3 特征加密
    print("\n[3/6] 特征加密（LWE + 差分隐私）...")
    feat_enc = FeatureEncryptor()
    enc_cnn, enc_hash = feat_enc.batch_encrypt_features(cnn_feat, hash_feat)
    np.save(os.path.join(FEATURE_SAVE_DIR, "enc_cnn.npy"), enc_cnn)
    np.save(os.path.join(FEATURE_SAVE_DIR, "enc_hash.npy"), enc_hash)

    # 4 构建分层索引
    print("\n[4/6] 构建分层索引...")
    index = HierarchicalIndex()
    index.build_cluster_index(cnn_feat)
    index.save_index(os.path.join(INDEX_SAVE_DIR, "hierarchical_index"))

    # 5 密文域安全检索
    print("\n[5/6] 执行密文检索...")
    retrieval = SecureRetrieval()
    query_img = os.path.join(DATASET_DIR, os.listdir(DATASET_DIR)[0])
    retrieval.retrieve(query_img)

    # 6 AES图像解密
    print("\n[6/6] AES 图像解密...")
    decryptor = AesImageDecryptor()
    decryptor.batch_decrypt(ENCRYPTED_IMG_DIR, DECRYPTED_IMG_DIR)

    print("\n[全部流程完成]")

if __name__ == "__main__":
    main()