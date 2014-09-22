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
    return os.path.splitext(os.path.basename(wtfpath))[0].lower()


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


def loadwtfsandfonts(stylesfolder, fontregistry):
    # scan wtfs and find valid fonts
    wtfsbyname = loadwtfs(stylesfolder)
    for name,values in wtfsbyname.items():
        values['fonts'] = list(fontsforwtf(values['wtfdata'], fontregistry))

    return wtfsbyname

def typefaces(wtf):
    typefaces = {}
    for font_path in wtf['fonts']:
        f = ttfquery.describe.openFont(font_path)
        font,typeface = ttfquery.describe.shortName(f)
        if typeface not in typefaces:
            typefaces[typeface] = {}
        typefaces[typeface][font] = os.path.basename(font_path)
    return typefaces


def typefacesbywtf(wtfsbyname):
    typefaces_by_wtf =  {}
    for name,wtf in wtfsbyname.items():
        typefaces_by_wtf[name] = typefaces(wtf)
    print typefaces_by_wtf


if __name__ == '__main__':
    # scan fonts
    fontreg = ttfquery.ttffiles.Registry()
    fontreg.scan('./fonts/')
    wtfsbyname = loadwtfsandfonts('./langs/',fontreg)

    #print typefacesbywtf(wtfsbyname)
    print wtfsbyname



