===============================================================
sphinxcontrib-indexbuilder
===============================================================

Description
============================================================

SearchBuildTargets Script
------------------------------------------------------------

- 指定パス(SearchPath) に対してフォルダとファイル名の走査を行う

- 指定ファイル名(TargetFileName) があるフォルダパスを抽出 (target_path_list)

- 指定の階層の深さ(target_path_list) に応じて buildPath の index.rst ファイルを追記する

  * 第1階層( SearchPath 直下のフォルダ名 ) index.rst の タイトルとして扱う

  * 第2階層 index.rst のサブタイトルとして扱う

  * index.rst に階層に応じて KeyFile名を追記する

  * ヘッドライン化する段階は headingdepth として数字で指定可能

- target_path_list から .rst ファイル ( KeyFile )を生成する

  * TargetFileName の文字コードを SJIS -> UTF8

  * TargetFileName のカレントフォルダ名( KeyFileFolder )で TargetFileName のファイル名を置き換え
    
  * 拡張子を ``.rst`` にする

  * .rst ファイルの末尾に target_path_list へのリンクを追記する

    * ``:smblink:`` ディレクティブを利用する

  * 指定フォルダパス(saveto) パスにファイルを配置する


tagfinder
--------------------------------------------------

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


Installation
============

::

    pip install sphinxcontrib-indexbuilder


Configuration
=============

1. Add ``'sphinxcontrib.indexbuilder'`` to the ``extensions`` list in ``conf.py``.

  ::

    extensions += [ 'sphinxcontrib.indexbuilder' ]


Usage
=====

build index.rst and .rst files
-------------------------------------------

Try this command to show usages

.. code-block:: bash

  $ python ./SearchBuildTargets.py --help


build 

To add a link address use something like::

    :smblink:`\\Server\newfolder\to\path`
    :smblink:`folder <\\Server\newfolder\to\path>`

convert to ``file://Server/newfolder/to/path`` style


require
===================================

import os.path                      # OS処理
from chardet.universaldetector import UniversalDetector # 文字エンコード自動判定
from collections import OrderedDict # 順序付き辞書(dict)
from docopt import docopt           # コマンド処理時の引数の定義と解釈

pandoc http://pandoc.org            # 様式変換


pyInstaller めも
===================================

Macでのビルドについて
------------------------------------------------------------

ビルド環境:

  pyenv 3.6.3/envs/sphinx

pyenv 環境でビルドに失敗するときは、一度 pyenv 環境を PYTHON_CONFIGURE_OPTS="--enable-shared" 環境変数を設定した上で
再度

.. code-block:: bash

  $ pyenv install -f pyenvパッケージ名 

して再インストールすることで対応できる。

https://github.com/pyenv/pyenv/wiki/Home/_compare/45570ea%5E...45570ea

Windowsでのビルドについて
------------------------------------------------------------

ビルド環境：

  WinPython-64bit-3.6.2.0Qt5

以下のエラーが発生するので

|  Fatal Python error: Py_Initialize: unable to load the system file codec
|  LookupError: unknown encoding: utf-8

https://qiita.com/aphextrax/items/c5df13042ec4626127ee を参考に WinPython Command Prompt にて

.. code-block:: cmd

 > pip uninstall enum34

してから、

.. code-block:: cmd

  > C:\Users\joey\Desktop\WinPython-64bit-3.6.2.0Qt5\WORK>pyinstaller SearchBuildTargets.py --onefile

でビルドする。
