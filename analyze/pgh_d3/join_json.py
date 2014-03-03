#!/usr/bin/env python

# takes one file with one json object per line, outputs a file with an array
# of json objects.

import fileinput, sys

sys.stdout.write('[\n')

isFirst = True
# Have to avoid a trailing comma. So we write the ,\n and then the line, for
# every line except the first.
for line in fileinput.input():
    if not isFirst:
        sys.stdout.write(',\n')
    isFirst = False
    sys.stdout.write(line.strip())

sys.stdout.write(']\n')
sys.stdout.close()
