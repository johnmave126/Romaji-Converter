Romaji Converter
===
This is a prototype for something like '喵翻'. Basically, it captures the clipboard and feeds it to MeCab and Kakasi to get a splitted version(in word unit) of Japanese sentence, with Hiragana, Katana, and Kanji converted to Romaji. Meanwhile, it looks up a dictionary(currently 沪江日语) for each word. At last, it display an ugly UI of original sentence, its Romaji version, and definition of each word.
This version is very very prototyping and with lots of bugs.

HOWTO
---------
Run the main.py

Dependencies
---------
Apart from requirements.txt, there is also some other dependencies
Python 2.7.x: https://www.python.org/
MeCab: http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html
wxPython: http://www.wxpython.org/

There is no 64-bit version for mecab-python, I have compiled one, but **with caution**, it is **not** compiled with VS2008 as stated required [here](http://stackoverflow.com/questions/3047542/building-lxml-for-python-2-7-on-windows/5122521#5122521). Instead, for my convenience, it is compiled with VS2013.

Also, you should not use pip to install pykakasi, you need to clone its [HEAD](https://github.com/miurahr/pykakasi), and run `python setup.py genkanwa`, and then `python setup.py install` to install it.

These dependencies are annoying, that's why this project is just a prototype.

Known Issues
---------
* Mecab doesn't give a very accurate split of sentence(or too accurate), which leads trouble to 促音 and 拗音. It sometimes cuts at suffix and sometimes not. Maybe what I need is not a Morphological Analyzer(its term), maybe a simpler thing.
* wxPython is definitely not a good GUI toolkit, I cannot achieve transparent background. It crashes when you quickly click on this word and another word.
* Network dictionary look up is too slow, I cannot bear it when playing galgame.

TODO
---------
* Use another language and better GUI toolkit to rebuild the project. MSVC/MFC maybe.
* Use better analyzer to analyze sentence. I am considering use Kakasi directly and do a reverse spliting.
* Use a local dictionary instead of a network one.
* Build a UI to integrate ITH and open galgame from that UI just like '喵翻'
* If possible, I want to just make this an extension of '喵翻' instead of a standalone application