"""SearchBuildTargetsテスト"""
import unittest as ut
import os
from indexbuilder import SearchBuildTargets
from pathlib import Path

def Lpath(path):
    """Localized Path : Windows と linux のセパレータ差異対応
    Windows のセパレータ'\\'への対応として、セパレータが '/' ではない場合は、 '/' を os.sep (OSのデフォルトセパレータ) に置き換える"""
    if os.sep != '/':
        return path.replace('/', os.sep)
    else:
        return path

class SearchBuildTargetsTest(ut.TestCase):
    """SearchBuildTargets テスト"""

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

        for task in tasklist:

            _ans = task['ans']
            _relative = task['relative']
            _anchor = task['anchor']

            self.assertEqual(_ans, str(SearchBuildTargets.get_absolue_path(_relative,_anchor)))

    def test_get_absolue_path_windows(self):
        """pathlib 処理 windows localhost の network name に対するチェック"""

        if os.sep != '/':

            print("Windows 環境試験")

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

            for task in tasklist:

                _ans = task['ans']
                _relative = task['relative']
                _anchor = task['anchor']

                self.assertEqual(_ans, str(SearchBuildTargets.get_absolue_path(_relative,_anchor)))






