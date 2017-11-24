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
    
