#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata, json

with open('IPA.json') as ipajson:
    IPA = json.loads(ipajson.read())

def splitclusters(s):
    """Generate the grapheme clusters for the string s. (Not the full
    Unicode text segmentation algorithm, but probably good enough for
    Devanagari.)

    """
    virama = u'\N{DEVANAGARI SIGN VIRAMA}'
    cluster = u''
    last = None
    for c in s:
        cat = unicodedata.category(c)[0]
        if cat == 'M' or cat == 'L' and last == virama:
            cluster += c
        else:
            if cluster:
                yield cluster
            cluster = c
        last = c
    if cluster:
        yield cluster


name_in_indic = ''.join(raw_input('Enter your name in devanagari: ').decode('utf8').split(' '))
letters = list(splitclusters(name_in_indic))

print(''.join(letters))

for letter in letters:
    for key, value in IPA.iteritems():
        if letter in value:
            print (key),
