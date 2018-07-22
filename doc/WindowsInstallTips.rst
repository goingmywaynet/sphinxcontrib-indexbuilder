============================================================
Knowledge Base 2.0
============================================================

Install
============================================================

- 37文字以内のWindowsディレクトリパスに WinPython 用ディレクトリを作成。
  
  - D:\winpython にフォルダを作成

- windows のプログラムと機能の一覧に Microsoft Visual C++ 2017 Redistribute を追加する。
  
  - すでに存在する場合はこの手順をスキップしてよい。

  #. dist\windows 内の ``VC_redist.x64.exe`` を上記フォルダへcopy

  #. copyした ``VC_redist.x64.exe`` をダブルクリック

    - Microsoft Visual C++ 2017 Redistribute インストールダイアログが開始

    - ライセンス条項および使用条件に同意にチェック

    - ``インストール`` ボタンクリック

    - admin権限承認

    - ``閉じる`` で完了

  .. note::
    不要かもしれない。要確認

- WinPython をインストールする。

- dist\windows 内の ``WinPython64-3.6.5.0Qt5.exe`` をダブルクリック

  - WinPython 64 バージョン名 Setup ダイアログ起動

  - ``I Agree`` をクリック

  - Destination Folder にインストール先を指定する。 ここでは先ほど指定したフォルダ名 D:\winpython を指定する。

  - ``Install`` をクリック

  - インストール進捗が表示されるので、完了するまで待つ。

  - ``Next`` をクリック

  - ``Finish`` をクリック

  .. note::
    winpython はファイルの展開をするだけなので、レジストリは汚さない。

- Janome と sphinx-contrib をインストールする

  - ``C:\winpython\winpython control panel`` をダブルクリック

  - ``dist\Janome-0.3.6.tar.gz`` をコントロールパネルの ``Install/Upgrade packages`` ペインにドラッグアンドドロップ

  - ``dist\sphinxcontrib-smblink-0.2.tar.gz`` をコントロールパネルの ``Install/Upgrade packages`` ペインにドラッグアンドドロップ

  - ``Install Packages`` ボタンをクリックし、インストール完了を待つ

  - ``Uninstall Packages`` に 上記パッケージが入っていることを確認

  - ``X`` でウィンドウを閉じる

- sphinx フォルダの作成
  
  - ``WinPython Command Prompt`` を起動し、ビルド用フォルダに移動 
  
    ビルド用フォルダ D:\KB\mybuild

  - ビルド用フォルダにて sphinx-quickstart を実行し、sphinxの文書ビルド環境を構築する。

    各設定は基本的に任意でOK だが、 Languageだけは ja にしておく

- 検索処理にjanomeを使用する設定を追加

  - ビルド用フォルダにある conf.py を開き、末尾に以下の情報を追記して保存する。

  .. code-block:: python

    html_search_options = {
      'type': 'janome'
    }

windows 内でバッチファイルを作る方法
============================================================

winpython をインストールしたフォルダから script\python.bat hoge.py と実行する


