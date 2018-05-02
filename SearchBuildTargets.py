
# coding: utf-8

# In[ ]:


# coding: -*- utf-8 -*-


# In[ ]:


"""SearchBuildTargets.py

Overview:
  指定ディレクトリを走査し、index.rst と ディレクトリ名.rst を生成するスクリプトです。
  
  各ディレクトリに指定のファイル名 (000_IndexFile.txtなど)をターゲットファイル名として、
  これの存在を検索します。
  ターゲットファイル名が存在する場合は、ターゲットファイルを当該ファイルのカレントディレクトリ名
  で rename し、 foldername.rst として保存します。
  また、生成した各 .rst を集約した index.rst も生成します。

Usage:
  SearchBuildTargets SEARCH_FROM 
                     [-o <path>     | --saveto=<path>]
                     [-t <filename> | --targetname=<filename>]
                     [-d <number>   | --headingdepth=<number>]
                     [-l <text>     | --linktext=<text>]           
  SearchBuildTargets [-h] [--help]

Options:
  SEARCH_FROM                   : 検索対象ディレクトリ ex. './search' or \\\\path\\to\\search
  -o, --saveto=<path>           : 処理結果の出力先 ex. './tmp' or \\\\save\\to\\ [default: .] *save to current directory
  -t, --targetname=<filename>   : ターゲットファイル名   [default: keyfile.txt]
  -d, --headingdepth=<number>   : 見出しとして使う階層数 [default: 1]
  -l, --linktext=<text>         : rstファイル末尾に付加する検索されたフォルダへのリンク名。定義ない場合は作成しない。 [default: none]
  -h, --help                    : show this help message and exit

"""


# In[ ]:


import os.path                      # OS処理
from chardet.universaldetector import UniversalDetector # 文字エンコード自動判定
from collections import OrderedDict # 順序付き辞書(dict)
from docopt import docopt           # コマンド処理時の引数の定義と解釈


# In[ ]:


MYVERSION = '0.1 20180303'  # このScriptのVersion


# In[ ]:


# 指定のファイル名がリストに存在するかの判定
def isContain(filelist, keywoard):
    for filename in filelist:
        if filename == keywoard:
            return True


# In[ ]:


def returnHeading(title,depth=1):       # rst 見出し生成
    headingChar = ['=','-','^','"']
    depth = len(headingChar) if depth < 0 or depth > len(headingChar) else depth
    length = len(title.encode("utf8"))

    #print(title + os.linesep + "".join([headingChar[depth-1] for x in range(length)]))
    
    return title + os.linesep + "".join([headingChar[depth-1] for x in range(length)]) + os.linesep

    #print("".join([headingChar[depth-1] for x in range(length)]))
    #print(len(title.encode("utf8")))


# In[ ]:


# index.rst ファイルの中身を作る
def create_index_file(target_path_list, headline_depth):
    return_ = []                                          # return のためのリスト
    
    before_depth  = 65535                                 # 階層の深さを比較するための初期値
                                                          #  （初期は必ずタイトルなので、これ以上にない深さにしておく）
    before_target = target_path_list[0]                   # あとで評価の枝が移動したことを検知するために1件目を
                                                          # 比較対象として持っておく
    depth_count   = 1                                     # 評価階層の深さの初期値

    for target in target_path_list:                       # target_path_list を順序良く評価していく
    #    print(target)
    #    print("before_depth =",before_depth)
    #    print("current_depth=",target['depth'])
    #    print("count        =",depth_count)
    #    print("end_depth    =",end_depth)
    
    
        # 現在位置比較のための情報を作る
        before_path  = before_target['path'].split(os.sep)          # 直前の評価位置
        current_path = target['path'].split(os.sep)                 # 現在の評価位置
        comp_depth = min(target['depth'], before_target['depth'])   # 評価位置の階層が変わった場合は浅い方で比較        
        #print(before_path , current_path)
        #print(before_path[:comp_depth])
        #print(current_path[:comp_depth])
        

        if target['depth'] < before_depth :               # 評価の途中で現在位置が前回より階層が浅くなった場合は評価をリセット
                                                          # 階層をリセットすると、この評価対象は Headline化階層より浅くなり
                                                          # Headline 化される
            depth_count = 1                               # Headline 化階層カウンタ = 1 = 必ずHeadline化
            #print("reset")

        if before_path[:comp_depth] != current_path[:comp_depth] : # 評価パスが違う枝に移動した場合リセット
            depth_count = 1                               # Headline 化階層カウンタ
            #print("reset")
     
        elif target['depth'] > before_depth :             # 評価の途中で階層が深くなった場合はカウンタ++
            depth_count = depth_count + 1
            

        if depth_count <= headline_depth :                # カウンタが headline_depth 範囲内の場合は、見出し化する
            return_.append(os.linesep)
            return_.append(returnHeading(target['name'],depth_count))
            return_.append(os.linesep)
            #print(depth_count)
            #print(returnHeading(target['name'],depth_count))

        else:                                             # カウンタが headline_depth 範囲外なら記事ファイルとする
            return_.append(target['name'])
            return_.append(os.linesep)
            #print(target['name'])

        before_depth = target['depth']                # 直前の深さを保持
        before_target = target                        # 直前の対象を保持

    return return_


