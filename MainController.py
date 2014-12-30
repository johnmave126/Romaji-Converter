#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
import PageConstructor

class MainController(wx.App):
    def __init__(self, frame):
        self._frame = frame
        self._page_contructor = PageConstructor.PageConstructor(frame)
        self._page_contructor.generate([(u'邪悪','jaaku','3'),('2','3','4')])
