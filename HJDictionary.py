import socket
import urllib

from bs4 import BeautifulSoup

import Dictionary
import ThreadPool

class HJDictionary(Dictionary.Dictionary):
    HJ_URL = 'http://dict.hjenglish.com/jp/jc/'

    def __init__(self, *args, **kwargs):
        super(HJDictionary, self).__init__(*args, **kwargs)

        socket.setdefaulttimeout(5)
        self.thread_pool = ThreadPool.ThreadPool(5)


    def lookup(self, words):
        i = 0
        for word in words:
            self.thread_pool.add_job(self.lookupOne, word, i)
            i += 1

        res = self.thread_pool.wait_for_complete()
        res.sort()
        return map(lambda x: x[2], res)

    @staticmethod
    def lookupOne(word, i):
        if not isinstance(word, unicode):
            return (i, word, '')
        try:
            word_encoded = urllib.quote(word.encode('utf8'), safe='~()*!.\'')
            soup = BeautifulSoup(urllib.urlopen(HJDictionary.HJ_URL + word_encoded))

            elem = soup.find(id='comment_0')
            if elem is None:
                return (i, word, '')
            return (i, word, elem.prettify())
        except Exception, e:
            print e
            return (i, word, '')
