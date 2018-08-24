"""SearchBuildTargetsテスト"""
import unittest as ut
import os
from indexbuilder import SearchBuildTargets

def Lpath(path):
  """Localized Path : Windows と linux のセパレータ差異対応
  Windows のセパレータ'\\'への対応として、セパレータが '/' ではない場合は、 '/' を os.sep (OSのデフォルトセパレータ) に置き換える"""
  if os.sep != '/':
    return path.replace('/', os.sep)
  else:
    return path

class SearchBuildTargetsTest(ut.TestCase):
  """SearchBuildTargets テスト"""

  def test_convert_smblink(self):
    """smblinkのpath変換"""

    tasklist = [
      {'lines': [ "" ,":smblink:`linkedfile.txt`" ,""], #試験ファイルを見つける
      'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
      'ans': [ "" ,":smblink:`./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/linkedfile.txt`" ,""]}\

      ,{'lines': [ "" ,":smblink:`./notfound.txt`" ,""], #存在しないファイルは無視する
      'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
      'ans': [ "" ,":smblink:`./notfound.txt`" ,""]}\

      ,{'lines': [ "" ,":smblink:`./linkedfile.txt`" ,""], # ./が入る書き方も対応する
      'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
      'ans': [ "" ,":smblink:`./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/./linkedfile.txt`" ,""]}\

      ,{'lines': [ "hogehoge" ,"fugafuga :smblink:`linkedfile.txt` nyaronya" ,""], #他のことが書いてある場合も可能
      'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
      'ans': [ "hogehoge" ,"fugafuga :smblink:`./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/linkedfile.txt` nyaronya" ,""]}\

      ,{'lines': [ "hogehoge" ,"fugafuga :smblink:`linkedfile.txt <linkedfile.txt>` nyaronya" ,""], # :smblink:`text <file>`の書き方
      'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
      'ans': [ "hogehoge" ,"fugafuga :smblink:`linkedfile.txt <./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/linkedfile.txt>` nyaronya" ,""]}\

      ,{'lines': [ "hogehoge" ,".. image:: test.jpg" ,""], #image
      'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
      'ans': [ "hogehoge" ,".. image:: ./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/test.jpg" ,""]}\

      ,{'lines': [ "hogehoge" ,"this is .. image:: test.jpg" ,""], #行内image
      'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
      'ans': [ "hogehoge" ,"this is .. image:: ./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/test.jpg" ,""]}\

      ,{'lines': [ "hogehoge" ,".. figure:: test.jpg" ,""], #figure
      'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
      'ans': [ "hogehoge" ,".. figure:: ./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/test.jpg" ,""]}\

      ,{'lines': [ "hogehoge" ,"this is .. figure:: test.jpg" ,""], #行内figure
      'drive_path': "./tests/Folder/Folder1/FolderD/FolderD1/FolderD11",
      'ans': [ "hogehoge" ,"this is .. figure:: ./tests/Folder/Folder1/FolderD/FolderD1/FolderD11/test.jpg" ,""]}\
      ]

    for task in tasklist:

      _ans = [ Lpath(i) for i in task['ans'] ]
      _drive_path = Lpath(task['drive_path'])
      _lines = [ Lpath(i) for i in task['lines'] ]
      
      self.assertEqual(_ans, SearchBuildTargets.convert_smblink(_lines,_drive_path))


