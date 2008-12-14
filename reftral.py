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

    def get_lang_opts(self, lang):
        """
        returns a dict containing available suboptions for the given
        translation type, or if there aren't any it will return None
        """

        # split lang code
        langs = lang.split('_')
        prilang = langs[0]
        seclang = langs[1]

        soup = self.soup
        # let's find the javascript containing the suboptions
        # get javascripts
        jss = soup.findAll('script')

        # I bet this will break someday...
        js = ''
        for x in jss:
            for y in x.contents:
                if 'lang_opts' in y:
                    js = y
        # if we don't have any options, break here and return None
        if js == '':
            return None

        # otherwise, move on with processing
        splitted = js.split('\n')
        pri_conds = []
        sec_conds = []
        pri_todos = []
        sec_todos = []
        for z in splitted:
            # nested ifs for readability
            if 'if (' in z:
                if prilang in z or seclang in z:
                    conds = z.split('(')
                    for x in conds[1:]:
                        if not ')' in x:
                            # primary condition
                            pri_conds.append(x)
                        else:
                            raw_cond = x.split(')')[0]
                            if '&&' in x or '||' in x:
                                # secondary condition
                                sec_conds.append(raw_cond)
                            else:
                                if not 'localel' in x:
                                    # still primary condition
                                    pri_conds.append(raw_cond)
                                else:
                                    # or a primary condition's todo
                                    todo = x.split('=')
                                    for j in xrange(len(todo)):
                                        item = todo[j]
                                        if 'localel.innerHTML' in item:
                                            do = ''.join(todo[j+1:])
                                            pri_todos.append(
                                                do.replace(';', ''))
                            if 'optsel' in x:
                                # secondary condition's todo
                                todo = x.split('=')
                                for i in xrange(len(todo)):
                                    item = todo[i]
                                    if 'optsel.innerHTML' in item:
                                        do = ''.join(todo[i+1:])
                                        # we don't want ";"
                                        sec_todos.append(do.replace(';', ''))

        print pri_conds
        print
        print sec_conds
        print
        print pri_todos
        print
        print sec_todos

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

