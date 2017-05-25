#!/usr/bin/env python

import random
import re

n_words = 1000

words = [
  re.sub(r'[^a-z]', '', line.strip().lower())
  for line in open('/etc/dictionaries-common/words')
]
words = [re.sub('\'s', '', w) for w in words]
random.seed(1)
print '\n'.join(sorted(random.sample(words, n_words)))
