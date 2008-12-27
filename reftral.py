# coding: utf8
import urllib
import urllib2

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    print 'This library requires BeautifulSoup to work\nGet it at ' \
          'http://www.crummy.com/software/BeautifulSoup/'

URL = 'http://dictionary1.classic.reference.com/translate/index.html'
JS_FN_PART = 'dictionary_c'

class Translator:
    def __init__(self):
        html = urllib2.urlopen(URL)
        self.soup = BeautifulSoup(html)

    def get_langs(self):
        """
        returns a dict containing all available languages
        """
        soup = self.soup
        opts = soup.find('div', {'class': 'tap_selOptions'})
        langs = {}

        # we don't want "Translate from..." -> [2:]
        for x in opts.select.contents[2:]:
            if x != '\n':
                langs[x['value']] = x.contents[0]

        return langs

    def translate(self, lang, text):
        """
        returns a list containing the translated text
        """

        data_raw = {'lp': lang, 'text': text}
        data = urllib.urlencode(data_raw)
        req = urllib2.Request(URL, data)
        resp = urllib2.urlopen(req)

        soup = BeautifulSoup(resp).find('div', {'class': 'transbox'})
        raw = soup.findAll('td', {'align': 'left', 'valign': 'top'})
        tral = []
        for x in raw[1].p.contents:
            # hacky: need to do this via isinstance somehow
            if not str(type(x)) == "<type 'instance'>":
                tral.append(x)

        # Can't decide between list and string *g*
        # return ' '.join(tral)
        return tral

