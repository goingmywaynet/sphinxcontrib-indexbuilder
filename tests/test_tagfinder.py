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

  def test_walk_path_to_target_path_list(self):
    """パス探索処理"""

    """  以下のタグがみつかる

    [./Folder/Folder1/FolderB/tag.txt]
    FolderB
    :tftag: this-is-tag-100
    :desc: This is Folder1/FolderB tag

    [./Folder/Folder1/FolderB/FolderB1/tag.txt]
    FolderB1
    :tftag: this-is-tag-101,this-is-tag-201
    :desc: this is Folder1/FolderB/FolderB1 tag

    [./Folder/Folder1/FolderA/FolderA1/tag.txt]
    FolderA1 - Multi tag test
    :tftag: this-is-tag-100
    :desc: THIS IS ./Folder/Folder1/FolderA/FolderA1/tag.txt 1st tag DESCRIPTION

    :tftag: this-is-tag-200
    :desc: THIS IS ./Folder/Folder1/FolderA/FolderA1/tag.txt 2nd tag DESCRIPTION

    [./Folder/Folder1/FolderA/FolderA2/tag.txt]
    FolderA2 - Multi tag and Multi line desc test
    :tftag: this-is-tag-100
    :desc: THIS IS Multi Line DESCRIPTION line 1
    THIS IS Multi Line DESCRIPTION line 2

    :tftag: this-is-tag-202
    :desc: THIS IS DESCRIPTION FOR 2nd
      DESCRIPTION FUGAFUGA
    """

    path_list = TagFinder.walk_path_to_target_path_list('./tests/Folder', 'tag.txt')
    self.assertEqual(4, len(path_list), 'number of tag file')
    self.assertEqual('FolderA1', path_list[0]['name'], 'path name is FolderA1')


  def test_walk_path_list(self):
    """タグ探索処理"""
    
    path_list = TagFinder.walk_path_to_target_path_list('./tests/Folder', 'tag.txt')

    tag = 'this-is-tag-100'
    tag_list = TagFinder.walk_path_list(path_list, tag)
    A1tag = [tag for tag in tag_list if tag['name'] == 'FolderA1'] 
    A2tag = [tag for tag in tag_list if tag['name'] == 'FolderA2'] 
    self.assertEqual(3, len(tag_list), ' count tag : ' + tag )
    self.assertEqual('FolderA1', A1tag[0]['name'], ' find tag FolderA1')
    self.assertEqual('FolderA2', A2tag[0]['name'], ' find tag FolderA2')

    tag = 'this-is-tag-101'
    tag_list = TagFinder.walk_path_list(path_list, tag)
    Btag = [tag for tag in tag_list if tag['name'] == 'FolderB'] 
    B1tag = [tag for tag in tag_list if tag['name'] == 'FolderB1'] 
    self.assertEqual(1, len(tag_list), ' count tag : ' + tag )
    self.assertEqual('FolderB1', B1tag[0]['name'], ' find tag FolderB1')

    tag = 'this-is-tag-?00'
    tag_list = TagFinder.walk_path_list(path_list, tag)
    A1tag = [tag for tag in tag_list if tag['name'] == 'FolderA1'] 
    A2tag = [tag for tag in tag_list if tag['name'] == 'FolderA2'] 
    Btag = [tag for tag in tag_list if tag['name'] == 'FolderB'] 
    B1tag = [tag for tag in tag_list if tag['name'] == 'FolderB1'] 
    self.assertEqual(4, len(tag_list), ' count tag : ' + tag )
    self.assertEqual(' THIS IS Multi Line DESCRIPTION line 1 THIS IS Multi Line DESCRIPTION line 2  ', A2tag[0]['desc'], ' find tag FolderA2')

    tag = 'this-is-tag-2*'
    tag_list = TagFinder.walk_path_list(path_list, tag)
    A1tag = [tag for tag in tag_list if tag['name'] == 'FolderA1'] 
    A2tag = [tag for tag in tag_list if tag['name'] == 'FolderA2'] 
    Btag = [tag for tag in tag_list if tag['name'] == 'FolderB'] 
    B1tag = [tag for tag in tag_list if tag['name'] == 'FolderB1'] 
    self.assertEqual(3, len(tag_list), ' count tag : ' + tag )
    self.assertEqual(' THIS IS ./Folder/Folder1/FolderA/FolderA1/tag.txt 2nd tag DESCRIPTION ', A1tag[0]['desc'], ' find tag FolderA1')

