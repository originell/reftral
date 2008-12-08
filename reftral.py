# coding: utf8
import urllib
import urllib2

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    print 'This library requires BeautifulSoup to work\nGet it at ' \
          'http://www.crummy.com/software/BeautifulSoup/'

URL = 'http://dictionary1.classic.reference.com/translate/index.html'

class Translator:
    def get_langs(self):
        """
        returns a dict containing all available languages
        """

        html = urllib2.urlopen(URL)
        opts = BeautifulSoup(html).find('div', {'class': 'tap_selOptions'})
        langs = {}

        # we don't want "Translate from..." -> [2:]
        for x in opts.select.contents[2:]:
            if x != '\n':
                langs[x['value']] = x.contents[0]

        return langs

    def translate(self, lang, text):
        """
        returns a string containing the translated text
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

        return tral

