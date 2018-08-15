"""TagFinderテスト"""
import unittest as ut
from indexbuilder import TagFinder

class TagFinderTest(ut.TestCase):
  """TagFinder テスト"""

  def test_convertToWSLStyle(self):
    """SMB形式への文字列変換"""

    # [変換後,変換前] の組み合わせを宣言
    convert_list = [
      ['filepath','filepath']
      ,['/file/path','\\file\path']
      ,['/file/path%20withspace','\\file\path withspace']
    ]

    for pair in convert_list:

      self.assertEqual(pair[0], TagFinder.convertToWSLStyle(pair[1]), pair[1])

