'''
Windows環境のディレクトリ・ファイルの名前にて、全角文字を半角に変換する
'''

import os

def rename_files(path):
    for root, dirs, files in os.walk(path):
        for name in files + dirs:
            src = os.path.join(root, name)
            dst = normalize_name(name)
            dst = os.path.join(root, dst)
            os.rename(src, dst)

def normalize_name(name):
	# 全角スペースを半角スペースに変換
    name = name.replace('　', ' ')
    name = name.replace('＃', '#')
    # 全角英数字を半角英数字に変換
    name = name.translate(str.maketrans('０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ', '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))
    name = name.replace('（', '(')
    name = name.replace('）', ')')
    name = name.replace('！', '!')
    name = name.replace('［', '【')
    name = name.replace('］', '】')
    return name

# 実行例
rename_files(r'')
# 上記にパスを指定する