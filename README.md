# Privacy-Preserving Image Retrieval Scheme Using Combined Features in Cloud Computing
基于组合特征的云计算隐私保护图像检索方案

## 项目介绍
本项目为论文官方开源实现，面向云端加密图像安全检索场景，提供 AES 图像加解密、CNN+深度哈希组合特征提取、LWE+差分隐私特征加密、分层索引构建与密文域检索全流程功能。

## 项目目录
├── data/                     # 数据集
├── encrypted_images/         # 加密图像
├── decrypted_images/         # 解密图像
├── features/                 # 特征文件
├── index/                    # 索引文件
├── aes_image_encrypt.py      # AES图像加密
├── aes_image_decrypt.py      # AES图像解密
├── config.py                 # 配置
├── feature_extract.py        # 组合特征提取
├── feature_encrypt.py        # 特征加密
├── index_build.py            # 分层索引
├── retrieval.py              # 密文检索
└── main.py                   # 主程序

## 安装依赖
pip install torch torchvision pillow pycryptodome numpy scikit-learn faiss-cpu

## 使用方法
# 一键运行全流程
python main.py

# 分步运行
python aes_image_encrypt.py
python feature_extract.py
python feature_encrypt.py
python index_build.py
python retrieval.py
python aes_image_decrypt.py

## 项目声明
- 项目名称：Privacy-Preserving Image Retrieval Scheme Using Combined Features in Cloud Computing
- 作者：Liang Jing
- 单位：暨南大学网络空间安全学院
- 开发语言：Python
- 代码规模：约1200行
