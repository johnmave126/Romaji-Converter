import threading
import pyperclip
import time

class ClipboardWatcher(threading.Thread):
    def __init__(self, callback, pause=.5):
        super(ClipboardWatcher, self).__init__()
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self):       
        recent_value = ""
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                self._callback(recent_value)
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True
