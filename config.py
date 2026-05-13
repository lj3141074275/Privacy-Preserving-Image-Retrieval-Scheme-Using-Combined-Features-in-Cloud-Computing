# -*- coding: utf-8 -*-
"""
全局配置文件
作用：统一管理项目参数、路径、模型配置、加密密钥
对应论文：系统参数设置模块
"""
import torch
import numpy as np

# 基础路径配置
DATASET_DIR = "./data/Corel-10K"
ENCRYPTED_IMG_DIR = "./data/encrypted_images"
DECRYPTED_IMG_DIR = "./data/decrypted_images"
FEATURE_SAVE_DIR = "./features"
INDEX_SAVE_DIR = "./index"
LOG_DIR = "./log"

# 图像预处理参数
IMAGE_SIZE = 224
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

# 特征维度配置（论文核心参数）
CNN_FEATURE_DIM = 2048
HASH_FEATURE_DIM = 64
COMBINED_FEATURE_DIM = CNN_FEATURE_DIM + HASH_FEATURE_DIM

# AES 加密密钥（16位 = 128位加密）
AES_KEY = b'1234567890123456'
AES_IV = b'abcdefghijklmnop'

# 特征加密密钥
FEATURE_ENCRYPT_KEY = 987654321
LWE_PRIME_P = 1000003
LWE_PRIME_Q = 100003
DIFFERENTIAL_PRIVACY_EPS = 1.0

# 聚类与检索参数
CLUSTER_NUM = 10
TOP_K = 10
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# 日志与保存
SAVE_LOG = True
PRINT_PROCESS = True