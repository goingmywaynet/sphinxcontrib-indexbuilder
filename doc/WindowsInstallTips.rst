============================================================
Knowledge Base 2.0
============================================================

Install
============================================================

- 37文字以内のWindowsディレクトリパスに WinPython 用ディレクトリを作成。
  
  - ``D:\winpython`` にフォルダを作成

- windows のプログラムと機能の一覧に Microsoft Visual C++ 2017 Redistribute を追加する。
  
  - すでに存在する場合はこの手順をスキップしてよい。

  #. dist\windows 内の ``VC_redist.x64.exe`` を上記 ``D:\winpython`` フォルダへcopy

  #. copyした ``VC_redist.x64.exe`` をダブルクリック

    - Microsoft Visual C++ 2017 Redistribute インストールダイアログが開始

    - ライセンス条項および使用条件に同意にチェック

    - ``インストール`` ボタンクリック

    - admin権限承認

    - ``閉じる`` で完了

  .. note::
    不要かもしれない。要確認

- WinPython をインストールする。

- ``dist\windows`` 内の ``WinPython64-3.6.5.0Qt5.exe`` をダブルクリック

  #. WinPython 64 バージョン名 Setup ダイアログ起動

  #. ``I Agree`` をクリック

  #. Destination Folder にインストール先を指定する。 ここでは先ほど指定したフォルダ名 D:\winpython を指定する。

  #. ``Install`` をクリック

  #. インストール進捗が表示されるので、完了するまで待つ。

  #. ``Next`` をクリック

  #. ``Finish`` をクリック

  .. note::
    winpython はファイルの展開をするだけなので、レジストリは汚さない。

- Janome と sphinxcontrib をインストールする

  #. ``C:\winpython\winpython control panel`` をダブルクリック

  #. ``dist\Janome-0.3.6.tar.gz`` をコントロールパネルの ``Install/Upgrade packages`` ペインにドラッグアンドドロップ

  #. ``dist\sphinxcontrib-smblink-0.2.tar.gz`` をコントロールパネルの ``Install/Upgrade packages`` ペインにドラッグアンドドロップ

  #. ``Install Packages`` ボタンをクリックし、インストール完了を待つ

  #. ``Uninstall Packages`` に 上記パッケージが入っていることを確認

  #. ``X`` でウィンドウを閉じる

- sphinx フォルダの作成
  
  #. ``WinPython Command Prompt`` を起動し、ビルド用フォルダに移動 
  
    ビルド用フォルダ D:\KB\mybuild

  #. ビルド用フォルダにて sphinx-quickstart を実行し、sphinxの文書ビルド環境を構築する。

    - `C:\winpython\WinPython Command Prompt` を起動 

    .. cocd-block:: cmd

      C:\winpython\scripts>D:

      D:\>cd D:\KB\mybuild

      D:\KB\mybuild>sphinx-quickstart

      Welcome to the Sphinx 1.7.2 quickstart utility.

      Please enter values for the following settings (just press Enter to
      accept a default value, if one is given in brackets).

      Selected root path: .

      You have two options for placing the build directory for Sphinx output.
      Either, you use a directory "_build" within the root path, or you separate
      "source" and "build" directories within the root path.
      > Separate source and build directories (y/n) [n]:

      Inside the root directory, two more directories will be created; "_templates"
      for custom HTML templates and "_static" for custom stylesheets and other static
      files. You can enter another prefix (such as ".") to replace the underscore.
      > Name prefix for templates and static dir [_]:

      The project name will occur in several places in the built documentation.
      > Project name: myproject
      > Author name(s): myproject
      > Project release []: 0.1

      If the documents are to be written in a language other than English,
      you can select a language here by its language code. Sphinx will then
      translate text that it generates into that language.

      For a list of supported codes, see
      http://sphinx-doc.org/config.html#confval-language.
      > Project language [en]: ja

      The file name suffix for source files. Commonly, this is either ".txt"
      or ".rst".  Only files with this suffix are considered documents.
      > Source file suffix [.rst]:

      One document is special in that it is considered the top node of the
      "contents tree", that is, it is the root of the hierarchical structure
      of the documents. Normally, this is "index", but if your "index"
      document is a custom template, you can also set this to another filename.
      > Name of your master document (without suffix) [index]:

      Sphinx can also add configuration for epub output:
      > Do you want to use the epub builder (y/n) [n]:
      Indicate which of the following Sphinx extensions should be enabled:
      > autodoc: automatically insert docstrings from modules (y/n) [n]:
      > doctest: automatically test code snippets in doctest blocks (y/n) [n]:
      > intersphinx: link between Sphinx documentation of different projects (y/n) [n]
      :
      > todo: write "todo" entries that can be shown or hidden on build (y/n) [n]:
      > coverage: checks for documentation coverage (y/n) [n]:
      > imgmath: include math, rendered as PNG or SVG images (y/n) [n]:
      > mathjax: include math, rendered in the browser by MathJax (y/n) [n]:
      > ifconfig: conditional inclusion of content based on config values (y/n) [n]:
      > viewcode: include links to the source code of documented Python objects (y/n)
      [n]:
      > githubpages: create .nojekyll file to publish the document on GitHub pages (y/
      n) [n]:

      A Makefile and a Windows command file can be generated for you so that you
      only have to run e.g. `make html' instead of invoking sphinx-build
      directly.
      > Create Makefile? (y/n) [y]:
      > Create Windows command file? (y/n) [y]:

      Creating file .\conf.py.
      Creating file .\index.rst.
      Creating file .\Makefile.
      Creating file .\make.bat.

      Finished: An initial directory structure has been created.

      You should now populate your master file .\index.rst and create other documentat
      ion
      source files. Use the Makefile to build the docs, like so:
         make builder
      where "builder" is one of the supported builders, e.g. html, latex or linkcheck.

      D:\KB\mybuild>


    - 各設定は基本的に任意でOK だが、 Languageだけは ja にしておく

- 検索処理にjanome, リンク処理にsmblinkを使用する設定を追加

  #. ビルド用フォルダにある conf.py を開き、末尾に以下の情報を追記して保存する。

  .. code-block:: python

    extensions += [ 'sphinxcontrib.smblink' ]

    html_search_options = {
      'type': 'janome'
    }

    source_parsers = {'.md': 'recommonmark.parser.CommonMarkParser'}

  #. 動作確認で `C:\winpython\WinPython Command Prompt` で以下の通りビルドを実行してみる

  .. code-block:: cmd

    D:\KB\mybuild>make html
    Running Sphinx v1.7.2
    loading translations [ja]... done
    making output directory...
    loading pickled environment... not yet created
    building [mo]: targets for 0 po files that are out of date
    building [html]: targets for 1 source files that are out of date
    updating environment: 1 added, 0 changed, 0 removed
    reading sources... [100%] index
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    writing output... [100%] index
    generating indices... genindex
    writing additional pages... search
    copying static files... done
    copying extra files... done
    dumping search index in Japanese (code: ja) ... done
    dumping object inventory... done
    build succeeded.

    The HTML pages are in _build\html.

  上の様にエラーがなくビルドができていれば成功



