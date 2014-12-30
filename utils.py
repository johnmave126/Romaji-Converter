from functools import wraps

import wx

def callLater(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wx.CallAfter(func, *args, **kwargs)
    return wrapper
