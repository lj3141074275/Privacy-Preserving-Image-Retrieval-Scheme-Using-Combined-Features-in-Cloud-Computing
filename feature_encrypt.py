# -- coding utf-8 --

特征加密模块
作用：对CNN特征做LWE加密，对哈希特征做差分隐私加密
对应论文：Index Encryption（LWE + DP）

import numpy as np
from config import 

class LWEEncryptor
    LWE加密（用于CNN特征）
    def __init__(self, p=LWE_PRIME_P, q=LWE_PRIME_Q, key=FEATURE_ENCRYPT_KEY)
        self.p = p
        self.q = q
        np.random.seed(key)
        self.M = np.random.randn(CNN_FEATURE_DIM + 10, CNN_FEATURE_DIM + 10)
        self.M_inv = np.linalg.inv(self.M)
        self.gamma = np.random.randint(1000, 10000)

    def encrypt_cnn_feature(self, cnn_feat)
        extended = np.concatenate([cnn_feat, [np.linalg.norm(cnn_feat)], np.random.randn(8)])
        noise = np.random.normal(0, 0.001, size=extended.shape)
        encrypted = (self.gamma  extended + noise) @ self.M
        return encrypted.astype(np.float32)

    def decrypt_cnn_feature(self, enc_cnn)
        decrypted = (enc_cnn @ self.M_inv)  self.gamma
        return decrypted[CNN_FEATURE_DIM]

class DifferentialPrivacyEncryptor
    差分隐私加密（用于哈希特征）
    def __init__(self, eps=DIFFERENTIAL_PRIVACY_EPS)
        self.eps = eps
        self.sensitivity = 2.0

    def laplace_noise(self, size)
        scale = self.sensitivity  self.eps
        return np.random.laplace(loc=0, scale=scale, size=size)

    def encrypt_hash_feature(self, hash_feat)
        shuffled = np.random.permutation(hash_feat)
        noise = self.laplace_noise(shuffled.shape)
        dp_feat = shuffled + noise
        dp_feat = np.sign(dp_feat)
        dp_feat[dp_feat == 0] = 1
        return dp_feat.astype(np.float32)

class FeatureEncryptor
    def __init__(self)
        self.lwe = LWEEncryptor()
        self.dp = DifferentialPrivacyEncryptor()

    def encrypt_combined_feature(self, cnn_feat, hash_feat)
        enc_cnn = self.lwe.encrypt_cnn_feature(cnn_feat)
        enc_hash = self.dp.encrypt_hash_feature(hash_feat)
        return enc_cnn, enc_hash

    def batch_encrypt_features(self, cnn_list, hash_list)
        enc_cnn_list = []
        enc_hash_list = []

        for cnn, hash_f in zip(cnn_list, hash_list)
            enc_cnn, enc_hash = self.encrypt_combined_feature(cnn, hash_f)
            enc_cnn_list.append(enc_cnn)
            enc_hash_list.append(enc_hash)

        print(f[特征加密完成] 共加密 {len(enc_cnn_list)} 个特征)
        return np.array(enc_cnn_list), np.array(enc_hash_list)

if __name__ == __main__
    cnn_feats = np.load(os.path.join(FEATURE_SAVE_DIR, features_cnn.npy))
    hash_feats = np.load(os.path.join(FEATURE_SAVE_DIR, features_hash.npy))

    enc = FeatureEncryptor()
    enc_cnn, enc_hash = enc.batch_encrypt_features(cnn_feats, hash_feats)

    np.save(os.path.join(FEATURE_SAVE_DIR, enc_cnn.npy), enc_cnn)
    np.save(os.path.join(FEATURE_SAVE_DIR, enc_hash.npy), enc_hash)