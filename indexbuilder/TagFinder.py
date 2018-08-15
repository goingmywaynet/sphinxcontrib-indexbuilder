
# coding: utf-8

# In[1]:


# coding: -*- utf-8 -*-


# In[1]:


"""TagFinder.py

Overview:
  Sphinx 独自ディレクティブ
  .. tagfinder:: ディレクティブと tagfile によりインデックスを生成するho

Usage:

    - 以下のディレクティブを書くと、指定パス(tagSearchPath) に対してフォルダとファイル名の走査を行う::

      .. tagfinder::
        :file: tagFileName
        :tag: tagname
        :path: \\file\to


    - 指定ファイル名(tagFileName) にがあるフォルダパスを抽出 (tag_path_list)

      指定ファイルの書き方::

        Title
        :tftag: tagname, tagname2, tagname3
        :desc: description


    - tag_path_list の各ファイルに対して以下の処理を行う

      ファイル内に指定の文字列(tagname)が存在するか検索

      存在する場合は、当該ファイルの一行目をタイトル、フォルダパスとして取得し、リンクリスト化::

        `title <file://file/to/path/>`, "description"
        `title <file://file/to/path/>`, "description"
        `title <file://file/to/path/>`, "description"
"""


# In[2]:


from docutils import nodes          # html生成処理
import re                           # 正規表現処理
import string                       # 文字処理


# In[3]:


import os.path                      # OS処理
from chardet.universaldetector import UniversalDetector # 文字エンコード自動判定
from collections import OrderedDict # 順序付き辞書(dict)
from docopt import docopt           # コマンド処理時の引数の定義と解釈
import shelve                       # データ永続化


# In[4]:


def convertToWSLStyle(text):
    """
    character escape function
    """
    
    replaceDic = { 
        # Escape character : code list
        r'\^' :r'%5E', 
        r'\~' :r'%7E', 
        r'{'  :r'%7B', 
        r'}'  :r'%7D', 
        r'\[' :r'%5B', 
        r'\]' :r'%5D', 
        r';'  :r'%3B', 
        r'@'  :r'%40', 
        r'='  :r'%3D', 
        r'\&' :r'%26', 
        r'\$' :r'%24', 
        r'#'  :r'%23', 
        r' '  :r'%20', 
        '\\\\':r'/',   
    }

    text = re.sub(r'%', r'%25', text)     # escape "%" character at first
    for (reg, rep) in replaceDic.items(): # escape replaceDic characters
        text = re.sub(reg, rep, text)

    return text
    


# In[5]:


