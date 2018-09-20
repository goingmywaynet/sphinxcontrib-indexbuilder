"""SearchBuildTargetsテスト"""
import unittest as ut
import os
from indexbuilder import SearchBuildTargets
from pathlib import Path

class SearchBuildTargetsTest(ut.TestCase):
    """SearchBuildTargets テスト"""

    def test_convert_smblink(self):
        """smblinkのpath変換"""

        currentP = Path('.')

        tasklist = [
            {'lines': [ "" ,":smblink:`linkedfile.txt`" ,""], #試験ファイルを見つける
            'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
            'ans': [ "" ,":smblink:`" + \
                    str(currentP.joinpath("./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/linkedfile.txt").absolute()) +\
                    "`",""]}\

            ,{'lines': [ "" ,":smblink:`./notfound.notfound`" ,""], #存在しないファイルは無視
            'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
            'ans': [ "" ,":smblink:`" + \
                    "./notfound.notfound"
                    "`",""]}\

            ,{'lines': [ "" ,":smblink:`./linkedfile.txt`" ,""], #./の記述もok
            'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
            'ans': [ "" ,":smblink:`" + \
                    str(currentP.joinpath("./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/linkedfile.txt").absolute()) +\
                    "`",""]}\

            ,{'lines': [ "hogehoge" ,":smblink:`./linkedfile.txt`" ,"fugafuga"], #他のことが書いてあってもok
            'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
            'ans': [ "hogehoge" ,":smblink:`" + \
                    str(currentP.joinpath("./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/linkedfile.txt").absolute()) +\
                    "`","fugafuga"]}\

            ,{'lines': [ "hogehoge" ,":smblink:`this is link <./linkedfile.txt>`" ,"fugafuga"], # `name <path>` 記法への対応
            'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
            'ans': [ "hogehoge" ,":smblink:`" + \
                    "this is link <" +\
                    str(currentP.joinpath("./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/linkedfile.txt").absolute()) +\
                    ">"+\
                    "`","fugafuga"]}\

            ,{'lines': [ "hogehoge" ,".. image:: test.jpg" ,"fugafuga"], #.. image:: ディレクティブ
            'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
            'ans': [ "hogehoge" ,".. image:: " + \
                    os.sep +\
                    str(currentP.joinpath("./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/test.jpg").absolute()) \
                    ,"fugafuga"]}\

            ,{'lines': [ "hogehoge" ,"this is .. image:: test.jpg" ,"fugafuga"], # 行内 .. image:: ディレクティブ
            'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
            'ans': [ "hogehoge" ,"this is .. image:: " + \
                    os.sep +\
                    str(currentP.joinpath("./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/test.jpg").absolute()) \
                    ,"fugafuga"]}\

            ,{'lines': [ "hogehoge" ,".. figure:: test.jpg" ,"    :size: 100%"], #.. figure:: ディレクティブ
            'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
            'ans': [ "hogehoge" ,".. figure:: " + \
                    os.sep +\
                    str(currentP.joinpath("./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/test.jpg").absolute()) \
                    ,"    :size: 100%"]}\

                    ]

        if os.sep == '/':
            for task in tasklist:

                _ans = [ i for i in task['ans'] ]
                _drive_path = task['drive_path']
                _lines = [ i for i in task['lines'] ]

                self.assertEqual(_ans, SearchBuildTargets.convert_smblink(_lines,_drive_path))

        else: print("windows では失敗するので試験省略")


    def test_get_absolue_path(self):
        """pathlib 処理"""

        currentP = Path('.')

        tasklist = [
          {'relative': 'README.rst' #試験ファイルを見つける (str ,str)
          ,'anchor': str(currentP.absolute())
          ,'ans': str( (currentP / Path('README.rst')).absolute() )}

          ,{'relative': 'README.rst' #試験ファイルを見つける (str , Path)
          ,'anchor': currentP
          ,'ans': str( (currentP / Path('README.rst')).absolute() )}

          ,{'relative': Path('README.rst') #試験ファイルを見つける (Path , Path)
          ,'anchor': currentP
          ,'ans': str( (currentP / Path('README.rst')).absolute() )}

          ,{'relative': Path('README.rst') #試験ファイルを見つける (Path , str)
          ,'anchor': str(currentP.absolute())
          ,'ans': str( (currentP / Path('README.rst')).absolute() )}

          ,{'relative': 'NOTFOUND' #試験ファイルがない (str , str)
          ,'anchor': str(currentP.absolute())
          ,'ans': 'NOTFOUND'}

          ,{'relative': './tests/tmp' #階層移動(下方向)
          ,'anchor': str(currentP.absolute())
          ,'ans': str( (currentP / Path('./tests/tmp')).absolute() )}
         ]

        if os.sep == '/':

            for task in tasklist:

                _ans = task['ans']
                _relative = task['relative']
                _anchor = task['anchor']

                self.assertEqual(_ans, str(SearchBuildTargets.get_absolue_path(_relative,_anchor)))

        else: print("windows では失敗するので試験省略")

    def test_get_absolue_path_windows(self):
        """pathlib 処理 windows localhost の network name に対するチェック"""

        currentP = r'\\localhost\Public'

        tasklist = [
          {'relative': 'Downloads' #試験ファイルを見つける (str ,str)
          ,'anchor': currentP
          ,'ans': str( (Path(currentP) / Path('Downloads')).absolute() )}

          ,{'relative': 'Pictures\Sample Pictures\Koala.jpg' #試験ファイルを見つける (str ,str)
          ,'anchor': currentP
          ,'ans': str( (Path(currentP) / Path('Pictures/Sample Pictures/Koala.jpg')).absolute() )}

          ,{'relative': r'\\localhost\Public\Pictures\Sample Pictures\Koala.jpg' #試験ファイルを見つける (RawStr ,str)
          ,'anchor': ''
          ,'ans': str( (Path(currentP) / Path('Pictures/Sample Pictures/Koala.jpg')).absolute() )}

          ,{'relative': '\\localhost\Public\Pictures\Sample Pictures\Koala.jpg' #試験ファイルを見つける (str ,str)
          ,'anchor': ''
          ,'ans': str( (Path(currentP) / Path('Pictures/Sample Pictures/Koala.jpg')).absolute() )}

          ,{'relative': 'Sample Pictures\Koala.jpg' #試験ファイルを見つける (str ,str)
          ,'anchor': '\\localhost\Public\Pictures'
          ,'ans': str( (Path(currentP) / Path('Pictures/Sample Pictures/Koala.jpg')).absolute() )}

          ,{'relative': 'Sample Pictures\Koala.jpg' #試験ファイルを見つける (str ,str)
          ,'anchor': r'\\localhost\Public\Pictures\\'
          ,'ans': str( (Path(currentP) / Path('Pictures/Sample Pictures/Koala.jpg')).absolute() )}
        ]

        if os.sep != '/':

            for task in tasklist:

                _ans = task['ans']
                _relative = task['relative']
                _anchor = task['anchor']

                self.assertEqual(_ans, str(SearchBuildTargets.get_absolue_path(_relative,_anchor)))

        else: print("Windows 専用試験なので省略")





