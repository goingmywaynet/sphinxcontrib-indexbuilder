===============================================================
AutoBuildSphinxIndexScript2 
===============================================================

動作仕様
============================================================


- SearchPath に対してフォルダとファイル名の走査を行う

- TargetFileName があるフォルダパスを抽出 (target_path_list)

- target_path_list から .rst ファイル ( KeyFile )を生成する

  * TargetFileName の文字コードを SJIS -> UTF8

  * TargetFileName のカレントフォルダ名( KeyFileFolder )で TargetFileName のファイル名を置き換え
    
  * 拡張子を ``.rst`` にする

  * .rst ファイルの末尾に target_path_list へのリンクを追記する

    * ``:smblink:`` ディレクティブを利用する

  * saveto パスにファイルを配置する

- target_path_list の階層の深さに応じて buildPath の index.rst ファイルを追記する

  * 第1階層( SearchPath 直下のフォルダ名 ) index.rst の タイトルとして扱う

  * 第2階層 index.rst のサブタイトルとして扱う

  * index.rst に階層に応じて KeyFile名を追記する

  * ヘッドライン化する段階は headingdepth として数字で指定可能

ToDo
===================================

- reST 形式と MarkDown 形式に対応する

  * TargetFileName は自動的に rst に変換する。（後方互換性）

  * ``.md`` ファイル名は MarkDown 扱いとする。

- saveto パスへの保存方式に2方式を用意する。

  * ディレクトリを全て排除する方式（後方互換）

  * ディレクトリを維持して構成する方式

- 独自に index タグを収集して特設ページに一覧化する

- 手動での更新コマンドを準備する

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
