#
# jupyter notebook 用 Makefile
#
#   $ make  コマンドでipynbをscript化し、unittestを走らせる
#
#   なお、unittestは ./tests/test*.py が対象 (unittest のデフォルト動作)
#
# Memo:
#   vi で:set expandtab（:set et)状態の時に  <TAB> を入力するには insert mode で Ctrl-v の後に <TAB> を入力
#
#

SCRIPT_OUTPUT_DIR   =   ./indexbuilder

#
# jupyter nbconvert で ipynb 全てを script 化し、unittest を走らせる
#
all: script test

#
# jupyter nbconvert で ipynb 全てを script 化
# 
script:
	jupyter nbconvert --output-dir=$(SCRIPT_OUTPUT_DIR) --to script *.ipynb


#
# 配布パッケージを作る Creating tar archive
#
sdist:; python setup.py sdist

#
# unittest を走らせる
#
test:
	python -m unittest -v
	cp ${SCRIPT_OUTPUT_DIR}/*.py ./tests/tmp/exts/

#
# tests フォルダで動作実験
#
test-run:
	python ./indexbuilder/SearchBuildTargets.py -o ./tests/tmp -t keyfile.txt -d 1 -l "hoge" -i ./header.rst ./tests/Folder/Folder1
	ls -tlrs ./tests/tmp

#
# tests フォルダの初期化
#
clean:
	rm ./tests/tmp/*.rst
	rm ./tests/tmp/*.db
