import os
from PIL import Image
import argparse
import pytesseract

RESIZE = 1
NAMECHANGE = 2
SELECTNAMECHANGE = 3
CONVERTPDF = 4
IMAGEEXTRACTION = 5

######################################################################################
# ディレクトリ確認
#-------------------------------------------------------------------------------------
def check_path_exists(title):
    while True:
        path = str(input(title))
        if os.path.exists(path):
            return path
        else:
            print(">>>>>>>>[ERROR!!!ERROR!!!ERROR!!!]")
            print("指定されたパスは存在しません。")

######################################################################################
# ファイル確認
#-------------------------------------------------------------------------------------
def check_file_exists(title):
    while True:
        filepath = str(input(title))
        if os.path.isfile(filepath):
            return filepath
        else:
            print(">>>>>>>>[ERROR!!!ERROR!!!ERROR!!!]")
            print(">>>>>>>>指定されたファイルは存在しません。")

######################################################################################
# リサイズ
#-------------------------------------------------------------------------------------
def get_image_files(directory):
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):
                image_files.append(os.path.join(root, file))
    return image_files

#-------------------------------------------------------------------------------------
def resize():
    print("########################################")
    print("##### 画像のトリミングを行います")
    print("##### 画像のパスとサイズを指定してください")
    # ユーザーからの入力を受け取る
    dir_path = input("トリミングしたいパス->")
    left = int(input("トリミングエリア(左)->"))
    right = int(input("トリミングエリア(右)->"))
    upper = int(input("トリミングエリア(上)->"))
    lower = int(input("トリミングエリア(下)->"))

    # トリミングしたい領域を指定
    box = (left, upper, right, lower)

    # ディレクトリ内の画像ファイルのパスを取得
    img_files = get_image_files(dir_path)

    # 画像をトリミングして保存する
    for img_file in img_files:
        image = Image.open(img_file)            # 画像を開く
        cropped_image = image.crop(box)         # 画像をトリミング
        cropped_image.save(img_file)            # トリミングした画像を保存

######################################################################################
# リネーム
#-------------------------------------------------------------------------------------
def rename_files():
    print("########################################")
    print("##### 指定したディレクトリとその配下にあるディレクトリとファイル名を変換します")
    print("##### 【例】")
    print("        （ -> (")
    print("        ！-> !")
    print("##### 変換したいディレクトリを指定してください")
    path = check_path_exists("@@@@@@@ パス->")

    for root, dirs, files in os.walk(path):
        for name in files + dirs:
            src = os.path.join(root, name)
            dst = normalize_name(name)
            dst = os.path.join(root, dst)
            os.rename(src, dst)

