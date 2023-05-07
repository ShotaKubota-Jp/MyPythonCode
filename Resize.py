'''
画像を一括でリサイズするプログラム
ユーザにリサイズしたいディレクトリのサイズを指定させる
exeファイルにて実行することを想定

exeで固めるコマンド
　→pyinstaller --onefile Resize.py
'''

import os
from PIL import Image
import argparse

def get_image_files(directory):
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):
                image_files.append(os.path.join(root, file))
    return image_files

def main():
    print("########################################")
    print("##### 画像のリサイズを行います")
    print("##### 画像のパスとサイズを指定してください")
    print("########################################")
    # ユーザーからの入力を受け取る
    dir_path = input("リサイズしたいパス->")
    left = int(input("リサイズエリア(左)->"))
    right = int(input("リサイズエリア(右)->"))
    upper = int(input("リサイズエリア(上)->"))
    lower = int(input("リサイズエリア(下)->"))

    # リサイズしたい領域を指定
    box = (left, upper, right, lower)

    # ディレクトリ内の画像ファイルのパスを取得
    img_files = get_image_files(dir_path)

    # 画像をリサイズして保存する
    for img_file in img_files:
        image = Image.open(img_file)            # 画像を開く
        cropped_image = image.crop(box)         # 画像をリサイズ
        cropped_image.save(img_file)            # リサイズした画像を保存

if __name__ == '__main__':
    main()
