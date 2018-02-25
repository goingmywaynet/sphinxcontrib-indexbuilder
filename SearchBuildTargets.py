
# coding: utf-8

# In[1]:


# coding: -*- utf-8 -*-


# In[2]:


#


# In[3]:


import os.path                      # OS処理
from chardet.universaldetector import UniversalDetector # 文字エンコード自動判定
from collections import OrderedDict # 順序付き辞書(dict)


# In[4]:


# 定数
HEADLINE_DEPTH = 1               # index.rst でタイトル表示する階層数
TARGET_FILE_NAME = 'keyfile.txt' # 探索するファイル名
TARGET_PATH  = './test'          # 探索するパスの根 windows UNC path ("//host/computer/dir") を想定
SAVE_PATH = './tmp'              # 保存先パス
TARGET_LINK_NAME = 'Contents Folder' # .rst ファイル末尾に追記する元ファイルへのリンク名


# In[5]:


# Windows のセパレータ'\\'への対応として、セパレータが '/' ではない場合は、 '/' を os.sep (OSのデフォルトセパレータ) に置き換える
if os.sep != '/':
    print('re')
    root_path = TARGET_PATH.replace('/', os.sep)
    save_path = SAVE_PATH.replace('/',os.sep)
else:
    root_path = TARGET_PATH
    save_path = SAVE_PATH
        


# In[6]:


# 指定のファイル名がリストに存在するかの判定
def isContain(filelist, keywoard):
    for filename in filelist:
        if filename == keywoard:
            return True


# In[7]:


def returnHeading(title,depth=1):       # rst 見出し生成
    headingChar = ['=','-','^','"']
    depth = len(headingChar) if depth < 0 or depth > len(headingChar) else depth
    length = len(title.encode("utf8"))

    #print(title + os.linesep + "".join([headingChar[depth-1] for x in range(length)]))
    
    return title + os.linesep + "".join([headingChar[depth-1] for x in range(length)]) + os.linesep

    #print("".join([headingChar[depth-1] for x in range(length)]))
    #print(len(title.encode("utf8")))


# In[8]:


# 指定した path を巡回して、target_path_list を作る

def walk_path_to_target_path_list(search_root_path, target_file_name):

    #target_dict = OrderedDict() # 順序付き辞書(dict)
    _target_path_list = [] # 辞書入れリスト

    for _root, _dirs, _files in os.walk(search_root_path): # 相対path, サブディレクトリ, 内含ファイルリスト を走査

        #print( root,dirs,files) # debug

        if (isContain(_files, target_file_name)): # 指定するファイル名を含むディレクトリの場合は以下を処理
            _drive, _path = os.path.splitdrive(_root) # ネットワークドライブ名とパス名を分離         
            _target_dict = {'drive': _drive,                                 # windows 共有ディレクトリのドライブ名
                           'path': _path,                                   # target file を含まない path
                           'full_path': os.path.join(_path, target_file_name),   # target file を含む path
                           'name': os.path.basename(_path),                 # 最終ディレクトリ名を生成対象ファイル名に
                           'depth': _path.count(os.sep)}                    # 階層の深さを
            _target_path_list.append(_target_dict)

    return sorted(_target_path_list,key=lambda my_dict: my_dict['path'])


# In[9]:


# index.rst ファイルの中身を作る
def create_index_file(target_path_list, headline_depth):
    return_ = []                                          # return のためのリスト
    before_depth  = 65535
    depth_count   = 1

    for target in target_path_list:                       # target_path_list を順序良く評価していく
    #    print(target)
    #    print("before_depth =",before_depth)
    #    print("current_depth=",target['depth'])
    #    print("count        =",depth_count)
    #    print("end_depth    =",end_depth)

        if target['depth'] < before_depth :               # 評価の途中で階層が浅くなった場合は評価をリセット
            depth_count = 1                               # Headline 化階層カウンタ

        if target['depth'] > before_depth :               # 評価の途中で階層が深くなった場合はカウンタ++
            depth_count = depth_count + 1

        if depth_count <= headline_depth :                # カウンタが headline_depth 範囲内の場合は、見出し化する
            #print(depth_count)
            #print(os.linesep)
            #print(returnHeading(target['name'],depth_count))
            return_.append(os.linesep)
            return_.append(returnHeading(target['name'],depth_count))
            return_.append(os.linesep)

        else:
            print(target['name'])                         # カウンタが headline_depth 範囲外なら記事ファイルとする
            return_.append(target['name'])
            return_.append(os.linesep)

        before_depth = target['depth']                # 直前の深さを保持

    return return_


# In[10]:


# ディレクトリを走査して、対象ファイルのリストを生成する。
target_path_list = walk_path_to_target_path_list(root_path, TARGET_FILE_NAME)


# In[11]:


# index.rst ファイルを書き出す
index_txt = create_index_file(target_path_list, HEADLINE_DEPTH)
file = open(os.path.join(save_path,"index.rst"), mode='w', encoding='utf-8')
file.write("".join(index_txt))
file.close()


# In[12]:


# ファイルの文字エンコード判定
def detect_file_encode(file):
    detector = UniversalDetector()

    try:
        with open(file, mode='rb') as f:
            while True:
                binary = f.readline()
                if binary == b'':
                    # ファイルを最後まで読みきった
                    break

                detector.feed(binary)
                if detector.done:
                    # 十分な確度でエンコーディングが推定できた
                    break
    finally:
        detector.close()

    return detector.result
    #print(encoding_info)


# In[14]:


# ターゲットファイルを rst ファイル化
for target in target_path_list:
    if os.path.exists(target['full_path']): 
        
        #target_path_list の各ファイルを開いていく
        _encode = detect_file_encode(target['full_path'])["encoding"] # ファイルの文字コードを自動判定する
        if _encode == "SHIFT_JIS": _encode = "cp932"                  # 自動判定で SHIFT_JIS になる場合は予防的に上位互換の cp932 として扱う
        _file = open(target['full_path'],mode='r',encoding=_encode)
        _lines = _file.readlines()
        _file.close()
        
        #末尾にリンクを追記する
        _lines.append(os.linesep)
        _lines.append(":smblink:`{LINK_NAME} <{LINK_PATH}>`".format(LINK_NAME=TARGET_LINK_NAME, LINK_PATH=target['path']))
        _lines.append(os.linesep)
        
        #print(os.path.join(save_path,str(target['name']) + ".rst"))
        save_file = open(os.path.join(save_path,str(target['name']) + ".rst"), mode='w', encoding='utf-8')
        for _line in _lines:
            save_file.write(_line)
            #print(_line)        
        save_file.close()


# これらの関数の多くは Windows の一律命名規則 (UNCパス名) を正しくサポートしていません。 splitunc() と ismount() は正しく UNC パス名を操作できます。
# 
# os.path.splitunc(path)(原文)
# パス名 path をペア (unc, rest) に分割します。ここで unc は (r'\\host\mount' のような) UNC マウントポイント、そして rest は (r'\path\file.ext' のような) パスの残りの部分です。ドライブ名を含むパスでは常に unc が空文字列になります。
# 
# 利用可能: Windows
# 
# os.path.splitunc(path)
# Deprecated since version 3.1: Use splitdrive instead.
# 
