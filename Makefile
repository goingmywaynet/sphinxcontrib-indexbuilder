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
# unittest を走らせる
#
test:; python -m unittest -v
