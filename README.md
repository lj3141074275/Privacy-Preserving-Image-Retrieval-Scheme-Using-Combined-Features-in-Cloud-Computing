# Privacy-Preserving Image Retrieval Scheme Using Combined Features in Cloud Computing
基于特征融合的云计算隐私保护图像检索方案

### 项目介绍
本项目为论文官方开源实现，面向云端加密图像安全检索场景，提供 AES 图像加解密、CNN+深度哈希组合特征提取、LWE+差分隐私特征加密、分层索引构建与密文域检索全流程功能。


### 安装依赖
pip install torch torchvision pillow pycryptodome numpy scikit-learn faiss-cpu

### 使用方法
#### 一键运行全流程
python main.py

#### 分步运行
python aes_image_encrypt.py
python feature_extract.py
python feature_encrypt.py
python index_build.py
python retrieval.py
python aes_image_decrypt.py

#### 模块说明
1. AES 图像加解密
算法：AES-128-CBC
作用：实现图像明文 / 密文转换，保护云端数据隐私
对应文件：aes_image_encrypt.py、aes_image_decrypt.py
2. 组合特征提取
CNN 特征：ResNet50 提取 2048 维语义特征
深度哈希：生成 64 维二值哈希特征
组合特征：2048+64=2112 维
对应文件：feature_extract.py
3. 特征加密
CNN 特征：LWE 格基加密
哈希特征：差分隐私（拉普拉斯噪声）
对应文件：feature_encrypt.py
4. 分层索引
第一层：CNN 特征 K-Means 聚类
第二层：哈希特征精匹配
实现亚线性检索
对应文件：index_build.py
5. 密文域检索
先匹配聚类簇 → 再计算汉明距离
输出 Top-K 相似图像
对应文件：retrieval.py


#### 项目声明
- 项目名称：Privacy-Preserving Image Retrieval Scheme Using Combined Features in Cloud Computing
- 作者：Liang Jing
- 单位：暨南大学网络空间安全学院
- 开发语言：Python
- 代码规模：约1200行