# In[ ]:


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


# In[ ]:


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


# # 定数
# HEADLINE_DEPTH = 1               # index.rst でタイトル表示する階層数
# TARGET_FILE_NAME = 'keyfile.txt' # 探索するファイル名
# TARGET_PATH  = r'./test'          # 探索するパスの根 windows UNC path ("//host/computer/dir") を想定
# #TARGET_PATH  = r'\\win7\Public\Documents\test' # Windows SMB
# SAVE_PATH = r'./tmp'              # 保存先パス
# #SAVE_PATH = r'\\win7\Public\Documents\tmp' # Windows SMB
# TARGET_LINK_NAME = 'Contents Folder' # .rst ファイル末尾に追記する元ファイルへのリンク名

# In[ ]:


# MAIN 処理
if __name__ == '__main__':
    arguments = docopt(__doc__, version=MYVERSION)
    
    # 引数の整理
    HEADLINE_DEPTH   = int(arguments['--headingdepth']) # index.rst でタイトル表示する階層数
    TARGET_FILE_NAME = arguments['--targetname']   # 探索するファイル名
    TARGET_PATH      = arguments['SEARCH_FROM']    # 探索するパスの根 windows UNC path ("//host/computer/dir") を想定
    SAVE_PATH        = arguments['--saveto']       # 保存先パス
    TARGET_LINK_NAME = arguments['--linktext']     # .rst ファイル末尾に追記する元ファイルへのリンク名 'none'なら作らない
    #print(arguments)
    
    # 検索先定義がない場合は終了する
    if TARGET_PATH == None or not os.path.exists(TARGET_PATH):
        print('検索先が見つからなかった為、終了します。')
        import sys
        sys.exit(1) 
        
    # Windows のセパレータ'\\'への対応として、セパレータが '/' ではない場合は、 '/' を os.sep (OSのデフォルトセパレータ) に置き換える
    if os.sep != '/':
        root_path = TARGET_PATH.replace('/', os.sep)
        save_path = SAVE_PATH.replace('/',os.sep)
        print('Windows用に / から ' + os.sep +  ' へセパレータの置き換え実施しました。')
    else:
        root_path = TARGET_PATH
        save_path = SAVE_PATH

    
    # ディレクトリを走査して、対象ファイルのリストを生成する。
    target_path_list = walk_path_to_target_path_list(root_path, TARGET_FILE_NAME)

    # index.rst ファイルを書き出す
    index_txt = create_index_file(target_path_list, HEADLINE_DEPTH)
    file = open(os.path.join(save_path,"index.rst"), mode='w', encoding='utf-8')
    file.write("".join(index_txt))
    file.close()

    # ターゲットファイルを rst ファイル化
    for target in target_path_list:

        _full_path = os.path.join(target['drive'], target['full_path'])    # windows network drive path

        if os.path.exists(_full_path): 
            #target_path_list の各ファイルを開いていく
            _encode = detect_file_encode(_full_path)["encoding"] # ファイルの文字コードを自動判定する
            if _encode == "SHIFT_JIS": _encode = "cp932"                  # 自動判定で SHIFT_JIS になる場合は予防的に上位互換の cp932 として扱う
            _file = open(_full_path,mode='r',encoding=_encode)
            _lines = _file.readlines()
            _file.close()

            if TARGET_LINK_NAME != 'none':
                #末尾にリンクを追記する
                _lines.append(os.linesep)
                _lines.append(":smblink:`{LINK_NAME} <{LINK_PATH}>`".format(LINK_NAME=TARGET_LINK_NAME, 
                                                                            LINK_PATH=os.path.join(target['drive'],
                                                                                                   target['path'])))
            _lines.append(os.linesep)

            #print(os.path.join(save_path,str(target['name']) + ".rst"))
            save_file = open(os.path.join(save_path,str(target['name']) + ".rst"), mode='w', encoding='utf-8')
            for _line in _lines:
                save_file.write(_line)
                #print(_line)        
            save_file.close()