#-------------------------------------------------------------------------------------
def normalize_name(name):
    name = name.replace('　', ' ') # 全角スペースを半角スペースに変換
    name = name.replace('＃', '#')
    name = name.replace('♯', '#')
    # 全角英数字を半角英数字に変換
    name = name.translate(str.maketrans('０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ', '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))
    name = name.replace('（', '(')
    name = name.replace('）', ')')
    name = name.replace('！', '!')
    name = name.replace('［', '【')
    name = name.replace('］', '】')
    name = name.replace('．', ',')
    name = name.replace('；', ';')
    return name

######################################################################################
# 選択リネーム
#-------------------------------------------------------------------------------------
def select_rename_files():
    print("########################################")
    print("##### 指定したディレクトリとその配下にあるディレクトリとファイル名を変換します")
    print("##### 変換したいディレクトリを指定してください")
    path = check_path_exists("@@@@@@@ パス->")
    convBefore = str(input("@@@@@@@ 変換したい文言->"))
    convAfter = str(input("@@@@@@@ 変換後の文言->"))

    for root, dirs, files in os.walk( path ):
        for name in files + dirs:
            src = os.path.join( root, name )
            dst = select_normalize_name( name, convBefore, convAfter )
            dst = os.path.join( root, dst )
            os.rename( src, dst )

#-------------------------------------------------------------------------------------
def select_normalize_name( name, strBefore, strAfter ):
    name = name.replace( strBefore, strAfter )
    return name

######################################################################################
# PDF一括
#-------------------------------------------------------------------------------------
def create_pdf_from_images_in_directory(directory_path, directory_path_input):
    for subdir, dirs, files in os.walk(directory_path):
        # ディレクトリ内に画像ファイルがある場合のみ実行
        if files:
            images = []
            for file in files:
                if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
                    image_path = os.path.join(subdir, file)
                    # 画像をPIL.Imageで開く
                    image = Image.open(image_path)
                    # 画像をリストに追加
                    images.append(image)

            # 画像が1つ以上ある場合にPDFを生成
            if images:
                # 出力PDFファイル名を作成
                if directory_path_input == "1":
                    # プログラムの場所に保存
                    pdf_path = os.path.join(os.path.dirname(subdir), os.path.basename(subdir) + '.pdf')
                else:
                    # 一つ下の階層に保存
                    pdf_path = os.path.join(subdir, subdir.split(os.sep)[-1] + '.pdf')

                # 画像をPDFに変換して保存
                images[0].save(
                    pdf_path, 
                    "PDF", 
                    resolution=100.0, 
                    save_all=True, 
                    append_images=images[1:]
                )

#-------------------------------------------------------------------------------------
def ConvPDF():
    print("########################################")
    print("##### 指定したディレクトリの画像を一括して、PDFに変換します")
    print("##### PDFで一括したいディレクトリを指定してください")
    directory_path = check_file_exists("@@@@@@@ パス->")

    print("#####  【指定したディレクトリ配下】-> 1")
    print("#####  【サブディレクトリ配下】-> 2")
    while True:
        directory_path_input = input("@@@@@@@ 保存したい場所->")
        if directory_path_input in ["1", "2"]:
            create_pdf_from_images_in_directory(directory_path, directory_path_input)
            break
        else:
            print(">>>>>>>>[ERROR!!!ERROR!!!ERROR!!!]")
            print(">>>>>>>>無効な入力です")

######################################################################################
# 文字抽出
#-------------------------------------------------------------------------------------
def ImageExtraction():
    print("########################################")
    print("##### 画像から文字を抽出します")
    print("##### パスを指定してください")
    directory_path = check_file_exists("@@@@@@@ パス->")

    print("##### 抽出する言語は？")
    print("##### 日本語:1, 英語:2, 日本語+英語:3")
    while True:
        languageNum = int(input("@@@@@@@ 言語->"))    
        if languageNum == 1:
            # 画像を開く
            image = Image.open(directory_path)
            # 画像内の文字を抽出
            text = pytesseract.image_to_string(image, lang='jpn')
            break
        elif languageNum == 2:
            # 画像を開く
            image = Image.open(directory_path)
            # 画像内の文字を抽出
            text = pytesseract.image_to_string(image, lang='eng')
            break
        elif languageNum == 3:
            # 画像を開く
            image = Image.open(directory_path)
            # 画像内の文字を抽出
            text = pytesseract.image_to_string(image, lang='jpn+eng')
            break
        else:
            print(">>>>>>>>[ERROR!!!ERROR!!!ERROR!!!]")
            print(">>>>>>>>無効な入力です")

    # 抽出されたテキストを表示
    print(text)

######################################################################################
# MAIN関数
#-------------------------------------------------------------------------------------
def main():
    print("########################################")
    print("##### ツールを指定してください")
    print("##### -> 1：リサイズ")
    print("##### -> 2：ディレクトリ・ファイル名変更")
    print("##### -> 3：入力式ディレクトリ・ファイル名変更")
    print("##### -> 4：画像からPDFに一括結合")
    print("##### -> 5：画像から文字を抽出")
    print("#####     　＊Tesseract-OCRをインストールして下さい")
    print("########################################")

    while True:
        procNum = int(input("@@@@@@@ 指定->"))
        if procNum == RESIZE:
            resize()
            break
        elif procNum == NAMECHANGE:
            rename_files()
            break
        elif procNum == SELECTNAMECHANGE:
            select_rename_files()
            break
        elif procNum == CONVERTPDF:
            ConvPDF()
            break
        elif procNum == IMAGEEXTRACTION:
            ImageExtraction()
            break
        else:
            print(">>>>>>>>[ERROR!!!ERROR!!!ERROR!!!]")
            print(">>>>>>>>無効な入力です")

#-------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

# exeファイルに固めるコマンド
# pyinstaller --onefile Tool.py
# 完成しているプログラム
