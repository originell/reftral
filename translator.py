"""
Example translate app
"""

import reftral

translat0r = reftral.Translator()

TEXT = """
Hallo,

meine

Lieblingssprache
ist

Python"""

ready = translat0r.translate('de_en', TEXT)
#print ready
print ' '.join(ready)
