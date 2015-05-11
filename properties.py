__author__ = 'Avinesh_Kumar'

import logging
import itertools

properties = {}


def loadproperties(pfile):
    for line in open(pfile):
        sepindex = 0
        endi = 0
        hasbackslash = 0
        isback = 0
        arrayc = list(line)
        iterator = range(0, arrayc.__len__()).__iter__()
        key = ''
        # print arrayc
        if arrayc[0] == '#' or not line.strip():
            # print "continue"
            continue
        else:
            # print "in else"
            for i in iterator:
                c = arrayc[i]
                hasbackslash = 0
                if c == '\\':
                    # print "back"
                    isback = 1
                    i = iterator.next()
                    hasbackslash += 1
                    while arrayc[i] == '\\':
                        hasbackslash += 1
                        i = iterator.next()
                    # print "my i=", i
                    for k in range(0, hasbackslash/2):
                        key += '\\'
                else:
                    if not sepindex and not (c == '=' or c == ':' or c == '\n' or c == '\r'):
                        key += c

                c = arrayc[i]
                # print c
                if not (hasbackslash % 2) and (c == '=' or c == ':'):
                    # print "sepindex has", i, c
                    hasbackslash = 0
                    if not sepindex:
                        sepindex = i
                    continue
                elif (hasbackslash % 2) and (c == '=' or c == ':'):
                    key += c
                else:
                    hasbackslash = 0

                # print key
                if c == '#' or c == '\n':
                    endi = i
                    # print "endindex", i
                    break
                else:
                    endi = i
            # print "sep index: ", sepindex
            # print "end index: ", endi
            # print "key: ", key
            if sepindex:
                if isback:
                    properties.__setitem__(key.strip(), ''.join(arrayc[sepindex + 1:endi+1]).strip())
                else:
                    properties.__setitem__(''.join(arrayc[0:sepindex]).strip(), ''.join(arrayc[sepindex + 1:endi+1]).strip())
            else:
                if isback:
                    properties.__setitem__(key.strip(), '')
                else:
                    properties.__setitem__(''.join(arrayc[0:endi]).strip(), '')

    return properties





