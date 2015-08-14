#!/usr/bin/env python
import os
import sys
from translate import Translator
from tempfile import NamedTemporaryFile
try:
    import urllib2 as request
    from urllib import quote
except:
    from urllib import request
    from urllib.parse import quote

text = os.environ.get('POPCLIP_TEXT', 'hello world')
destlang = os.environ.get('POPCLIP_OPTION_DESTLANG', 'zh-CN')
ttslang = os.environ.get('POPCLIP_OPTION_TTSLANG', 'en')
tts = os.environ.get('POPCLIP_OPTION_TTS', '1')

translator = Translator(to_lang=destlang)
translation = translator.translate(text)
sys.stdout.write(translation + '\n')

if tts == '1':
    r = request.Request(
            url=('http://translate.google.com/translate_tts'
                 '?tl=%s&ie=UTF-8&client=t&q=%s') % (ttslang, quote(text, '')),
            headers={'User-Agent': 'Mozilla/5.0',
                     'Referer': 'https://translate.google.com/'})
    f = NamedTemporaryFile(delete=False)
    f.write(request.urlopen(r).read())
    f.close()
    os.system('afplay {0}'.format(f.name))
    os.unlink(f.name)
