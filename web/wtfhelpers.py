import os
import sys
import string
import codecs


import ttfquery.ttffiles
import ttfquery.describe
import ttfquery.glyphquery

from clockface import decodeLetters
import Simulate


def wtffiles(wtfdir):
    """list wtffiles in folder"""
    wtffiles = []
    for path,dirs,files in os.walk(wtfdir):
        for f in files:
            wtfpath = os.path.join(path,f)
            if os.path.splitext(wtfpath)[1].lower()=='.wtf':
                wtffiles.append(wtfpath)
    return wtffiles

def wtfname(wtfpath):
    return os.path.splitext(os.path.basename(wtfpath))[0]


def loadwtfs(folder):
    """ load wtfs in folder"""
    wtfbyname = {}
    for wtfpath in wtffiles(folder):
        try:
            name = wtfname(wtfpath)
            wtfdata = Simulate.readwtf(wtfpath)
            wtfbyname[name] = {}
            wtfbyname[name]['wtfpath'] = wtfpath
            wtfbyname[name]['wtfdata'] = wtfdata
        except Exception as exc:
            print exc

    return wtfbyname


def findvalidfonts(fontpaths,testtext):
       """find fonts in the list fontpaths that contain glyphs for testtext"""
       s = set(fontpaths)
       for fontpath in fontpaths:
           f = ttfquery.describe.openFont(fontpath)
           for uc in testtext:
               if not ttfquery.glyphquery.hasGlyph(f,uc):
                   s.remove(fontpath)
                   break
       return s


def fontsforwtf(wtfdata,fontreg):
    """ retun valid font files in fontreg for wtf at wtfpath"""
    lines = decodeLetters(style=wtfdata['letters'],case=string.lower)
    first_line_chars = ''.join(x for x in lines[0])
    return findvalidfonts(fontreg.files,first_line_chars)


def loadwtfsandfonts(stylesfolder,fontregistry):
    # scan wtfs and find valid fonts
    wtfsbyname = loadwtfs(stylesfolder)
    for name,values in wtfsbyname.items():
        values['fonts'] = fontsforwtf(values['wtfdata'],fontregistry)

    return wtfsbyname


if __name__ == '__main__':
    # scan fonts
    fontreg = ttfquery.ttffiles.Registry()
    fontreg.scan(os.path.expanduser('./fonts/'))

    wtfsbyname = loadwtfsandfonts('./langs/',fontreg)
    for name,values in wtfsbyname.items():
        print name
        print values['wtfpath']
        print values['fonts']




