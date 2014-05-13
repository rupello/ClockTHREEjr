__author__ = 'rupello'

import sys
import os
import json
import numpy

import Simulate

def rowcol2div(row,col):
    "returns div id ef '#a0' for row=0, col=0, '#b1' for col=1, row=2  etc.."
    return '#{}{}'.format(chr(97+col),row)

def makeworddivs(data):
    "return a list of jquery selectors for each word"
    worddivs=[]
    for i,w in enumerate(data['words']):
        row = data['rows'][i]    # the row index of w
        col = data['cols'][i]    # the starting column index of w
        wlen = data['lens'][i]   # the length of w (in leds)
        worddivs.append(','.join([rowcol2div((col+offset),row) for offset in range(wlen)]))
    return worddivs

def makesentences(data):
    "return a list of word indeces for each sentence"
    return [(numpy.where(sentence)[0]).tolist() for sentence in data['data']]

def data2json(data):
    worddivs = makeworddivs(data)
    sentences = makesentences(data)
    return json.dumps({'words':worddivs,'sentences':sentences})

if __name__ == '__main__':
    data = Simulate.readwtf('langs/English_v2.wtf')
    print data2json(data)[:100]
