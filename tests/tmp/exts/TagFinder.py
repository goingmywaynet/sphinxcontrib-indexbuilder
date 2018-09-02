
# coding: utf-8

# In[ ]:


# coding: -*- utf-8 -*-


# In[ ]:


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


# In[ ]:


import re                           # 正規表現処理
import string                       # 文字処理


# In[ ]:


import os.path                      # OS処理
from chardet.universaldetector import UniversalDetector # 文字エンコード自動判定
from collections import OrderedDict # 順序付き辞書(dict)
from docopt import docopt           # コマンド処理時の引数の定義と解釈
import shelve                       # データ永続化


# sphinxcontrib化

# In[ ]:


from docutils import nodes          # sphinx拡張処理 docutils node
from docutils.parsers.rst import directives,Directive # sphinx拡張処理 docutils directive
from sphinx.locale import _         # sphinx拡張処理
"""API : http://www.sphinx-doc.org/ja/stable/extdev/index.html#apis-used-for-writing-extensions
document: 
sample: http://www.xavierdupre.fr/blog/2015-06-07_nojs.html"""


# ディレクティブ tagfinder

# In[ ]:


class tagfinder(nodes.Admonition, nodes.Element):
    """ノードクラス tagfinder : docutils.nodes の中で定義されているdocutilsの標準クラスを継承するだけ"""
    pass


# In[ ]:


class TagFinderDirective(Directive):
    """ディレクティブクラス tagfinder : ノードクラスのインスタンスを作って返す
    API : http://code.nabla.net/doc/docutils/api/docutils/parsers/rst/docutils.parsers.rst.Directive.html#docutils.parsers.rst.Directive
    """
    
    # this enables content in the directive
    has_content = True # このディレクティブは自身で直接nodeを返す
    """A boolean; True if content is allowed.  Client
      code must handle the case where content is required but not
      supplied (an empty content list will be supplied)."""
    
    #required_arguments = 0 # 必須オプション数 (オプション名含む) # options_spec を使う場合は不要
    #optional_arguments = 0 # 必須オプション数に加えて追加可能な数 # options_spec を使う場合は不要

    # 渡すオプションを指定する
    option_spec = {'file': directives.unchanged, # :file: tag にファイル名 directives.unchanged は textのまま dicに載せる
                   'tag': directives.unchanged,  # :tag:  tag の名称 directives.unchanged は textのまま dicに載せる
                   'path': directives.unchanged }# :path: 探索するファイルパス directives.unchanged は textのまま dicに載せる
    # API: http://code.nabla.net/doc/docutils/api/docutils/parsers/rst/docutils.parsers.rst.directives.html#module-docutils.parsers.rst.directives 

    def run(self):
        #arg = self.arguments # arguments を取得するけど、option_spec と options を使うので不要
        file = str(self.options['file']).split(',')
        tags = str(self.options['tag']).split(',')
        path = str(self.options['path']).split(',')
        
        if len(file) > 1 or len(path) >1:
            print("\n\t" + "tagfinder Directive ERROR\n" + "fileオプションとpathオプションは1つしか指定できません")
        
        print(file,tags,path)

        for tag in tags:
            print(tag.strip())
        
        env = self.state.document.settings.env

        ref_node = nodes.Text('title')

        return [ref_node]


# オリジナル処理

# In[ ]:


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
    


# In[ ]:


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


# In[ ]:


def isContain(filelist, keywoard):
    """指定のファイル名がリストに存在するかの判定"""
    for filename in filelist:
        if filename == keywoard:
            return True


# In[ ]:


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


# In[ ]:


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


# In[ ]:


def findtags(file, tag, path):
    """
    - 以下のディレクティブを書くと、指定パス(tagSearchPath) に対してフォルダとファイル名の走査を行う::

      .. tagfinder::
        :file: tagFileName
        :tag: tagname
        :path: \\file\to
    """
    
    path_list = walk_path_to_target_path_list(path, file)
    
    return path_list


# In[ ]:


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


# In[ ]:


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


# FILENAME = 'tag.txt'
# TAG = 'this-is-tag-?00'
# PATH = './test'

# path_list = findtags(FILENAME, TAG, PATH)

# path_list

# for target in path_list:
#     """path_listの中身を評価して、リンクを追記していく"""
#     
#     full_path = os.path.join(target['drive'], target['full_path'])
# 
#     try:
#         with open(full_path, mode='rt') as f:
#             while True:
#                 lines = f.readlines()
#                 break
#         for count, line in enumerate(lines):
#             """:tftag:の探索
#             count : 0開始の行数
#             line  : 行の中身"""
#             
#             #print(str(count) + ">" + line)
#             taglist = []  # 見つけた :tftag: と関連する :desc: タグを格納する 2次元配列 [ [name,desc], [name,desc], ..]
#             
#             if match_pattern(':tftag:*',line):
#                 if re.search(converted_match_pattern(TAG), line):
#                     """:tftag:が見つかったら次の:tftag: の前の行、もしくは行末まで取得する"""
#                     
#                     #print("match :" + line + " , name :" + target['name'])
#                     #print("<a href=\"file:" + convertToWSLStyle(full_path) + u"\">" + target['name'] + u"</a>")
#                     
#                     tmp = []
#                     flag = False
#                     for sline in lines[count+1:]:
#                         
#                         #print(" >>" + sline)
#                         
#                         if match_pattern(':tftag:*',sline.replace('\n',' ')):
#                             #print("match next pattern") 
#                             break #次の:tftag:が見つかったらおわり
#                             
#                         if flag: tmp.append(sline.replace('\n',' ')) #すでにdescが見つかって居る場合は、次の:tftag:まで取得を継続
#                             
#                         if match_pattern(':desc:*', sline.replace('\n',' ')):
#                             tmp.append(sline.replace(':desc:','').replace('\n',' '))
#                             flag = True
#                             
#                             
#                     print([target['name'],''.join(tmp)]) # [name , desc] の配列。 descは改行をスペースに置き換えてある
#                     print("<a href=\"file:" 
#                           + convertToWSLStyle(os.path.join(target['drive'], target['path'])) 
#                           + "\">" + target['name'] + "</a>" + ''.join(tmp))
#                     
# 
# 
#     finally:
#         f.close()
#         print("--- file closed")
# 
# 

# In[ ]:


def setup(app):
    """sphinx-contrib 用 setup 関数"""
    #app.add_config_value('todo_include_todos', False, 'html')
    print("RUN TagFinder setup()")

    #app.add_node(tagfinder,
    #            html=(visit_tag_node, depart_tag_node)) #フェーズ3までで終わるため visiter不要
    #app.add_node(todo,
    #             html=(visit_todo_node, depart_todo_node),
    #             latex=(visit_todo_node, depart_todo_node),
    #             text=(visit_todo_node, depart_todo_node))

    app.add_directive('tagfinder', TagFinderDirective)
    #app.add_directive('todolist', TodolistDirective)
    #app.connect('doctree-resolved', process_todo_nodes)
    #app.connect('env-purge-doc', purge_todos)

    return {'version': '0.1'}   # identifies the version of our extension

