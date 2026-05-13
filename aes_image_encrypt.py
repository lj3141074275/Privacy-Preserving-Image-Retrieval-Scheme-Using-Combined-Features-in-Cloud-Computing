# -*- coding: utf-8 -*-
"""
AES 图像加密模块
作用：对图像进行 AES-128 CBC 模式加密
对应论文：图像加密保护模块 ImgEnc
安全性：对称加密，符合云计算隐私保护要求
"""
import os
import numpy as np
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from config import *

class AesImageEncryptor:
    def __init__(self, key=AES_KEY, iv=AES_IV):
        self.key = key
        self.iv = iv
        self.aes = AES.new(self.key, AES.MODE_CBC, self.iv)

    def encrypt_image(self, image_path, save_path):
        """AES 加密单张图像"""
        try:
            # 读取图像
            img = Image.open(image_path).convert("RGB")
            img_np = np.array(img)
            img_bytes = img_np.tobytes()
            shape_info = bytes(str(img_np.shape) + "|" + str(np.prod(img_np.shape)), encoding='utf-8')
            data = shape_info + b"|||" + img_bytes

            # AES 加密
            padded_data = pad(data, AES.block_size)
            encrypted_data = self.aes.encrypt(padded_data)

            # 保存加密文件
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(encrypted_data)

            if PRINT_PROCESS:
                print(f"[AES 加密完成] {os.path.basename(image_path)}")
            return True
        except Exception as e:
            print(f"[加密错误] {image_path}: {str(e)}")
            return False

    def batch_encrypt(self, img_dir, save_dir):
        """批量 AES 加密文件夹图像"""
        os.makedirs(save_dir, exist_ok=True)
        img_list = [f for f in os.listdir(img_dir) if f.endswith(('jpg', 'png', 'jpeg'))]

        for idx, img_name in enumerate(img_list):
            src = os.path.join(img_dir, img_name)
            dst = os.path.join(save_dir, f"enc_{img_name}.aes")
            self.encrypt_image(src, dst)

            if (idx + 1) % 100 == 0:
                print(f"[批量加密] 已完成 {idx + 1}/{len(img_list)}")

        print(f"[AES 批量加密完成] 总计加密 {len(img_list)} 张图像")

if __name__ == "__main__":
    encryptor = AesImageEncryptor()
    encryptor.batch_encrypt(DATASET_DIR, ENCRYPTED_IMG_DIR)