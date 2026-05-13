# -*- coding: utf-8 -*-
"""
AES 图像解密模块
作用：对 AES 加密的图像进行解密恢复
对应论文：图像解密模块 ImgDec
"""
import os
import numpy as np
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from config import *

class AesImageDecryptor:
    def __init__(self, key=AES_KEY, iv=AES_IV):
        self.key = key
        self.iv = iv
        self.aes = AES.new(self.key, AES.MODE_CBC, self.iv)

    def decrypt_image(self, enc_path, save_path):
        """AES 解密单张图像"""
        try:
            # 读取加密文件
            with open(enc_path, "rb") as f:
                encrypted_data = f.read()

            # AES 解密
            decrypted_padded = self.aes.decrypt(encrypted_data)
            decrypted_data = unpad(decrypted_padded, AES.block_size)

            # 解析图像形状与数据
            parts = decrypted_data.split(b"|||")
            shape_part = parts[0].decode()
            shape = eval(shape_part.split("|")[0])
            img_bytes = parts[1]
            img_np = np.frombuffer(img_bytes, dtype=np.uint8).reshape(shape)

            # 保存恢复图像
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            Image.fromarray(img_np).save(save_path)

            if PRINT_PROCESS:
                print(f"[AES 解密完成] {os.path.basename(enc_path)}")
            return True
        except Exception as e:
            print(f"[解密错误] {enc_path}: {str(e)}")
            return False

    def batch_decrypt(self, enc_dir, save_dir):
        """批量 AES 解密图像"""
        os.makedirs(save_dir, exist_ok=True)
        enc_list = [f for f in os.listdir(enc_dir) if f.endswith(".aes")]

        for idx, aes_name in enumerate(enc_list):
            src = os.path.join(enc_dir, aes_name)
            dst = os.path.join(save_dir, f"dec_{aes_name[4:-4]}.png")
            self.decrypt_image(src, dst)

            if (idx + 1) % 100 == 0:
                print(f"[批量解密] 已完成 {idx + 1}/{len(enc_list)}")

        print(f"[AES 批量解密完成] 总计解密 {len(enc_list)} 张图像")

if __name__ == "__main__":
    decryptor = AesImageDecryptor()
    decryptor.batch_decrypt(ENCRYPTED_IMG_DIR, DECRYPTED_IMG_DIR)