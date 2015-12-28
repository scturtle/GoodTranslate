#!/usr/bin/env python
import re
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
from tk import calc_tk

text = os.environ.get('POPCLIP_TEXT', 'hello world')
destlang = os.environ.get('POPCLIP_OPTION_DESTLANG', 'zh-CN')
ttslang = os.environ.get('POPCLIP_OPTION_TTSLANG', 'en')
tts = os.environ.get('POPCLIP_OPTION_TTS', '1')

translator = Translator(to_lang=destlang)
translation = translator.translate(text.replace('\n', ' '))
if sys.getdefaultencoding() != "utf-8":
    translation = translation.encode('utf-8')
sys.stdout.write(translation)


def split_trunks(text):
    ''' stolen from ``bettertranslate`` '''
    text = text.replace('\n', '')
    sentences = re.split(r'([\,\.\;]+)\s*', text)
    trunks = []
    for idx, sen in enumerate(sentences):
        if trunks and len(trunks[-1]) + 1 + len(sen) < 200:
            trunks[-1] += (' ' if trunks[-1][-1] in ',.;' else '') + sen
            continue
        arr = []
        tmp = ''
        for w in re.split(' ', sen):
            if len(tmp) + 1 + len(w) < 200:
                tmp += (' ' if tmp else '') + w
            else:
                arr.append(tmp)
                assert len(w) < 200, 'word too long'
                tmp = w
        arr.append(tmp)
        trunks.extend(arr)
    return trunks

if tts == '1':
    f = NamedTemporaryFile(delete=False)
    for text in split_trunks(text):
        r = request.Request(
                url=('http://translate.google.com/translate_tts'
                     '?tl=%s&ie=UTF-8&client=t&tk=%s&q=%s') % (ttslang, calc_tk(text), quote(text, '')),
                headers={'User-Agent': 'Mozilla/5.0',
                         'Referer': 'https://translate.google.com/'})
        f.write(request.urlopen(r).read())
    f.close()
    os.system('afplay ' + f.name)
    os.unlink(f.name)