def smblink_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    sphinx role function
    Role to create link addresses.
    """
    text = rawtext
    if '`' in text:
        text = text.split('`')[1]         # drop role name
    if '<' in text and '>' in text:
        name, path = text.split('<')      # split name, path by "<"
        path = path.split('>')[0]
        name = re.sub(r'[ ]+$','', name)  # remove spaces before "<"
    else:
        name = text
        path = name
    href = u"<a href=\"file:" + convertToWSLStyle(path) + u"\">" + name + u"</a>"
    node = nodes.raw('', href, format='html')
    return [node], []


# In[6]:


def isContain(filelist, keywoard):
    """指定のファイル名がリストに存在するかの判定"""
    for filename in filelist:
        if filename == keywoard:
            return True


# In[7]:


def walk_path_to_target_path_list(search_root_path, target_file_name):
    """指定した path を巡回して、target_path_list を作る"""

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
                           'depth': _path.count(os.sep),                    # 階層の深さを
                           'timestamp': os.stat(os.path.join(_path, target_file_name)).st_mtime # TimeStamp
                           }                    
            _target_path_list.append(_target_dict)
            
            #for Debug
            #print("drive: %s , path: %s , full_path: %s , name: %s , depth: %d" % 
            #      (_drive,_path,os.path.join(_path, target_file_name), os.path.basename(_path), _path.count(os.sep)))


    return sorted(_target_path_list,key=lambda my_dict: my_dict['path'])


# In[8]:


def detect_file_encode(file):
    """ファイルの文字エンコード判定"""
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


# In[9]:


def tagfinder(file, tag, path):
    """
    - 以下のディレクティブを書くと、指定パス(tagSearchPath) に対してフォルダとファイル名の走査を行う::

      .. tagfinder::
        :file: tagFileName
        :tag: tagname
        :path: \\file\to
    """
    
    path_list = walk_path_to_target_path_list(path, file)
    
    return path_list


# In[10]:


def match_pattern(pattern, line):
    """渡されたlineからpatternを正規表現検索する。
    ただし、pattern は正規表現エスケープされ、以下の特殊な変換が行われる。
    アスタリスク(*) は 正規表現 .* に
    クエスチョン(?) は 正規表現 . に変換される
    
    返り値は re.match オブジェクト(bool値として扱える)"""

    tmppt = re.escape(pattern) #入力パターンをエスケープ
    tmppt = re.sub(r'\\\*',r'.*',tmppt) # アスタリスク(*) は正規表現の任意文字(.*)に変形
    tmppt = re.sub(r'\\\?',r'.',tmppt)  # クエスチョン(?) は正規表現の任意1文字(.)に変形
    
    pt =  re.compile(tmppt) # 正規表現にコンパイル

    return re.search(pt,line) # 検索結果は re.match オブジェクト


# In[72]:


def converted_match_pattern(pattern):
    """渡されたpatternをcompileされた正規表現として返す
    ただし、pattern は正規表現エスケープされ、以下の特殊な変換が行われる。
    アスタリスク(*) は 正規表現 .* に
    クエスチョン(?) は 正規表現 . に変換される
    
    返り値は re.match オブジェクト(bool値として扱える)"""

    tmppt = re.escape(pattern) #入力パターンをエスケープ
    tmppt = re.sub(r'\\\*',r'.*',tmppt) # アスタリスク(*) は正規表現の任意文字(.*)に変形
    tmppt = re.sub(r'\\\?',r'.',tmppt)  # クエスチョン(?) は正規表現の任意1文字(.)に変形
    
    return re.compile(tmppt) # 正規表現にコンパイル


# In[86]:


FILENAME = 'tag.txt'
TAG = 'this-is-tag-?00'
PATH = './test'


# In[87]:


path_list = tagfinder(FILENAME, TAG, PATH)


# In[88]:


path_list


# In[95]:


for target in path_list:
    """path_listの中身を評価して、リンクを追記していく"""
    
    full_path = os.path.join(target['drive'], target['full_path'])

    try:
        with open(full_path, mode='rt') as f:
            while True:
                lines = f.readlines()
                break
        for count, line in enumerate(lines):
            """:tftag:の探索
            count : 0開始の行数
            line  : 行の中身"""
            
            #print(str(count) + ">" + line)
            taglist = []  # 見つけた :tftag: と関連する :desc: タグを格納する 2次元配列 [ [name,desc], [name,desc], ..]
            
            if match_pattern(':tftag:*',line):
                if re.search(converted_match_pattern(TAG), line):
                    """:tftag:が見つかったら次の:tftag: の前の行、もしくは行末まで取得する"""
                    
                    #print("match :" + line + " , name :" + target['name'])
                    #print("<a href=\"file:" + convertToWSLStyle(full_path) + u"\">" + target['name'] + u"</a>")
                    
                    tmp = []
                    flag = False
                    for sline in lines[count+1:]:
                        
                        #print(" >>" + sline)
                        
                        if match_pattern(':tftag:*',sline.replace('\n',' ')):
                            #print("match next pattern") 
                            break #次の:tftag:が見つかったらおわり
                            
                        if flag: tmp.append(sline.replace('\n',' ')) #すでにdescが見つかって居る場合は、次の:tftag:まで取得を継続
                            
                        if match_pattern(':desc:*', sline.replace('\n',' ')):
                            tmp.append(sline.replace(':desc:','').replace('\n',' '))
                            flag = True
                            
                            
                    print([target['name'],''.join(tmp)]) # [name , desc] の配列。 descは改行をスペースに置き換えてある
                    print("<a href=\"file:" 
                          + convertToWSLStyle(os.path.join(target['drive'], target['path'])) 
                          + "\">" + target['name'] + "</a>" + ''.join(tmp))
                    


    finally:
        f.close()
        print("--- file closed")


