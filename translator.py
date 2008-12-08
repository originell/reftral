"""
Example translate app
"""

import reftral

translat0r = reftral.Translator()

TEXT = """
Hallo

mein

Name
ist

Python"""

ready = translat0r.translate('de_en', TEXT)
print ready
