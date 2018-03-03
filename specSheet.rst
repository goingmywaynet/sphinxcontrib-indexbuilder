===============================================================
AutoBuildSphinxIndexScript2 
===============================================================

動作仕様
============================================================


- SearchPath に対してフォルダとファイル名の走査を行う

  

- KeyFileName があるフォルダパス( KeyFilePath )を抽出

  * KeyFilePath 配列に以下の2種類の情報を付加

    * KeyFilePathまでの階層深さ KeyDepth

    * KeyFilePath のあるカレントフォルダ名 KeyFileFolder

- KeyFilePath から .rst ファイル ( KeyFile )を生成する

  * KeyFileName の文字コードを SJIS -> UTF8

  * KeyFileName のカレントフォルダ名( KeyFileFolder )で KeyFileName のファイル名を置き換え
    
  * 拡張子を .rst にする

  * .rst ファイルの末尾に KeyFilePath へのリンクを追記する

    * :smblink: ディレクティブを利用する

  * buildPath にファイルを配置する

- KeyFilePath の階層の深さに応じてbuildPath の index.rst ファイルを追記する

  * 第1階層( SearchPath 直下のフォルダ名 ) index.rst の タイトルとして扱う

  * 第2階層 index.rst のサブタイトルとして扱う

  * index.rst に階層に応じて KeyFile名を追記する
    
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
