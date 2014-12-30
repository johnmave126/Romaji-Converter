import wx
from wx import html
from utils import callLater

class MyPopupMenu(wx.Menu):
    
    def __init__(self, parent):
        super(MyPopupMenu, self).__init__()
        
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnMinimize, mmi)

        cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        self.AppendItem(cmi)
        self.Bind(wx.EVT_MENU, self.OnClose, cmi)


    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

class MyHTMLDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(MyHTMLDialog, self).__init__(*args, style=0, **kwargs)
        self._html_container = html.HtmlWindow(self)
        self.Hide()

    def showPage(self, html):
        self._html_container.SetPage(html)


class GalgameRomaji(wx.Frame):
    VERTICAL_HEIGHT = 200

    def __init__(self, parent, id, title):
        super(GalgameRomaji, self).__init__(parent, -1, title, style=wx.STAY_ON_TOP)

        screen_width, _ = wx.DisplaySize()

        self.SetBackgroundColour(wx.Colour(128, 128, 128))
        self.SetSize((screen_width - 20, GalgameRomaji.VERTICAL_HEIGHT))
        self.MoveXY(0, 20)
        self.Center(wx.HORIZONTAL)
        self.Show(True)

        self._hbox = wx.WrapSizer(wx.HORIZONTAL)
        self.SetSizer(self._hbox)

        self._dialog = MyHTMLDialog(self)

        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnRightDown(self, e):
        self.PopupMenu(MyPopupMenu(self), e.GetPosition())

    def OnLeftUp(self, e):
        self.hideHTML()

    @callLater
    def showHTML(self, widget, html):
        self._dialog.showPage(html)

        x, y = widget.GetScreenPosition()
        _, h = widget.GetSize()
        self._dialog.MoveXY(x, y + h)
        self._dialog.Show()

    def hideHTML(self):
        self._dialog.Hide()

    def OnClose(self, e):
        self.Destroy()
