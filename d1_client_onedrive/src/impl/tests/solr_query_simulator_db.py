#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
''':mod:`solr_simulator_db`
===========================

:Synopsis:
 - Database of faceted objects for Solr simulator.
:Author: DataONE (Dahl)
'''
'''
This file contains a generated database of faceted objects. The facets names
and values are:

color: white, red, green, blue, yellow
shape: square, rectangle, circle, oval, pentagon
texture: rough, smooth, firm, soft, hard
weight: light, lighter, medium, heavy, heavier

The object name is a combination of its facet values.

The db contains 1000 objects. Duplicates are allowed.
'''

# Stdlib.
import itertools
import logging
import pprint
import random

# Set up logger for this module.
log = logging.getLogger(__name__)

facets = {
  'color': ('white', 'red', 'green', 'blue', 'yellow'),
  'shape': ('square', 'rectangle', 'circle', 'oval', 'pentagon'),
  'texture': ('rough', 'smooth', 'firm', 'soft', 'hard'),
  'weight': ('light', 'lighter', 'medium', 'heavy', 'heavier'),
}

facet_order = ['color', 'shape', 'texture', 'weight']

faceted_objects = [
  ('yellow-rectangle-soft-lighter', 'yellow', 'rectangle', 'soft', 'lighter'),
  ('blue-square-rough-lighter', 'blue', 'square', 'rough', 'lighter'),
  ('red-oval-smooth-medium', 'red', 'oval', 'smooth', 'medium'),
  ('green-pentagon-smooth-heavier', 'green', 'pentagon', 'smooth', 'heavier'),
  ('green-circle-firm-light', 'green', 'circle', 'firm', 'light'),
  ('yellow-circle-firm-medium', 'yellow', 'circle', 'firm', 'medium'),
  ('red-rectangle-hard-lighter', 'red', 'rectangle', 'hard', 'lighter'),
  ('yellow-rectangle-soft-light', 'yellow', 'rectangle', 'soft', 'light'),
  ('blue-square-firm-heavy', 'blue', 'square', 'firm', 'heavy'),
  ('green-oval-rough-heavy', 'green', 'oval', 'rough', 'heavy'),
  ('white-oval-hard-heavier', 'white', 'oval', 'hard', 'heavier'),
  ('blue-circle-soft-light', 'blue', 'circle', 'soft', 'light'),
  ('green-circle-hard-light', 'green', 'circle', 'hard', 'light'),
  ('white-pentagon-rough-heavy', 'white', 'pentagon', 'rough', 'heavy'),
  ('blue-pentagon-hard-medium', 'blue', 'pentagon', 'hard', 'medium'),
  ('yellow-rectangle-firm-medium', 'yellow', 'rectangle', 'firm',
   'medium'), ('blue-circle-firm-medium', 'blue', 'circle', 'firm', 'medium'), (
     'red-rectangle-rough-heavier', 'red', 'rectangle', 'rough', 'heavier'), (
       'white-rectangle-hard-medium', 'white', 'rectangle', 'hard', 'medium'), (
         'yellow-pentagon-rough-lighter', 'yellow', 'pentagon', 'rough', 'lighter'), (
           'yellow-rectangle-smooth-medium', 'yellow', 'rectangle', 'smooth', 'medium'), (
             'green-oval-rough-heavy', 'green', 'oval', 'rough', 'heavy'),
  ('green-rectangle-rough-heavier', 'green', 'rectangle', 'rough', 'heavier'), (
    'red-circle-rough-light', 'red', 'circle', 'rough', 'light'), (
      'blue-rectangle-firm-lighter', 'blue', 'rectangle', 'firm', 'lighter'), (
        'green-pentagon-soft-lighter', 'green', 'pentagon', 'soft', 'lighter'), (
          'green-oval-smooth-light', 'green', 'oval', 'smooth', 'light'), (
            'white-rectangle-rough-light', 'white', 'rectangle', 'rough', 'light'), (
              'white-square-smooth-light', 'white', 'square', 'smooth', 'light'), (
                'white-square-rough-lighter', 'white', 'square', 'rough', 'lighter'), (
                  'green-pentagon-hard-lighter', 'green', 'pentagon', 'hard', 'lighter'),
  ('green-rectangle-rough-heavier', 'green', 'rectangle', 'rough', 'heavier'), (
    'white-oval-rough-heavier', 'white', 'oval', 'rough', 'heavier'), (
      'yellow-oval-firm-medium', 'yellow', 'oval', 'firm', 'medium'), (
        'yellow-rectangle-firm-light', 'yellow', 'rectangle', 'firm', 'light'), (
          'white-oval-hard-heavy', 'white', 'oval', 'hard', 'heavy'), (
            'white-rectangle-soft-lighter', 'white', 'rectangle', 'soft', 'lighter'), (
              'green-pentagon-rough-light', 'green', 'pentagon', 'rough', 'light'), (
                'yellow-square-smooth-medium', 'yellow', 'square', 'smooth', 'medium'), (
                  'blue-rectangle-rough-heavy', 'blue', 'rectangle', 'rough', 'heavy'), (
                    'blue-circle-firm-lighter', 'blue', 'circle', 'firm', 'lighter'),
  ('blue-oval-smooth-medium', 'blue', 'oval', 'smooth', 'medium'), (
    'green-oval-hard-heavier', 'green', 'oval', 'hard', 'heavier'), (
      'green-square-firm-heavier', 'green', 'square', 'firm', 'heavier'), (
        'green-circle-firm-lighter', 'green', 'circle', 'firm', 'lighter'), (
          'blue-pentagon-firm-medium', 'blue', 'pentagon', 'firm', 'medium'), (
            'blue-square-smooth-heavy', 'blue', 'square', 'smooth', 'heavy'), (
              'blue-pentagon-soft-light', 'blue', 'pentagon', 'soft', 'light'), (
                'red-pentagon-soft-heavy', 'red', 'pentagon', 'soft', 'heavy'), (
                  'green-pentagon-smooth-heavy', 'green', 'pentagon', 'smooth', 'heavy'),
  ('green-oval-firm-heavier', 'green', 'oval', 'firm', 'heavier'), (
    'blue-pentagon-smooth-medium', 'blue', 'pentagon', 'smooth', 'medium'), (
      'green-rectangle-smooth-heavy', 'green', 'rectangle', 'smooth', 'heavy'), (
        'blue-rectangle-soft-light', 'blue', 'rectangle', 'soft', 'light'), (
          'green-oval-hard-lighter', 'green', 'oval', 'hard', 'lighter'), (
            'green-oval-firm-light', 'green', 'oval', 'firm', 'light'), (
              'white-rectangle-hard-lighter', 'white', 'rectangle', 'hard', 'lighter'), (
                'green-circle-soft-medium', 'green', 'circle', 'soft', 'medium'), (
                  'green-oval-smooth-light', 'green', 'oval', 'smooth', 'light'), (
                    'blue-pentagon-soft-heavier', 'blue', 'pentagon', 'soft', 'heavier'),
  ('blue-square-smooth-lighter', 'blue', 'square', 'smooth', 'lighter'), (
    'yellow-rectangle-firm-medium', 'yellow', 'rectangle', 'firm', 'medium'), (
      'green-rectangle-hard-medium', 'green', 'rectangle', 'hard', 'medium'), (
        'blue-pentagon-soft-heavy', 'blue', 'pentagon', 'soft', 'heavy'), (
          'green-rectangle-rough-lighter', 'green', 'rectangle', 'rough', 'lighter'), (
            'yellow-rectangle-firm-medium', 'yellow', 'rectangle', 'firm', 'medium'), (
              'white-pentagon-rough-heavy', 'white', 'pentagon', 'rough', 'heavy'), (
                'white-circle-smooth-heavy', 'white', 'circle', 'smooth', 'heavy'), (
                  'blue-rectangle-firm-heavier', 'blue', 'rectangle', 'firm', 'heavier'),
  ('green-rectangle-rough-heavy', 'green', 'rectangle', 'rough', 'heavy'), (
    'blue-pentagon-hard-lighter', 'blue', 'pentagon', 'hard', 'lighter'), (
      'yellow-square-smooth-medium', 'yellow', 'square', 'smooth', 'medium'), (
        'blue-square-smooth-lighter', 'blue', 'square', 'smooth', 'lighter'), (
          'yellow-circle-firm-lighter', 'yellow', 'circle', 'firm', 'lighter'), (
            'green-square-hard-lighter', 'green', 'square', 'hard', 'lighter'), (
              'green-rectangle-firm-medium', 'green', 'rectangle', 'firm', 'medium'), (
                'white-square-soft-light', 'white', 'square', 'soft', 'light'), (
                  'blue-circle-smooth-medium', 'blue', 'circle', 'smooth', 'medium'), (
                    'blue-circle-soft-medium', 'blue', 'circle', 'soft', 'medium'), (
                      'white-oval-firm-heavier', 'white', 'oval', 'firm', 'heavier'), (
                        'white-circle-hard-heavy', 'white', 'circle', 'hard', 'heavy'), (
                          'blue-oval-hard-lighter', 'blue', 'oval', 'hard', 'lighter'),
  ('white-pentagon-smooth-medium', 'white', 'pentagon', 'smooth', 'medium'), (
    'red-rectangle-soft-heavier', 'red', 'rectangle', 'soft', 'heavier'), (
      'yellow-rectangle-hard-heavy', 'yellow', 'rectangle', 'hard', 'heavy'), (
        'yellow-rectangle-firm-heavier', 'yellow', 'rectangle', 'firm', 'heavier'), (
          'red-rectangle-rough-medium', 'red', 'rectangle', 'rough', 'medium'), (
            'white-rectangle-soft-heavier', 'white', 'rectangle', 'soft',
            'heavier'), ('white-circle-firm-light', 'white', 'circle', 'firm', 'light'), (
              'green-pentagon-soft-light', 'green', 'pentagon', 'soft', 'light'), (
                'white-pentagon-soft-heavier', 'white', 'pentagon', 'soft', 'heavier'), (
                  'red-circle-smooth-lighter', 'red', 'circle', 'smooth', 'lighter'), (
                    'blue-square-smooth-heavy', 'blue', 'square', 'smooth', 'heavy'), (
                      'blue-square-soft-medium', 'blue', 'square', 'soft', 'medium'),
  ('blue-square-rough-lighter', 'blue', 'square', 'rough', 'lighter'), (
    'green-square-soft-lighter', 'green', 'square', 'soft', 'lighter'), (
      'green-circle-soft-heavy', 'green', 'circle', 'soft', 'heavy'), (
        'blue-oval-hard-medium', 'blue', 'oval', 'hard', 'medium'), (
          'green-oval-soft-heavy', 'green', 'oval', 'soft', 'heavy'), (
            'red-pentagon-rough-light', 'red', 'pentagon', 'rough', 'light'), (
              'yellow-pentagon-firm-heavier', 'yellow', 'pentagon', 'firm', 'heavier'), (
                'red-square-rough-light', 'red', 'square', 'rough', 'light'), (
                  'yellow-circle-rough-heavy', 'yellow', 'circle', 'rough', 'heavy'), (
                    'blue-square-firm-lighter', 'blue', 'square', 'firm', 'lighter'), (
                      'red-circle-soft-heavier', 'red', 'circle', 'soft', 'heavier'), (
                        'green-oval-firm-heavier', 'green', 'oval', 'firm', 'heavier'),
  ('red-circle-firm-heavy', 'red', 'circle', 'firm', 'heavy'), (
    'green-pentagon-soft-heavier', 'green', 'pentagon', 'soft', 'heavier'), (
      'yellow-pentagon-rough-medium', 'yellow', 'pentagon', 'rough', 'medium'), (
        'red-pentagon-hard-heavy', 'red', 'pentagon', 'hard', 'heavy'), (
          'red-square-firm-light', 'red', 'square', 'firm', 'light'), (
            'red-square-firm-heavy', 'red', 'square', 'firm', 'heavy'), (
              'yellow-oval-hard-heavy', 'yellow', 'oval', 'hard', 'heavy'), (
                'white-circle-hard-heavier', 'white', 'circle', 'hard', 'heavier'), (
                  'yellow-circle-soft-light', 'yellow', 'circle', 'soft', 'light'), (
                    'blue-square-firm-medium', 'blue', 'square', 'firm', 'medium'), (
                      'blue-oval-rough-light', 'blue', 'oval', 'rough', 'light'), (
                        'blue-oval-smooth-heavier', 'blue', 'oval', 'smooth', 'heavier'),
  ('white-rectangle-rough-heavier', 'white', 'rectangle', 'rough', 'heavier'), (
    'yellow-pentagon-hard-lighter', 'yellow', 'pentagon', 'hard',
    'lighter'), ('blue-square-hard-light', 'blue', 'square', 'hard', 'light'), (
      'red-oval-firm-heavier', 'red', 'oval', 'firm', 'heavier'), (
        'red-rectangle-smooth-heavy', 'red', 'rectangle', 'smooth',
        'heavy'), ('blue-circle-soft-heavy', 'blue', 'circle', 'soft', 'heavy'), (
          'yellow-square-hard-light', 'yellow', 'square', 'hard',
          'light'), ('blue-circle-hard-heavy', 'blue', 'circle', 'hard', 'heavy'), (
            'blue-pentagon-rough-heavier', 'blue', 'pentagon', 'rough', 'heavier'), (
              'yellow-oval-hard-lighter', 'yellow', 'oval', 'hard', 'lighter'), (
                'blue-pentagon-rough-heavier', 'blue', 'pentagon', 'rough', 'heavier'), (
                  'white-rectangle-hard-light', 'white', 'rectangle', 'hard', 'light'), (
                    'red-circle-firm-light', 'red', 'circle', 'firm', 'light'),
  ('yellow-rectangle-firm-medium', 'yellow', 'rectangle', 'firm', 'medium'), (
    'blue-oval-rough-light', 'blue', 'oval', 'rough', 'light'), (
      'green-pentagon-rough-lighter', 'green', 'pentagon', 'rough', 'lighter'), (
        'yellow-square-smooth-heavier', 'yellow', 'square', 'smooth', 'heavier'), (
          'white-square-rough-light', 'white', 'square', 'rough', 'light'), (
            'blue-rectangle-hard-lighter', 'blue', 'rectangle', 'hard', 'lighter'), (
              'white-pentagon-soft-light', 'white', 'pentagon', 'soft', 'light'), (
                'blue-rectangle-soft-lighter', 'blue', 'rectangle', 'soft', 'lighter'), (
                  'white-square-smooth-heavy', 'white', 'square', 'smooth', 'heavy'), (
                    'green-circle-smooth-light', 'green', 'circle', 'smooth', 'light'),
  ('green-rectangle-soft-heavier', 'green', 'rectangle',
   'soft', 'heavier'), ('red-pentagon-hard-heavy', 'red', 'pentagon', 'hard', 'heavy'), (
     'blue-circle-soft-medium', 'blue', 'circle', 'soft', 'medium'), (
       'red-circle-smooth-light', 'red', 'circle', 'smooth', 'light'), (
         'green-square-soft-heavier', 'green', 'square', 'soft', 'heavier'), (
           'yellow-oval-hard-medium', 'yellow', 'oval', 'hard', 'medium'), (
             'green-rectangle-rough-heavy', 'green', 'rectangle', 'rough', 'heavy'), (
               'red-rectangle-hard-heavier', 'red', 'rectangle', 'hard', 'heavier'), (
                 'yellow-rectangle-hard-heavy', 'yellow', 'rectangle', 'hard', 'heavy'), (
                   'green-circle-rough-medium', 'green', 'circle', 'rough', 'medium'), (
                     'red-square-soft-heavy', 'red', 'square', 'soft', 'heavy'),
  ('green-rectangle-soft-heavier', 'green', 'rectangle',
   'soft', 'heavier'), ('green-circle-firm-light', 'green', 'circle', 'firm', 'light'), (
     'blue-square-firm-medium', 'blue', 'square', 'firm', 'medium'), (
       'yellow-oval-soft-heavy', 'yellow', 'oval', 'soft', 'heavy'), (
         'blue-pentagon-hard-heavier', 'blue', 'pentagon', 'hard', 'heavier'), (
           'yellow-pentagon-soft-heavy', 'yellow', 'pentagon', 'soft', 'heavy'), (
             'yellow-pentagon-firm-light', 'yellow', 'pentagon', 'firm', 'light'), (
               'blue-rectangle-hard-lighter', 'blue', 'rectangle', 'hard', 'lighter'), (
                 'blue-rectangle-rough-heavier', 'blue', 'rectangle', 'rough', 'heavier'),
  ('green-rectangle-soft-lighter', 'green', 'rectangle',
   'soft', 'lighter'), ('yellow-oval-rough-light', 'yellow', 'oval', 'rough', 'light'), (
     'yellow-square-smooth-light', 'yellow', 'square', 'smooth', 'light'), (
       'green-pentagon-smooth-heavier', 'green', 'pentagon', 'smooth', 'heavier'), (
         'white-oval-rough-medium', 'white', 'oval', 'rough', 'medium'), (
           'yellow-circle-smooth-lighter', 'yellow', 'circle', 'smooth', 'lighter'), (
             'green-circle-hard-light', 'green', 'circle', 'hard', 'light'), (
               'blue-circle-hard-heavy', 'blue', 'circle', 'hard', 'heavy'), (
                 'blue-square-rough-medium', 'blue', 'square', 'rough', 'medium'), (
                   'green-rectangle-soft-heavy', 'green', 'rectangle', 'soft', 'heavy'), (
                     'white-oval-smooth-lighter', 'white', 'oval', 'smooth', 'lighter'),
  ('yellow-rectangle-soft-lighter', 'yellow', 'rectangle', 'soft', 'lighter'), (
    'red-circle-hard-light', 'red', 'circle', 'hard', 'light'), (
      'green-square-smooth-heavier', 'green', 'square', 'smooth', 'heavier'), (
        'yellow-square-soft-medium', 'yellow', 'square', 'soft', 'medium'), (
          'yellow-oval-smooth-light', 'yellow', 'oval', 'smooth', 'light'), (
            'yellow-circle-smooth-heavier', 'yellow', 'circle', 'smooth', 'heavier'), (
              'red-square-smooth-light', 'red', 'square', 'smooth', 'light'), (
                'blue-oval-hard-heavy', 'blue', 'oval', 'hard', 'heavy'), (
                  'yellow-circle-soft-light', 'yellow', 'circle', 'soft', 'light'), (
                    'blue-oval-soft-light', 'blue', 'oval', 'soft', 'light'), (
                      'blue-rectangle-hard-light', 'blue', 'rectangle', 'hard', 'light'),
  ('green-circle-hard-heavy', 'green', 'circle', 'hard', 'heavy'), (
    'white-square-hard-heavy', 'white', 'square', 'hard', 'heavy'), (
      'white-circle-firm-lighter', 'white', 'circle', 'firm', 'lighter'), (
        'blue-pentagon-hard-heavy', 'blue', 'pentagon', 'hard', 'heavy'), (
          'blue-rectangle-firm-medium', 'blue', 'rectangle', 'firm', 'medium'), (
            'red-rectangle-soft-light', 'red', 'rectangle', 'soft', 'light'), (
              'green-rectangle-soft-heavier', 'green', 'rectangle', 'soft', 'heavier'), (
                'yellow-square-soft-heavy', 'yellow', 'square', 'soft', 'heavy'), (
                  'blue-oval-soft-medium', 'blue', 'oval', 'soft', 'medium'), (
                    'green-pentagon-soft-heavy', 'green', 'pentagon', 'soft', 'heavy'), (
                      'red-pentagon-smooth-heavy', 'red', 'pentagon', 'smooth', 'heavy'),
  ('yellow-pentagon-firm-lighter', 'yellow', 'pentagon', 'firm', 'lighter'), (
    'green-circle-hard-medium', 'green', 'circle', 'hard', 'medium'), (
      'red-oval-smooth-heavier', 'red', 'oval', 'smooth', 'heavier'), (
        'yellow-oval-firm-heavier', 'yellow', 'oval', 'firm', 'heavier'), (
          'green-square-firm-medium', 'green', 'square', 'firm', 'medium'), (
            'red-rectangle-smooth-medium', 'red', 'rectangle', 'smooth', 'medium'), (
              'yellow-square-firm-light', 'yellow', 'square', 'firm', 'light'), (
                'blue-square-hard-lighter', 'blue', 'square', 'hard', 'lighter'), (
                  'white-oval-rough-heavier', 'white', 'oval', 'rough', 'heavier'), (
                    'yellow-square-hard-medium', 'yellow', 'square', 'hard', 'medium'), (
                      'red-oval-firm-lighter', 'red', 'oval', 'firm', 'lighter'),
  ('yellow-square-smooth-lighter', 'yellow', 'square', 'smooth', 'lighter'), (
    'green-pentagon-smooth-lighter', 'green', 'pentagon', 'smooth',
    'lighter'), ('yellow-pentagon-hard-heavy', 'yellow', 'pentagon', 'hard', 'heavy'), (
      'yellow-square-smooth-light', 'yellow', 'square', 'smooth', 'light'), (
        'yellow-pentagon-soft-heavier', 'yellow', 'pentagon', 'soft',
        'heavier'), ('red-oval-firm-heavy', 'red', 'oval', 'firm', 'heavy'), (
          'red-circle-smooth-medium', 'red', 'circle', 'smooth', 'medium'), (
            'green-rectangle-hard-medium', 'green', 'rectangle', 'hard',
            'medium'), ('red-oval-hard-lighter', 'red', 'oval', 'hard', 'lighter'), (
              'green-oval-hard-heavier', 'green', 'oval', 'hard', 'heavier'), (
                'red-circle-smooth-lighter', 'red', 'circle', 'smooth', 'lighter'), (
                  'blue-pentagon-firm-heavier', 'blue', 'pentagon', 'firm', 'heavier'), (
                    'white-circle-smooth-heavy', 'white', 'circle', 'smooth', 'heavy'), (
                      'green-pentagon-hard-light', 'green', 'pentagon', 'hard', 'light'),
  ('yellow-pentagon-hard-light', 'yellow', 'pentagon', 'hard', 'light'), (
    'yellow-rectangle-hard-heavier', 'yellow', 'rectangle', 'hard', 'heavier'), (
      'yellow-square-smooth-heavier', 'yellow', 'square', 'smooth',
      'heavier'), ('white-rectangle-firm-light', 'white', 'rectangle', 'firm', 'light'), (
        'blue-square-rough-light', 'blue', 'square', 'rough', 'light'), (
          'red-square-rough-light', 'red', 'square', 'rough', 'light'), (
            'blue-pentagon-rough-lighter', 'blue', 'pentagon', 'rough', 'lighter'), (
              'white-oval-rough-medium', 'white', 'oval', 'rough', 'medium'), (
                'green-rectangle-rough-light', 'green', 'rectangle', 'rough', 'light'), (
                  'red-pentagon-firm-heavier', 'red', 'pentagon', 'firm', 'heavier'), (
                    'white-oval-firm-heavier', 'white', 'oval', 'firm', 'heavier'),
  ('yellow-rectangle-firm-heavy', 'yellow', 'rectangle',
   'firm', 'heavy'), ('white-square-firm-medium', 'white', 'square', 'firm', 'medium'), (
     'red-rectangle-firm-light', 'red', 'rectangle', 'firm', 'light'), (
       'red-square-smooth-heavier', 'red', 'square', 'smooth', 'heavier'), (
         'green-rectangle-firm-light', 'green', 'rectangle', 'firm', 'light'), (
           'yellow-square-firm-light', 'yellow', 'square', 'firm', 'light'), (
             'blue-pentagon-soft-lighter', 'blue', 'pentagon', 'soft',
             'lighter'), ('blue-square-soft-light', 'blue', 'square', 'soft', 'light'), (
               'yellow-pentagon-firm-heavy', 'yellow', 'pentagon', 'firm', 'heavy'), (
                 'green-pentagon-firm-lighter', 'green', 'pentagon', 'firm', 'lighter'), (
                   'red-oval-rough-lighter', 'red', 'oval', 'rough', 'lighter'), (
                     'blue-oval-hard-heavy', 'blue', 'oval', 'hard', 'heavy'), (
                       'blue-circle-firm-heavy', 'blue', 'circle', 'firm', 'heavy'),
  ('yellow-rectangle-firm-heavier', 'yellow', 'rectangle', 'firm', 'heavier'), (
    'white-square-rough-heavy', 'white', 'square', 'rough',
    'heavy'), ('white-circle-smooth-lighter', 'white', 'circle', 'smooth', 'lighter'), (
      'red-rectangle-firm-lighter', 'red', 'rectangle', 'firm',
      'lighter'), ('yellow-oval-firm-heavy', 'yellow', 'oval', 'firm', 'heavy'), (
        'white-rectangle-soft-lighter', 'white', 'rectangle', 'soft', 'lighter'), (
          'yellow-circle-rough-medium', 'yellow', 'circle', 'rough', 'medium'), (
            'green-pentagon-soft-heavier', 'green', 'pentagon', 'soft',
            'heavier'), ('red-circle-soft-light', 'red', 'circle', 'soft', 'light'), (
              'white-oval-hard-heavier', 'white', 'oval', 'hard', 'heavier'), (
                'green-pentagon-rough-heavy', 'green', 'pentagon', 'rough', 'heavy'), (
                  'yellow-circle-rough-heavier', 'yellow', 'circle', 'rough', 'heavier'),
  ('red-square-rough-medium', 'red', 'square', 'rough',
   'medium'), ('green-oval-firm-heavier', 'green', 'oval', 'firm', 'heavier'), (
     'red-pentagon-smooth-lighter', 'red', 'pentagon', 'smooth',
     'lighter'), ('red-square-smooth-heavy', 'red', 'square', 'smooth', 'heavy'), (
       'blue-rectangle-smooth-medium', 'blue', 'rectangle', 'smooth',
       'medium'), ('red-rectangle-soft-heavier', 'red', 'rectangle', 'soft', 'heavier'), (
         'blue-square-hard-heavier', 'blue', 'square', 'hard', 'heavier'), (
           'blue-rectangle-soft-medium', 'blue', 'rectangle', 'soft', 'medium'), (
             'white-square-hard-medium', 'white', 'square', 'hard', 'medium'), (
               'yellow-circle-hard-heavier', 'yellow', 'circle', 'hard', 'heavier'), (
                 'white-pentagon-soft-lighter', 'white', 'pentagon', 'soft', 'lighter'), (
                   'red-square-firm-heavier', 'red', 'square', 'firm', 'heavier'), (
                     'red-square-firm-heavy', 'red', 'square', 'firm', 'heavy'),
  ('white-circle-smooth-light', 'white', 'circle', 'smooth', 'light'), (
    'yellow-rectangle-firm-heavier', 'yellow', 'rectangle', 'firm', 'heavier'), (
      'green-pentagon-rough-lighter', 'green', 'pentagon', 'rough',
      'lighter'), ('red-rectangle-rough-medium', 'red', 'rectangle', 'rough', 'medium'), (
        'white-pentagon-firm-heavy', 'white', 'pentagon', 'firm', 'heavy'), (
          'red-pentagon-hard-light', 'red', 'pentagon', 'hard', 'light'), (
            'green-pentagon-smooth-medium', 'green', 'pentagon', 'smooth', 'medium'), (
              'yellow-oval-smooth-lighter', 'yellow', 'oval', 'smooth', 'lighter'), (
                'white-oval-hard-heavier', 'white', 'oval', 'hard', 'heavier'), (
                  'yellow-oval-hard-light', 'yellow', 'oval', 'hard', 'light'), (
                    'yellow-square-hard-heavier', 'yellow', 'square', 'hard', 'heavier'),
  ('red-rectangle-smooth-heavier', 'red', 'rectangle', 'smooth', 'heavier'), (
    'green-circle-rough-lighter', 'green', 'circle', 'rough',
    'lighter'), ('white-oval-rough-light', 'white', 'oval', 'rough', 'light'), (
      'white-rectangle-rough-heavier', 'white', 'rectangle', 'rough',
      'heavier'), ('red-oval-rough-heavy', 'red', 'oval', 'rough', 'heavy'), (
        'green-rectangle-firm-heavy', 'green', 'rectangle', 'firm',
        'heavy'), ('blue-oval-rough-heavier', 'blue', 'oval', 'rough', 'heavier'), (
          'blue-rectangle-hard-heavier', 'blue', 'rectangle', 'hard', 'heavier'), (
            'green-rectangle-hard-lighter', 'green', 'rectangle', 'hard',
            'lighter'), ('white-square-firm-heavy', 'white', 'square', 'firm', 'heavy'), (
              'blue-pentagon-smooth-light', 'blue', 'pentagon', 'smooth', 'light'), (
                'yellow-oval-rough-light', 'yellow', 'oval', 'rough', 'light'), (
                  'yellow-oval-firm-light', 'yellow', 'oval', 'firm', 'light'), (
                    'yellow-circle-firm-medium', 'yellow', 'circle', 'firm', 'medium'), (
                      'white-oval-smooth-heavier', 'white', 'oval', 'smooth', 'heavier'),
  ('green-rectangle-hard-heavy', 'green', 'rectangle',
   'hard', 'heavy'), ('red-circle-hard-heavier', 'red', 'circle', 'hard', 'heavier'), (
     'red-oval-firm-lighter', 'red', 'oval', 'firm',
     'lighter'), ('red-circle-hard-light', 'red', 'circle', 'hard', 'light'), (
       'white-pentagon-hard-medium', 'white', 'pentagon', 'hard',
       'medium'), ('red-pentagon-rough-medium', 'red', 'pentagon', 'rough', 'medium'), (
         'red-square-hard-medium', 'red', 'square', 'hard',
         'medium'), ('white-square-soft-heavy', 'white', 'square', 'soft', 'heavy'), (
           'green-circle-soft-lighter', 'green', 'circle', 'soft',
           'lighter'), ('red-square-firm-medium', 'red', 'square', 'firm', 'medium'), (
             'green-circle-smooth-lighter', 'green', 'circle', 'smooth',
             'lighter'), ('red-oval-rough-lighter', 'red', 'oval', 'rough', 'lighter'), (
               'green-circle-firm-medium', 'green', 'circle', 'firm', 'medium'), (
                 'green-circle-soft-lighter', 'green', 'circle', 'soft', 'lighter'), (
                   'green-oval-smooth-lighter', 'green', 'oval', 'smooth', 'lighter'), (
                     'red-oval-firm-medium', 'red', 'oval', 'firm', 'medium'), (
                       'red-square-firm-heavier', 'red', 'square', 'firm', 'heavier'), (
                         'yellow-circle-soft-heavy', 'yellow', 'circle', 'soft', 'heavy'),
  ('yellow-pentagon-hard-medium', 'yellow', 'pentagon', 'hard',
   'medium'), ('white-rectangle-rough-light', 'white', 'rectangle', 'rough', 'light'), (
     'yellow-circle-smooth-heavier', 'yellow', 'circle', 'smooth',
     'heavier'), ('red-pentagon-soft-heavier', 'red', 'pentagon', 'soft', 'heavier'), (
       'blue-square-smooth-medium', 'blue', 'square', 'smooth',
       'medium'), ('white-circle-firm-medium', 'white', 'circle', 'firm', 'medium'), (
         'green-square-firm-heavier', 'green', 'square', 'firm',
         'heavier'), ('red-circle-soft-lighter', 'red', 'circle', 'soft', 'lighter'), (
           'white-rectangle-rough-medium', 'white', 'rectangle', 'rough',
           'medium'), ('red-square-hard-heavier', 'red', 'square', 'hard', 'heavier'), (
             'green-pentagon-soft-lighter', 'green', 'pentagon', 'soft', 'lighter'), (
               'white-circle-smooth-heavy', 'white', 'circle', 'smooth', 'heavy'), (
                 'white-square-firm-heavy', 'white', 'square', 'firm', 'heavy'), (
                   'yellow-pentagon-hard-medium', 'yellow', 'pentagon', 'hard',
                   'medium'), ('red-square-hard-light', 'red', 'square', 'hard', 'light'),
  ('white-pentagon-rough-medium', 'white', 'pentagon', 'rough',
   'medium'), ('yellow-square-firm-medium', 'yellow', 'square', 'firm', 'medium'), (
     'white-square-smooth-light', 'white', 'square', 'smooth',
     'light'), ('blue-pentagon-soft-lighter', 'blue', 'pentagon', 'soft', 'lighter'), (
       'green-oval-smooth-heavy', 'green', 'oval', 'smooth',
       'heavy'), ('red-pentagon-rough-light', 'red', 'pentagon', 'rough', 'light'), (
         'yellow-circle-soft-light', 'yellow', 'circle', 'soft', 'light'), (
           'blue-circle-firm-light', 'blue', 'circle', 'firm', 'light'), (
             'green-oval-soft-heavy', 'green', 'oval', 'soft', 'heavy'), (
               'blue-square-firm-heavier', 'blue', 'square', 'firm', 'heavier'), (
                 'blue-rectangle-smooth-heavy', 'blue', 'rectangle', 'smooth', 'heavy'), (
                   'blue-pentagon-firm-medium', 'blue', 'pentagon', 'firm', 'medium'), (
                     'yellow-circle-soft-light', 'yellow', 'circle', 'soft', 'light'), (
                       'red-square-smooth-light', 'red', 'square', 'smooth', 'light'), (
                         'green-circle-rough-heavy', 'green', 'circle', 'rough', 'heavy'),
  ('yellow-rectangle-rough-lighter', 'yellow', 'rectangle', 'rough', 'lighter'), (
    'blue-circle-smooth-medium', 'blue', 'circle', 'smooth',
    'medium'), ('yellow-rectangle-firm-heavy', 'yellow', 'rectangle', 'firm', 'heavy'), (
      'yellow-oval-soft-lighter', 'yellow', 'oval', 'soft', 'lighter'), (
        'red-circle-hard-medium', 'red', 'circle', 'hard', 'medium'), (
          'green-oval-rough-heavier', 'green', 'oval', 'rough', 'heavier'), (
            'yellow-pentagon-rough-medium', 'yellow', 'pentagon', 'rough', 'medium'), (
              'yellow-square-soft-heavy', 'yellow', 'square', 'soft', 'heavy'), (
                'blue-oval-smooth-lighter', 'blue', 'oval', 'smooth', 'lighter'), (
                  'red-square-smooth-lighter', 'red', 'square', 'smooth', 'lighter'), (
                    'blue-rectangle-soft-medium', 'blue', 'rectangle', 'soft', 'medium'),
  ('white-circle-hard-heavy', 'white', 'circle', 'hard', 'heavy'), (
    'green-pentagon-hard-lighter', 'green', 'pentagon', 'hard',
    'lighter'), ('red-rectangle-soft-heavier', 'red', 'rectangle', 'soft', 'heavier'), (
      'red-square-hard-heavier', 'red', 'square', 'hard',
      'heavier'), ('blue-pentagon-soft-medium', 'blue', 'pentagon', 'soft', 'medium'), (
        'green-rectangle-rough-medium', 'green', 'rectangle', 'rough', 'medium'), (
          'blue-oval-rough-medium', 'blue', 'oval', 'rough', 'medium'), (
            'white-oval-hard-medium', 'white', 'oval', 'hard', 'medium'), (
              'red-oval-soft-heavy', 'red', 'oval', 'soft', 'heavy'), (
                'yellow-pentagon-smooth-heavier', 'yellow', 'pentagon', 'smooth',
                'heavier'), ('red-oval-firm-medium', 'red', 'oval', 'firm', 'medium'), (
                  'white-square-firm-heavier', 'white', 'square', 'firm', 'heavier'), (
                    'white-oval-rough-light', 'white', 'oval', 'rough', 'light'), (
                      'white-oval-smooth-light', 'white', 'oval', 'smooth', 'light'), (
                        'blue-oval-smooth-medium', 'blue', 'oval', 'smooth', 'medium'), (
                          'yellow-oval-soft-heavy', 'yellow', 'oval', 'soft', 'heavy'), (
                            'blue-oval-firm-lighter', 'blue', 'oval', 'firm', 'lighter'),
  ('white-circle-hard-medium', 'white', 'circle', 'hard', 'medium'), (
    'red-pentagon-hard-medium', 'red', 'pentagon', 'hard',
    'medium'), ('green-circle-soft-heavy', 'green', 'circle', 'soft', 'heavy'), (
      'red-rectangle-rough-light', 'red', 'rectangle', 'rough',
      'light'), ('blue-circle-smooth-lighter', 'blue', 'circle', 'smooth', 'lighter'), (
        'red-pentagon-rough-lighter', 'red', 'pentagon', 'rough',
        'lighter'), ('green-square-rough-light', 'green', 'square', 'rough', 'light'), (
          'yellow-oval-firm-light', 'yellow', 'oval', 'firm', 'light'), (
            'white-square-firm-heavy', 'white', 'square', 'firm', 'heavy'), (
              'red-oval-smooth-heavy', 'red', 'oval', 'smooth', 'heavy'), (
                'yellow-pentagon-hard-heavy', 'yellow', 'pentagon', 'hard', 'heavy'), (
                  'yellow-rectangle-soft-heavier', 'yellow', 'rectangle', 'soft',
                  'heavier'), ('blue-oval-firm-heavy', 'blue', 'oval', 'firm', 'heavy'), (
                    'blue-square-hard-lighter', 'blue', 'square', 'hard', 'lighter'), (
                      'red-circle-rough-heavier', 'red', 'circle', 'rough', 'heavier'), (
                        'blue-square-rough-heavy', 'blue', 'square', 'rough', 'heavy'),
  ('yellow-rectangle-hard-heavy', 'yellow', 'rectangle', 'hard',
   'heavy'), ('red-pentagon-hard-lighter', 'red', 'pentagon', 'hard', 'lighter'), (
     'yellow-circle-hard-light', 'yellow', 'circle', 'hard',
     'light'), ('green-pentagon-rough-light', 'green', 'pentagon', 'rough', 'light'), (
       'yellow-circle-soft-lighter', 'yellow', 'circle', 'soft',
       'lighter'), ('yellow-oval-hard-heavier', 'yellow', 'oval', 'hard', 'heavier'), (
         'red-square-rough-light', 'red', 'square', 'rough', 'light'), (
           'green-rectangle-firm-heavier', 'green', 'rectangle', 'firm',
           'heavier'), ('red-square-rough-light', 'red', 'square', 'rough', 'light'), (
             'green-rectangle-soft-heavy', 'green', 'rectangle', 'soft', 'heavy'), (
               'yellow-square-smooth-lighter', 'yellow', 'square', 'smooth',
               'lighter'), ('red-oval-hard-medium', 'red', 'oval', 'hard', 'medium'), (
                 'yellow-square-firm-heavy', 'yellow', 'square', 'firm', 'heavy'), (
                   'yellow-square-firm-heavier', 'yellow', 'square', 'firm', 'heavier'), (
                     'blue-pentagon-firm-heavy', 'blue', 'pentagon', 'firm', 'heavy'), (
                       'white-circle-soft-lighter', 'white', 'circle', 'soft', 'lighter'),
  ('white-oval-smooth-heavy', 'white', 'oval', 'smooth',
   'heavy'), ('yellow-rectangle-soft-light', 'yellow', 'rectangle', 'soft', 'light'), (
     'green-rectangle-rough-heavy', 'green', 'rectangle', 'rough',
     'heavy'), ('yellow-circle-rough-light', 'yellow', 'circle', 'rough', 'light'), (
       'green-pentagon-rough-heavy', 'green', 'pentagon', 'rough',
       'heavy'), ('red-circle-smooth-heavy', 'red', 'circle', 'smooth', 'heavy'), (
         'white-rectangle-smooth-lighter', 'white', 'rectangle', 'smooth',
         'lighter'), ('white-circle-firm-heavy', 'white', 'circle', 'firm', 'heavy'), (
           'blue-rectangle-rough-heavier', 'blue', 'rectangle', 'rough', 'heavier'), (
             'red-pentagon-smooth-lighter', 'red', 'pentagon', 'smooth', 'lighter'), (
               'white-pentagon-smooth-medium', 'white', 'pentagon', 'smooth', 'medium'), (
                 'blue-circle-soft-medium', 'blue', 'circle', 'soft', 'medium'), (
                   'yellow-rectangle-smooth-light', 'yellow', 'rectangle', 'smooth',
                   'light'), ('blue-oval-soft-heavy', 'blue', 'oval', 'soft', 'heavy'),
  ('blue-rectangle-smooth-lighter', 'blue', 'rectangle', 'smooth', 'lighter'), (
    'yellow-rectangle-smooth-medium', 'yellow', 'rectangle', 'smooth',
    'medium'), ('blue-pentagon-rough-light', 'blue', 'pentagon', 'rough', 'light'), (
      'yellow-oval-hard-heavier', 'yellow', 'oval', 'hard',
      'heavier'), ('white-square-smooth-light', 'white', 'square', 'smooth', 'light'), (
        'green-rectangle-soft-heavy', 'green', 'rectangle', 'soft', 'heavy'), (
          'yellow-square-soft-medium', 'yellow', 'square', 'soft', 'medium'), (
            'yellow-rectangle-soft-lighter', 'yellow', 'rectangle', 'soft', 'lighter'), (
              'white-square-hard-medium', 'white', 'square', 'hard', 'medium'), (
                'blue-circle-firm-light', 'blue', 'circle', 'firm', 'light'), (
                  'blue-oval-soft-heavier', 'blue', 'oval', 'soft', 'heavier'), (
                    'red-rectangle-firm-heavy', 'red', 'rectangle', 'firm', 'heavy'), (
                      'red-rectangle-soft-heavy', 'red', 'rectangle', 'soft', 'heavy'), (
                        'green-rectangle-smooth-heavy', 'green', 'rectangle', 'smooth',
                        'heavy'), ('blue-square-firm-lighter', 'blue', 'square', 'firm',
                                   'lighter'), ('green-rectangle-soft-medium', 'green',
                                                'rectangle', 'soft', 'medium'),
  ('white-circle-rough-heavy', 'white', 'circle', 'rough',
   'heavy'), ('green-square-rough-heavy', 'green', 'square', 'rough', 'heavy'), (
     'red-oval-rough-heavier', 'red', 'oval', 'rough', 'heavier'), (
       'yellow-square-firm-heavier', 'yellow', 'square', 'firm', 'heavier'), (
         'yellow-pentagon-firm-light', 'yellow', 'pentagon', 'firm', 'light'), (
           'blue-rectangle-rough-heavier', 'blue', 'rectangle', 'rough', 'heavier'), (
             'white-circle-smooth-heavy', 'white', 'circle', 'smooth', 'heavy'), (
               'yellow-circle-firm-light', 'yellow', 'circle', 'firm', 'light'), (
                 'white-oval-hard-heavy', 'white', 'oval', 'hard', 'heavy'), (
                   'green-square-firm-heavy', 'green', 'square', 'firm', 'heavy'), (
                     'red-circle-smooth-medium', 'red', 'circle', 'smooth', 'medium'), (
                       'yellow-oval-smooth-light', 'yellow', 'oval', 'smooth', 'light'), (
                         'yellow-square-soft-light', 'yellow', 'square', 'soft', 'light'),
  ('blue-rectangle-rough-light', 'blue', 'rectangle', 'rough',
   'light'), ('red-circle-soft-heavy', 'red', 'circle', 'soft', 'heavy'), (
     'red-pentagon-firm-light', 'red', 'pentagon', 'firm',
     'light'), ('white-oval-firm-lighter', 'white', 'oval', 'firm', 'lighter'), (
       'white-square-hard-lighter', 'white', 'square', 'hard', 'lighter'), (
         'yellow-pentagon-soft-heavier', 'yellow', 'pentagon', 'soft',
         'heavier'), ('red-square-firm-lighter', 'red', 'square', 'firm', 'lighter'), (
           'red-circle-soft-medium', 'red', 'circle', 'soft', 'medium'), (
             'white-rectangle-smooth-medium', 'white', 'rectangle', 'smooth',
             'medium'), ('red-oval-soft-light', 'red', 'oval', 'soft', 'light'), (
               'blue-pentagon-hard-heavy', 'blue', 'pentagon', 'hard', 'heavy'), (
                 'yellow-circle-hard-heavier', 'yellow', 'circle', 'hard', 'heavier'), (
                   'yellow-circle-soft-heavier', 'yellow', 'circle', 'soft', 'heavier'), (
                     'white-oval-rough-medium', 'white', 'oval', 'rough', 'medium'), (
                       'red-circle-soft-heavy', 'red', 'circle', 'soft', 'heavy'), (
                         'yellow-rectangle-rough-heavy', 'yellow', 'rectangle', 'rough',
                         'heavy'), ('green-square-rough-lighter', 'green', 'square',
                                    'rough', 'lighter'),
  ('white-circle-hard-light', 'white', 'circle', 'hard',
   'light'), ('white-rectangle-firm-heavy', 'white', 'rectangle', 'firm', 'heavy'), (
     'green-rectangle-smooth-heavier', 'green', 'rectangle', 'smooth',
     'heavier'), ('red-pentagon-smooth-light', 'red', 'pentagon', 'smooth', 'light'), (
       'red-square-firm-medium', 'red', 'square', 'firm', 'medium'), (
         'red-oval-rough-medium', 'red', 'oval', 'rough', 'medium'), (
           'white-rectangle-firm-medium', 'white', 'rectangle', 'firm', 'medium'), (
             'yellow-square-soft-heavier', 'yellow', 'square', 'soft', 'heavier'), (
               'red-circle-firm-heavy', 'red', 'circle', 'firm', 'heavy'), (
                 'white-pentagon-firm-heavier', 'white', 'pentagon', 'firm', 'heavier'), (
                   'blue-square-smooth-medium', 'blue', 'square', 'smooth', 'medium'),
  ('yellow-circle-rough-lighter', 'yellow', 'circle', 'rough', 'lighter'), (
    'blue-rectangle-smooth-lighter', 'blue', 'rectangle', 'smooth', 'lighter'), (
      'white-pentagon-hard-heavier', 'white', 'pentagon', 'hard', 'heavier'), (
        'blue-rectangle-smooth-light', 'blue', 'rectangle', 'smooth', 'light'), (
          'red-oval-soft-lighter', 'red', 'oval', 'soft', 'lighter'), (
            'yellow-oval-rough-heavier', 'yellow', 'oval', 'rough', 'heavier'), (
              'yellow-rectangle-smooth-medium', 'yellow', 'rectangle', 'smooth',
              'medium'), ('red-circle-rough-heavy', 'red', 'circle', 'rough', 'heavy'), (
                'green-pentagon-firm-lighter', 'green', 'pentagon', 'firm', 'lighter'), (
                  'red-square-soft-heavy', 'red', 'square', 'soft', 'heavy'), (
                    'yellow-rectangle-hard-heavier', 'yellow', 'rectangle', 'hard',
                    'heavier'), ('blue-pentagon-firm-light', 'blue', 'pentagon', 'firm',
                                 'light'), ('white-oval-firm-medium', 'white', 'oval',
                                            'firm', 'medium'),
  ('blue-rectangle-soft-heavy', 'blue', 'rectangle', 'soft',
   'heavy'), ('red-square-soft-medium', 'red', 'square', 'soft', 'medium'), (
     'white-circle-hard-heavy', 'white', 'circle', 'hard',
     'heavy'), ('red-circle-rough-heavier', 'red', 'circle', 'rough', 'heavier'), (
       'yellow-circle-hard-lighter', 'yellow', 'circle', 'hard',
       'lighter'), ('blue-circle-hard-heavy', 'blue', 'circle', 'hard', 'heavy'), (
         'blue-square-soft-lighter', 'blue', 'square', 'soft',
         'lighter'), ('blue-square-rough-light', 'blue', 'square', 'rough', 'light'), (
           'green-rectangle-firm-heavy', 'green', 'rectangle', 'firm', 'heavy'), (
             'white-rectangle-rough-medium', 'white', 'rectangle', 'rough',
             'medium'), ('green-square-firm-heavy', 'green', 'square', 'firm', 'heavy'), (
               'yellow-square-smooth-heavier', 'yellow', 'square', 'smooth', 'heavier'), (
                 'yellow-oval-smooth-heavy', 'yellow', 'oval', 'smooth', 'heavy'), (
                   'green-square-smooth-medium', 'green', 'square', 'smooth', 'medium'), (
                     'blue-oval-smooth-lighter', 'blue', 'oval', 'smooth', 'lighter'), (
                       'white-square-hard-heavy', 'white', 'square', 'hard', 'heavy'), (
                         'red-rectangle-firm-light', 'red', 'rectangle', 'firm', 'light'),
  ('red-pentagon-soft-heavy', 'red', 'pentagon', 'soft',
   'heavy'), ('blue-pentagon-firm-medium', 'blue', 'pentagon', 'firm', 'medium'), (
     'red-circle-smooth-medium', 'red', 'circle', 'smooth',
     'medium'), ('red-pentagon-hard-heavy', 'red', 'pentagon', 'hard', 'heavy'), (
       'green-square-soft-lighter', 'green', 'square', 'soft',
       'lighter'), ('blue-square-smooth-light', 'blue', 'square', 'smooth', 'light'), (
         'white-square-smooth-lighter', 'white', 'square', 'smooth',
         'lighter'), ('yellow-circle-soft-heavy', 'yellow', 'circle', 'soft', 'heavy'), (
           'blue-square-rough-lighter', 'blue', 'square', 'rough', 'lighter'), (
             'white-pentagon-firm-light', 'white', 'pentagon', 'firm', 'light'), (
               'blue-pentagon-rough-lighter', 'blue', 'pentagon', 'rough', 'lighter'), (
                 'blue-circle-rough-light', 'blue', 'circle', 'rough', 'light'), (
                   'white-rectangle-hard-medium', 'white', 'rectangle', 'hard', 'medium'),
  ('blue-square-rough-heavy', 'blue', 'square', 'rough', 'heavy'), (
    'green-circle-soft-light', 'green', 'circle', 'soft',
    'light'), ('white-oval-smooth-light', 'white', 'oval', 'smooth', 'light'), (
      'blue-pentagon-soft-heavier', 'blue', 'pentagon', 'soft',
      'heavier'), ('red-oval-hard-lighter', 'red', 'oval', 'hard', 'lighter'), (
        'red-rectangle-smooth-lighter', 'red', 'rectangle', 'smooth',
        'lighter'), ('red-circle-firm-heavy', 'red', 'circle', 'firm', 'heavy'), (
          'blue-oval-rough-heavy', 'blue', 'oval', 'rough', 'heavy'), (
            'red-circle-rough-light', 'red', 'circle', 'rough', 'light'), (
              'red-pentagon-soft-heavier', 'red', 'pentagon', 'soft', 'heavier'), (
                'blue-square-smooth-light', 'blue', 'square', 'smooth', 'light'), (
                  'yellow-rectangle-smooth-medium', 'yellow', 'rectangle', 'smooth',
                  'medium'), ('blue-rectangle-rough-light', 'blue', 'rectangle', 'rough',
                              'light'), ('yellow-rectangle-smooth-heavier', 'yellow',
                                         'rectangle', 'smooth', 'heavier'),
  ('blue-oval-firm-medium', 'blue', 'oval', 'firm', 'medium'), (
    'yellow-circle-firm-heavy', 'yellow', 'circle', 'firm', 'heavy'), (
      'yellow-rectangle-firm-medium', 'yellow', 'rectangle', 'firm',
      'medium'), ('yellow-oval-rough-medium', 'yellow', 'oval', 'rough', 'medium'), (
        'red-square-firm-heavy', 'red', 'square', 'firm', 'heavy'), (
          'white-pentagon-rough-medium', 'white', 'pentagon', 'rough',
          'medium'), ('red-oval-hard-lighter', 'red', 'oval', 'hard', 'lighter'), (
            'red-pentagon-hard-heavier', 'red', 'pentagon', 'hard', 'heavier'), (
              'white-pentagon-smooth-heavy', 'white', 'pentagon', 'smooth', 'heavy'), (
                'blue-square-firm-medium', 'blue', 'square', 'firm', 'medium'), (
                  'green-rectangle-smooth-heavy', 'green', 'rectangle', 'smooth',
                  'heavy'), ('red-square-hard-light', 'red', 'square', 'hard', 'light'), (
                    'red-square-hard-lighter', 'red', 'square', 'hard', 'lighter'), (
                      'blue-rectangle-rough-lighter', 'blue', 'rectangle', 'rough',
                      'lighter'), (
                        'blue-oval-hard-heavy', 'blue', 'oval', 'hard', 'heavy'), (
                          'blue-square-firm-heavy', 'blue', 'square', 'firm', 'heavy'), (
                            'red-oval-soft-heavier', 'red', 'oval', 'soft', 'heavier'), (
                              'yellow-pentagon-rough-light', 'yellow', 'pentagon',
                              'rough', 'light'), ('blue-pentagon-soft-light', 'blue',
                                                  'pentagon', 'soft', 'light'),
  ('white-square-soft-heavy', 'white', 'square', 'soft', 'heavy'), (
    'red-rectangle-rough-medium', 'red', 'rectangle', 'rough', 'medium'), (
      'yellow-pentagon-firm-lighter', 'yellow', 'pentagon', 'firm',
      'lighter'), ('yellow-square-rough-light', 'yellow', 'square', 'rough', 'light'), (
        'white-rectangle-hard-medium', 'white', 'rectangle', 'hard',
        'medium'), ('blue-pentagon-soft-medium', 'blue', 'pentagon', 'soft', 'medium'), (
          'blue-oval-firm-lighter', 'blue', 'oval', 'firm',
          'lighter'), ('red-oval-soft-lighter', 'red', 'oval', 'soft', 'lighter'), (
            'yellow-rectangle-hard-heavy', 'yellow', 'rectangle', 'hard',
            'heavy'), ('red-oval-rough-heavy', 'red', 'oval', 'rough', 'heavy'), (
              'green-oval-firm-light', 'green', 'oval', 'firm', 'light'), (
                'yellow-rectangle-hard-heavy', 'yellow', 'rectangle', 'hard', 'heavy'), (
                  'green-oval-rough-heavier', 'green', 'oval', 'rough', 'heavier'),
  ('red-pentagon-firm-light', 'red', 'pentagon', 'firm', 'light'), (
    'yellow-circle-rough-lighter', 'yellow', 'circle', 'rough',
    'lighter'), ('yellow-circle-firm-heavier', 'yellow', 'circle', 'firm', 'heavier'), (
      'green-oval-rough-light', 'green', 'oval', 'rough',
      'light'), ('red-pentagon-firm-medium', 'red', 'pentagon', 'firm', 'medium'), (
        'green-rectangle-firm-heavier', 'green', 'rectangle', 'firm', 'heavier'), (
          'yellow-pentagon-smooth-medium', 'yellow', 'pentagon', 'smooth',
          'medium'), ('blue-square-firm-heavier', 'blue', 'square', 'firm', 'heavier'), (
            'blue-rectangle-rough-medium', 'blue', 'rectangle', 'rough', 'medium'), (
              'yellow-circle-rough-heavy', 'yellow', 'circle', 'rough', 'heavy'), (
                'red-pentagon-smooth-light', 'red', 'pentagon', 'smooth',
                'light'), ('red-oval-rough-medium', 'red', 'oval', 'rough', 'medium'), (
                  'white-rectangle-soft-light', 'white', 'rectangle', 'soft', 'light'), (
                    'red-square-soft-light', 'red', 'square', 'soft', 'light'), (
                      'green-pentagon-smooth-light', 'green', 'pentagon', 'smooth',
                      'light'), ('green-circle-firm-heavy', 'green', 'circle', 'firm',
                                 'heavy'), ('white-oval-firm-light', 'white', 'oval',
                                            'firm', 'light'),
  ('green-rectangle-smooth-light', 'green', 'rectangle', 'smooth',
   'light'), ('yellow-circle-hard-medium', 'yellow', 'circle', 'hard', 'medium'), (
     'red-oval-hard-heavy', 'red', 'oval', 'hard',
     'heavy'), ('white-pentagon-rough-medium', 'white', 'pentagon', 'rough', 'medium'), (
       'white-circle-rough-light', 'white', 'circle', 'rough',
       'light'), ('yellow-pentagon-soft-light', 'yellow', 'pentagon', 'soft', 'light'), (
         'white-pentagon-rough-lighter', 'white', 'pentagon', 'rough',
         'lighter'), ('green-circle-rough-heavy', 'green', 'circle', 'rough', 'heavy'), (
           'blue-square-smooth-lighter', 'blue', 'square', 'smooth',
           'lighter'), ('red-oval-smooth-light', 'red', 'oval', 'smooth', 'light'), (
             'red-pentagon-firm-medium', 'red', 'pentagon', 'firm',
             'medium'), ('white-oval-soft-medium', 'white', 'oval', 'soft', 'medium'), (
               'blue-oval-hard-heavier', 'blue', 'oval', 'hard', 'heavier'), (
                 'yellow-circle-rough-heavier', 'yellow', 'circle', 'rough', 'heavier'), (
                   'blue-circle-firm-medium', 'blue', 'circle', 'firm', 'medium'), (
                     'white-pentagon-smooth-medium', 'white', 'pentagon', 'smooth',
                     'medium'), ('green-pentagon-soft-light', 'green', 'pentagon', 'soft',
                                 'light'), ('white-square-hard-heavy', 'white', 'square',
                                            'hard', 'heavy'),
  ('yellow-rectangle-rough-lighter', 'yellow', 'rectangle', 'rough', 'lighter'), (
    'yellow-circle-smooth-light', 'yellow', 'circle', 'smooth',
    'light'), ('blue-rectangle-hard-lighter', 'blue', 'rectangle', 'hard', 'lighter'), (
      'yellow-square-rough-heavier', 'yellow', 'square', 'rough',
      'heavier'), ('blue-pentagon-soft-heavier', 'blue', 'pentagon', 'soft', 'heavier'), (
        'blue-circle-soft-heavy', 'blue', 'circle', 'soft',
        'heavy'), ('red-square-smooth-heavier', 'red', 'square', 'smooth', 'heavier'), (
          'blue-oval-soft-light', 'blue', 'oval', 'soft',
          'light'), ('green-square-smooth-light', 'green', 'square', 'smooth', 'light'), (
            'blue-square-soft-heavier', 'blue', 'square', 'soft', 'heavier'), (
              'blue-square-firm-lighter', 'blue', 'square', 'firm', 'lighter'), (
                'red-circle-rough-lighter', 'red', 'circle', 'rough', 'lighter'), (
                  'blue-square-rough-heavier', 'blue', 'square', 'rough', 'heavier'), (
                    'white-square-firm-heavy', 'white', 'square', 'firm', 'heavy'), (
                      'blue-circle-firm-heavy', 'blue', 'circle', 'firm', 'heavy'), (
                        'red-square-soft-medium', 'red', 'square', 'soft', 'medium'), (
                          'red-rectangle-smooth-heavy', 'red', 'rectangle', 'smooth',
                          'heavy'), ('white-square-hard-heavy', 'white', 'square', 'hard',
                                     'heavy'), ('blue-square-firm-heavy', 'blue',
                                                'square', 'firm', 'heavy'),
  ('white-circle-rough-lighter', 'white', 'circle', 'rough', 'lighter'), (
    'blue-pentagon-smooth-lighter', 'blue', 'pentagon', 'smooth',
    'lighter'), ('white-square-firm-lighter', 'white', 'square', 'firm', 'lighter'), (
      'blue-rectangle-hard-light', 'blue', 'rectangle', 'hard', 'light'), (
        'yellow-rectangle-soft-heavier', 'yellow', 'rectangle', 'soft',
        'heavier'), ('red-oval-smooth-medium', 'red', 'oval', 'smooth', 'medium'), (
          'white-rectangle-rough-heavy', 'white', 'rectangle', 'rough',
          'heavy'), ('blue-oval-rough-light', 'blue', 'oval', 'rough', 'light'), (
            'white-rectangle-rough-lighter', 'white', 'rectangle', 'rough', 'lighter'), (
              'green-circle-hard-medium', 'green', 'circle', 'hard', 'medium'), (
                'yellow-rectangle-hard-medium', 'yellow', 'rectangle', 'hard', 'medium'),
  ('green-circle-hard-lighter', 'green', 'circle', 'hard', 'lighter'), (
    'white-pentagon-rough-heavy', 'white', 'pentagon', 'rough',
    'heavy'), ('blue-pentagon-smooth-heavy', 'blue', 'pentagon', 'smooth', 'heavy'), (
      'blue-rectangle-soft-lighter', 'blue', 'rectangle', 'soft',
      'lighter'), ('red-circle-firm-medium', 'red', 'circle', 'firm', 'medium'), (
        'blue-circle-hard-heavier', 'blue', 'circle', 'hard',
        'heavier'), ('blue-circle-hard-medium', 'blue', 'circle', 'hard', 'medium'), (
          'white-pentagon-smooth-lighter', 'white', 'pentagon', 'smooth', 'lighter'), (
            'yellow-oval-soft-heavier', 'yellow', 'oval', 'soft', 'heavier'), (
              'blue-square-rough-lighter', 'blue', 'square', 'rough', 'lighter'), (
                'white-pentagon-hard-heavier', 'white', 'pentagon', 'hard', 'heavier'), (
                  'blue-square-firm-heavier', 'blue', 'square', 'firm', 'heavier'), (
                    'green-rectangle-smooth-lighter', 'green', 'rectangle', 'smooth',
                    'lighter'), ('white-pentagon-hard-light', 'white', 'pentagon', 'hard',
                                 'light'),
  ('white-pentagon-hard-lighter', 'white', 'pentagon', 'hard',
   'lighter'), ('white-oval-hard-medium', 'white', 'oval', 'hard', 'medium'), (
     'blue-rectangle-rough-light', 'blue', 'rectangle', 'rough',
     'light'), ('red-circle-rough-medium', 'red', 'circle', 'rough', 'medium'), (
       'green-circle-hard-light', 'green', 'circle', 'hard',
       'light'), ('green-square-firm-heavier', 'green', 'square', 'firm', 'heavier'), (
         'red-rectangle-hard-heavy', 'red', 'rectangle', 'hard',
         'heavy'), ('blue-oval-soft-heavy', 'blue', 'oval', 'soft', 'heavy'), (
           'green-circle-firm-heavy', 'green', 'circle', 'firm',
           'heavy'), ('red-circle-smooth-medium', 'red', 'circle', 'smooth', 'medium'), (
             'white-pentagon-rough-light', 'white', 'pentagon', 'rough', 'light'), (
               'green-rectangle-soft-lighter', 'green', 'rectangle', 'soft', 'lighter'), (
                 'red-square-smooth-medium', 'red', 'square', 'smooth', 'medium'), (
                   'yellow-oval-rough-medium', 'yellow', 'oval', 'rough', 'medium'),
  ('blue-pentagon-rough-heavier', 'blue', 'pentagon', 'rough', 'heavier'), (
    'yellow-pentagon-soft-lighter', 'yellow', 'pentagon',
    'soft', 'lighter'), ('red-square-smooth-light', 'red', 'square', 'smooth', 'light'), (
      'red-circle-hard-medium', 'red', 'circle', 'hard',
      'medium'), ('red-circle-smooth-light', 'red', 'circle', 'smooth', 'light'), (
        'yellow-square-firm-lighter', 'yellow', 'square', 'firm',
        'lighter'), ('blue-square-soft-lighter', 'blue', 'square', 'soft', 'lighter'), (
          'red-square-firm-medium', 'red', 'square', 'firm', 'medium'), (
            'green-pentagon-firm-lighter', 'green', 'pentagon', 'firm',
            'lighter'), ('red-circle-soft-light', 'red', 'circle', 'soft', 'light'), (
              'yellow-circle-soft-light', 'yellow', 'circle', 'soft', 'light'), (
                'white-rectangle-rough-light', 'white', 'rectangle', 'rough', 'light'), (
                  'green-square-hard-light', 'green', 'square', 'hard', 'light'), (
                    'green-pentagon-rough-heavy', 'green', 'pentagon', 'rough',
                    'heavy'), ('green-rectangle-hard-medium', 'green', 'rectangle',
                               'hard', 'medium'), ('red-circle-rough-lighter', 'red',
                                                   'circle', 'rough', 'lighter'),
  ('white-rectangle-rough-medium', 'white', 'rectangle', 'rough', 'medium'), (
    'green-square-rough-heavier', 'green', 'square', 'rough',
    'heavier'), ('red-rectangle-firm-heavy', 'red', 'rectangle', 'firm', 'heavy'), (
      'red-oval-rough-lighter', 'red', 'oval', 'rough',
      'lighter'), ('white-circle-hard-lighter', 'white', 'circle', 'hard', 'lighter'), (
        'yellow-circle-rough-light', 'yellow', 'circle', 'rough',
        'light'), ('white-circle-rough-heavy', 'white', 'circle', 'rough', 'heavy'), (
          'blue-rectangle-rough-light', 'blue', 'rectangle', 'rough',
          'light'), ('yellow-oval-smooth-light', 'yellow', 'oval', 'smooth', 'light'), (
            'yellow-rectangle-smooth-lighter', 'yellow', 'rectangle', 'smooth',
            'lighter'), ('yellow-pentagon-rough-medium', 'yellow', 'pentagon', 'rough',
                         'medium'), ('yellow-pentagon-hard-lighter', 'yellow', 'pentagon',
                                     'hard', 'lighter'), ('red-oval-hard-heavier', 'red',
                                                          'oval', 'hard', 'heavier'),
  ('blue-oval-rough-medium', 'blue', 'oval', 'rough', 'medium'), (
    'green-rectangle-soft-light', 'green', 'rectangle', 'soft',
    'light'), ('yellow-circle-rough-light', 'yellow', 'circle', 'rough', 'light'), (
      'blue-oval-rough-lighter', 'blue', 'oval', 'rough',
      'lighter'), ('white-square-firm-heavy', 'white', 'square', 'firm', 'heavy'), (
        'green-pentagon-smooth-heavier', 'green', 'pentagon', 'smooth', 'heavier'), (
          'green-rectangle-smooth-heavy', 'green', 'rectangle', 'smooth',
          'heavy'), ('blue-circle-soft-heavier', 'blue', 'circle', 'soft', 'heavier'), (
            'green-oval-rough-heavier', 'green', 'oval', 'rough', 'heavier'), (
              'green-circle-firm-light', 'green', 'circle', 'firm', 'light'), (
                'green-pentagon-firm-medium', 'green', 'pentagon', 'firm', 'medium'), (
                  'green-pentagon-firm-light', 'green', 'pentagon', 'firm', 'light'), (
                    'yellow-rectangle-rough-heavier', 'yellow', 'rectangle', 'rough',
                    'heavier'), ('yellow-square-rough-light', 'yellow', 'square', 'rough',
                                 'light'), ('green-pentagon-smooth-heavier', 'green',
                                            'pentagon', 'smooth', 'heavier'),
  ('red-square-firm-heavier', 'red', 'square', 'firm', 'heavier'), (
    'white-circle-smooth-light', 'white', 'circle', 'smooth',
    'light'), ('yellow-oval-firm-lighter', 'yellow', 'oval', 'firm', 'lighter'), (
      'green-rectangle-firm-lighter', 'green', 'rectangle', 'firm',
      'lighter'), ('yellow-oval-rough-lighter', 'yellow', 'oval', 'rough', 'lighter'), (
        'blue-rectangle-rough-medium', 'blue', 'rectangle', 'rough',
        'medium'), ('blue-square-smooth-heavy', 'blue', 'square', 'smooth', 'heavy'), (
          'yellow-rectangle-soft-light', 'yellow', 'rectangle', 'soft',
          'light'), ('red-square-hard-medium', 'red', 'square', 'hard', 'medium'), (
            'yellow-square-hard-medium', 'yellow', 'square', 'hard', 'medium'), (
              'red-rectangle-firm-heavy', 'red', 'rectangle', 'firm', 'heavy'), (
                'yellow-circle-hard-heavy', 'yellow', 'circle', 'hard', 'heavy'), (
                  'blue-circle-firm-light', 'blue', 'circle', 'firm', 'light'), (
                    'red-rectangle-rough-heavier', 'red', 'rectangle', 'rough',
                    'heavier'), ('blue-pentagon-hard-lighter', 'blue', 'pentagon', 'hard',
                                 'lighter'), ('yellow-square-smooth-light', 'yellow',
                                              'square', 'smooth', 'light'), (
                                                'red-square-smooth-medium', 'red',
                                                'square', 'smooth', 'medium'),
  ('green-rectangle-rough-heavy', 'green', 'rectangle', 'rough', 'heavy'), (
    'red-square-smooth-heavier', 'red', 'square', 'smooth',
    'heavier'), ('green-circle-smooth-light', 'green', 'circle', 'smooth', 'light'), (
      'white-oval-smooth-lighter', 'white', 'oval', 'smooth',
      'lighter'), ('blue-circle-firm-heavier', 'blue', 'circle', 'firm', 'heavier'), (
        'green-circle-rough-lighter', 'green', 'circle', 'rough',
        'lighter'), ('red-pentagon-soft-light', 'red', 'pentagon', 'soft', 'light'), (
          'blue-oval-firm-medium', 'blue', 'oval', 'firm',
          'medium'), ('white-square-rough-heavy', 'white', 'square', 'rough', 'heavy'), (
            'blue-circle-firm-light', 'blue', 'circle', 'firm', 'light'), (
              'red-square-smooth-medium', 'red', 'square', 'smooth', 'medium'), (
                'white-square-firm-heavy', 'white', 'square', 'firm', 'heavy'), (
                  'red-rectangle-hard-lighter', 'red', 'rectangle', 'hard', 'lighter'), (
                    'yellow-oval-hard-light', 'yellow', 'oval', 'hard', 'light'), (
                      'yellow-pentagon-smooth-medium', 'yellow', 'pentagon', 'smooth',
                      'medium'), ('yellow-circle-firm-medium', 'yellow', 'circle', 'firm',
                                  'medium'), ('red-pentagon-firm-heavy', 'red',
                                              'pentagon', 'firm', 'heavy'),
  ('green-rectangle-hard-light', 'green', 'rectangle', 'hard',
   'light'), ('white-square-rough-heavier', 'white', 'square', 'rough', 'heavier'), (
     'green-square-firm-light', 'green', 'square', 'firm', 'light'), (
       'yellow-rectangle-firm-lighter', 'yellow', 'rectangle', 'firm',
       'lighter'), ('red-oval-smooth-lighter', 'red', 'oval', 'smooth', 'lighter'), (
         'blue-circle-rough-light', 'blue', 'circle', 'rough',
         'light'), ('white-oval-soft-lighter', 'white', 'oval', 'soft', 'lighter'), (
           'yellow-oval-hard-light', 'yellow', 'oval', 'hard', 'light'), (
             'blue-rectangle-rough-medium', 'blue', 'rectangle', 'rough',
             'medium'), ('blue-square-rough-heavy', 'blue', 'square', 'rough', 'heavy'), (
               'green-square-smooth-heavier', 'green', 'square', 'smooth', 'heavier'), (
                 'yellow-rectangle-smooth-light', 'yellow', 'rectangle', 'smooth',
                 'light'), (
                   'yellow-oval-smooth-medium', 'yellow', 'oval', 'smooth', 'medium'), (
                     'blue-oval-hard-heavier', 'blue', 'oval', 'hard', 'heavier'), (
                       'white-oval-rough-lighter', 'white', 'oval', 'rough', 'lighter'), (
                         'white-square-rough-heavy', 'white', 'square', 'rough', 'heavy'),
  ('red-rectangle-smooth-light', 'red', 'rectangle', 'smooth',
   'light'), ('green-square-smooth-heavier', 'green', 'square', 'smooth', 'heavier'), (
     'red-oval-smooth-lighter', 'red', 'oval', 'smooth',
     'lighter'), ('green-pentagon-hard-heavy', 'green', 'pentagon', 'hard', 'heavy'), (
       'green-square-soft-heavier', 'green', 'square', 'soft',
       'heavier'), ('yellow-circle-firm-light', 'yellow', 'circle', 'firm', 'light'), (
         'blue-rectangle-soft-heavy', 'blue', 'rectangle', 'soft',
         'heavy'), ('white-square-rough-heavy', 'white', 'square', 'rough', 'heavy'), (
           'blue-oval-smooth-heavy', 'blue', 'oval', 'smooth',
           'heavy'), ('yellow-oval-rough-medium', 'yellow', 'oval', 'rough', 'medium'), (
             'blue-pentagon-rough-heavy', 'blue', 'pentagon', 'rough', 'heavy'), (
               'green-oval-rough-heavy', 'green', 'oval', 'rough', 'heavy'), (
                 'blue-circle-smooth-heavier', 'blue', 'circle', 'smooth', 'heavier'), (
                   'yellow-pentagon-rough-lighter', 'yellow', 'pentagon', 'rough',
                   'lighter'), (
                     'green-rectangle-firm-light', 'green', 'rectangle', 'firm',
                     'light'), ('yellow-pentagon-firm-lighter', 'yellow', 'pentagon',
                                'firm', 'lighter'), (
                                  'yellow-rectangle-soft-lighter', 'yellow', 'rectangle',
                                  'soft', 'lighter'), (
                                    'red-oval-rough-heavier', 'red', 'oval', 'rough',
                                    'heavier'), ('white-pentagon-smooth-medium', 'white',
                                                 'pentagon', 'smooth', 'medium'),
  ('red-square-smooth-heavier', 'red', 'square', 'smooth',
   'heavier'), ('green-square-rough-medium', 'green', 'square', 'rough', 'medium'), (
     'yellow-square-smooth-light', 'yellow', 'square', 'smooth',
     'light'), ('red-rectangle-firm-medium', 'red', 'rectangle', 'firm', 'medium'), (
       'yellow-circle-smooth-heavy', 'yellow', 'circle', 'smooth',
       'heavy'), ('white-pentagon-rough-light', 'white', 'pentagon', 'rough', 'light'), (
         'red-rectangle-firm-light', 'red', 'rectangle', 'firm',
         'light'), ('red-oval-rough-heavier', 'red', 'oval', 'rough', 'heavier'), (
           'white-rectangle-smooth-heavier', 'white', 'rectangle', 'smooth', 'heavier'), (
             'white-pentagon-firm-light', 'white', 'pentagon', 'firm', 'light'), (
               'green-square-rough-heavy', 'green', 'square', 'rough', 'heavy'), (
                 'white-square-firm-medium', 'white', 'square', 'firm', 'medium'), (
                   'green-circle-hard-medium', 'green', 'circle', 'hard', 'medium'), (
                     'green-circle-soft-lighter', 'green', 'circle', 'soft', 'lighter'), (
                       'green-circle-soft-medium', 'green', 'circle', 'soft', 'medium'), (
                         'red-pentagon-hard-medium', 'red', 'pentagon', 'hard', 'medium'),
  ('blue-rectangle-smooth-medium', 'blue', 'rectangle', 'smooth', 'medium'), (
    'white-square-rough-lighter', 'white', 'square', 'rough', 'lighter'), (
      'green-oval-firm-heavier', 'green', 'oval', 'firm',
      'heavier'), ('green-square-firm-medium', 'green', 'square', 'firm', 'medium'), (
        'white-circle-hard-heavier', 'white', 'circle', 'hard', 'heavier'), (
          'green-pentagon-hard-heavier', 'green', 'pentagon', 'hard', 'heavier'), (
            'yellow-square-smooth-heavier', 'yellow', 'square', 'smooth', 'heavier'), (
              'red-circle-firm-medium', 'red', 'circle', 'firm', 'medium'), (
                'blue-oval-rough-light', 'blue', 'oval', 'rough', 'light'), (
                  'blue-rectangle-soft-medium', 'blue', 'rectangle', 'soft', 'medium'), (
                    'yellow-rectangle-rough-medium', 'yellow', 'rectangle', 'rough',
                    'medium'), ('green-pentagon-hard-medium', 'green', 'pentagon', 'hard',
                                'medium'), ('yellow-oval-hard-light', 'yellow', 'oval',
                                            'hard', 'light'), (
                                              'white-rectangle-rough-lighter', 'white',
                                              'rectangle', 'rough', 'lighter'), (
                                                'yellow-rectangle-hard-medium', 'yellow',
                                                'rectangle', 'hard', 'medium'),
  ('green-rectangle-rough-light', 'green', 'rectangle', 'rough',
   'light'), ('yellow-pentagon-firm-heavy', 'yellow', 'pentagon', 'firm',
              'heavy'), ('green-square-smooth-medium', 'green', 'square', 'smooth',
                         'medium'), ('white-rectangle-hard-medium', 'white', 'rectangle',
                                     'hard', 'medium'), (
                                       'green-circle-firm-heavy', 'green', 'circle',
                                       'firm', 'heavy'), ('red-oval-hard-lighter', 'red',
                                                          'oval', 'hard', 'lighter'),
  ('white-rectangle-firm-light', 'white', 'rectangle', 'firm', 'light'), (
    'green-oval-smooth-heavy', 'green', 'oval', 'smooth',
    'heavy'), ('red-pentagon-hard-heavier', 'red', 'pentagon', 'hard', 'heavier'), (
      'yellow-oval-soft-light', 'yellow', 'oval', 'soft',
      'light'), ('green-circle-firm-light', 'green', 'circle', 'firm', 'light'), (
        'yellow-pentagon-firm-heavier', 'yellow', 'pentagon', 'firm', 'heavier'), (
          'yellow-square-rough-heavier', 'yellow', 'square', 'rough', 'heavier'), (
            'white-circle-firm-lighter', 'white', 'circle', 'firm', 'lighter'), (
              'green-oval-smooth-heavier', 'green', 'oval', 'smooth', 'heavier'), (
                'yellow-rectangle-smooth-light', 'yellow', 'rectangle', 'smooth',
                'light'), ('red-oval-hard-medium', 'red', 'oval', 'hard', 'medium'), (
                  'green-oval-rough-light', 'green', 'oval', 'rough', 'light'), (
                    'yellow-oval-smooth-light', 'yellow', 'oval', 'smooth',
                    'light'), ('blue-oval-soft-heavy', 'blue', 'oval', 'soft', 'heavy'), (
                      'white-pentagon-firm-lighter', 'white', 'pentagon', 'firm',
                      'lighter'), ('yellow-pentagon-firm-lighter', 'yellow', 'pentagon',
                                   'firm', 'lighter'), (
                                     'green-square-firm-lighter', 'green', 'square',
                                     'firm', 'lighter'), (
                                       'blue-circle-hard-heavy', 'blue', 'circle', 'hard',
                                       'heavy'), ('white-pentagon-hard-medium', 'white',
                                                  'pentagon', 'hard', 'medium'), (
                                                    'red-pentagon-hard-light', 'red',
                                                    'pentagon', 'hard', 'light'),
  ('blue-square-smooth-heavy', 'blue', 'square', 'smooth',
   'heavy'), ('yellow-pentagon-soft-medium', 'yellow', 'pentagon', 'soft',
              'medium'), ('white-oval-firm-medium', 'white', 'oval', 'firm', 'medium'), (
                'yellow-circle-soft-heavier', 'yellow', 'circle', 'soft', 'heavier'), (
                  'red-oval-hard-lighter', 'red', 'oval', 'hard', 'lighter'), (
                    'blue-pentagon-soft-heavy', 'blue', 'pentagon', 'soft', 'heavy'), (
                      'blue-circle-firm-medium', 'blue', 'circle', 'firm', 'medium'), (
                        'yellow-rectangle-firm-lighter', 'yellow', 'rectangle', 'firm',
                        'lighter'), ('blue-oval-hard-lighter', 'blue', 'oval', 'hard',
                                     'lighter'), ('white-oval-smooth-medium', 'white',
                                                  'oval', 'smooth', 'medium'),
  ('white-pentagon-hard-heavier', 'white', 'pentagon', 'hard', 'heavier'), (
    'white-rectangle-smooth-heavy', 'white', 'rectangle', 'smooth', 'heavy'), (
      'red-pentagon-soft-light', 'red', 'pentagon', 'soft',
      'light'), ('white-circle-firm-light', 'white', 'circle', 'firm', 'light'), (
        'yellow-square-rough-medium', 'yellow', 'square', 'rough', 'medium'), (
          'green-circle-smooth-medium', 'green', 'circle', 'smooth', 'medium'), (
            'yellow-rectangle-soft-heavier', 'yellow', 'rectangle', 'soft', 'heavier'), (
              'white-pentagon-smooth-light', 'white', 'pentagon', 'smooth', 'light'), (
                'red-square-hard-heavy', 'red', 'square', 'hard', 'heavy'), (
                  'blue-square-firm-heavy', 'blue', 'square', 'firm', 'heavy'), (
                    'blue-rectangle-hard-lighter', 'blue', 'rectangle', 'hard',
                    'lighter'), (
                      'white-oval-firm-heavy', 'white', 'oval', 'firm', 'heavy'), (
                        'red-square-firm-light', 'red', 'square', 'firm', 'light'), (
                          'red-pentagon-firm-heavy', 'red', 'pentagon', 'firm', 'heavy'),
  ('blue-oval-smooth-heavy', 'blue', 'oval', 'smooth',
   'heavy'), ('yellow-oval-hard-heavier', 'yellow', 'oval', 'hard', 'heavier'), (
     'red-square-soft-lighter', 'red', 'square', 'soft', 'lighter'), (
       'green-pentagon-smooth-heavy', 'green', 'pentagon', 'smooth', 'heavy'), (
         'yellow-pentagon-smooth-heavy', 'yellow', 'pentagon', 'smooth', 'heavy'), (
           'green-square-rough-heavier', 'green', 'square', 'rough', 'heavier'), (
             'blue-rectangle-firm-heavy', 'blue', 'rectangle', 'firm',
             'heavy'), ('green-square-firm-light', 'green', 'square', 'firm', 'light'), (
               'white-square-rough-lighter', 'white', 'square', 'rough', 'lighter'), (
                 'blue-rectangle-firm-heavier', 'blue', 'rectangle', 'firm', 'heavier'), (
                   'white-oval-rough-light', 'white', 'oval', 'rough', 'light'), (
                     'red-pentagon-soft-heavy', 'red', 'pentagon', 'soft', 'heavy'), (
                       'green-circle-rough-heavier', 'green', 'circle', 'rough',
                       'heavier'), ('red-rectangle-rough-light', 'red', 'rectangle',
                                    'rough', 'light'), ('red-circle-firm-heavy', 'red',
                                                        'circle', 'firm', 'heavy'),
  ('white-rectangle-smooth-medium', 'white', 'rectangle', 'smooth', 'medium'), (
    'green-square-smooth-lighter', 'green', 'square', 'smooth',
    'lighter'), ('red-circle-rough-medium', 'red', 'circle', 'rough', 'medium'), (
      'red-pentagon-hard-heavy', 'red', 'pentagon', 'hard',
      'heavy'), ('white-oval-hard-heavy', 'white', 'oval', 'hard', 'heavy'), (
        'blue-pentagon-hard-lighter', 'blue', 'pentagon', 'hard', 'lighter'), (
          'blue-pentagon-firm-lighter', 'blue', 'pentagon', 'firm', 'lighter'), (
            'green-rectangle-rough-light', 'green', 'rectangle', 'rough',
            'light'), ('red-circle-firm-light', 'red', 'circle', 'firm', 'light'), (
              'yellow-rectangle-hard-heavy', 'yellow', 'rectangle', 'hard', 'heavy'), (
                'red-rectangle-hard-lighter', 'red', 'rectangle', 'hard',
                'lighter'), ('blue-oval-soft-medium', 'blue', 'oval', 'soft', 'medium'), (
                  'red-pentagon-firm-heavier', 'red', 'pentagon', 'firm', 'heavier'), (
                    'green-pentagon-soft-heavier', 'green', 'pentagon', 'soft',
                    'heavier'), ('white-rectangle-smooth-light', 'white', 'rectangle',
                                 'smooth', 'light'), (
                                   'yellow-pentagon-hard-heavy', 'yellow', 'pentagon',
                                   'hard', 'heavy'), ('blue-pentagon-rough-heavy', 'blue',
                                                      'pentagon', 'rough', 'heavy'),
  ('yellow-pentagon-firm-light', 'yellow', 'pentagon', 'firm', 'light'), (
    'white-square-rough-lighter',
    'white', 'square', 'rough', 'lighter'), (
      'blue-circle-firm-medium', 'blue', 'circle', 'firm', 'medium'), (
        'white-pentagon-hard-heavy', 'white', 'pentagon', 'hard',
        'heavy'), ('green-oval-firm-light', 'green', 'oval', 'firm', 'light'), (
          'green-circle-rough-medium', 'green', 'circle', 'rough', 'medium'), (
            'yellow-pentagon-rough-light', 'yellow', 'pentagon', 'rough', 'light'), (
              'yellow-pentagon-hard-lighter', 'yellow', 'pentagon', 'hard', 'lighter'), (
                'white-oval-hard-heavy', 'white', 'oval', 'hard', 'heavy'), (
                  'white-pentagon-soft-heavy', 'white', 'pentagon', 'soft', 'heavy'), (
                    'blue-circle-smooth-light', 'blue', 'circle', 'smooth', 'light'), (
                      'red-oval-firm-light', 'red', 'oval', 'firm', 'light'), (
                        'yellow-square-smooth-light', 'yellow', 'square', 'smooth',
                        'light'), (
                          'green-oval-firm-light', 'green', 'oval', 'firm', 'light'), (
                            'yellow-oval-soft-heavier', 'yellow', 'oval', 'soft',
                            'heavier'), ('red-square-hard-light', 'red', 'square', 'hard',
                                         'light'), ('green-square-rough-light', 'green',
                                                    'square', 'rough', 'light'),
  ('blue-pentagon-rough-medium', 'blue', 'pentagon', 'rough',
   'medium'), ('yellow-pentagon-firm-medium', 'yellow', 'pentagon', 'firm',
               'medium'), ('blue-circle-rough-medium', 'blue', 'circle', 'rough',
                           'medium'), ('yellow-oval-hard-heavier', 'yellow', 'oval',
                                       'hard', 'heavier'), (
                                         'white-pentagon-smooth-medium', 'white',
                                         'pentagon', 'smooth', 'medium'),
  ('yellow-oval-firm-medium', 'yellow', 'oval', 'firm', 'medium'), (
    'blue-square-soft-medium', 'blue', 'square', 'soft',
    'medium'), ('yellow-rectangle-firm-heavy', 'yellow', 'rectangle', 'firm',
                'heavy'), ('white-pentagon-firm-medium', 'white', 'pentagon', 'firm',
                           'medium'), ('white-rectangle-rough-heavier', 'white',
                                       'rectangle', 'rough', 'heavier'),
  ('blue-oval-firm-medium', 'blue', 'oval', 'firm', 'medium'), (
    'yellow-pentagon-smooth-heavy', 'yellow', 'pentagon', 'smooth', 'heavy'), (
      'red-oval-soft-light', 'red', 'oval', 'soft',
      'light'), ('green-circle-rough-lighter', 'green', 'circle', 'rough', 'lighter'), (
        'yellow-square-rough-medium', 'yellow', 'square', 'rough', 'medium'), (
          'blue-square-smooth-medium', 'blue', 'square', 'smooth', 'medium'), (
            'white-pentagon-firm-medium', 'white', 'pentagon', 'firm', 'medium'), (
              'blue-rectangle-rough-heavier', 'blue', 'rectangle', 'rough', 'heavier'), (
                'yellow-circle-hard-light', 'yellow', 'circle', 'hard', 'light'), (
                  'white-circle-soft-heavier', 'white', 'circle', 'soft', 'heavier'), (
                    'red-pentagon-firm-heavier', 'red', 'pentagon', 'firm', 'heavier'), (
                      'white-pentagon-rough-heavier', 'white', 'pentagon', 'rough',
                      'heavier'), ('red-square-smooth-medium', 'red', 'square', 'smooth',
                                   'medium'), ('green-oval-rough-heavier', 'green',
                                               'oval', 'rough', 'heavier'),
  ('white-pentagon-rough-medium', 'white', 'pentagon', 'rough', 'medium'), (
    'blue-oval-hard-medium', 'blue', 'oval', 'hard', 'medium'), (
      'red-pentagon-rough-lighter', 'red', 'pentagon', 'rough',
      'lighter'), ('green-oval-smooth-light', 'green', 'oval', 'smooth', 'light'), (
        'white-pentagon-smooth-medium', 'white', 'pentagon', 'smooth',
        'medium'), ('white-square-rough-heavy', 'white', 'square', 'rough', 'heavy'), (
          'red-rectangle-hard-heavy', 'red', 'rectangle', 'hard',
          'heavy'), ('red-circle-hard-light', 'red', 'circle', 'hard', 'light'), (
            'blue-square-soft-lighter', 'blue', 'square', 'soft', 'lighter'), (
              'green-circle-firm-medium', 'green', 'circle', 'firm', 'medium'), (
                'red-square-soft-lighter', 'red', 'square', 'soft', 'lighter'), (
                  'blue-square-rough-light', 'blue', 'square', 'rough',
                  'light'), ('blue-oval-firm-medium', 'blue', 'oval', 'firm', 'medium'), (
                    'yellow-circle-hard-light', 'yellow', 'circle', 'hard', 'light'), (
                      'white-oval-soft-medium', 'white', 'oval', 'soft', 'medium'), (
                        'white-oval-soft-medium', 'white', 'oval', 'soft', 'medium'), (
                          'blue-oval-firm-medium', 'blue', 'oval', 'firm', 'medium'), (
                            'blue-square-rough-heavier', 'blue', 'square', 'rough',
                            'heavier'), ('red-oval-smooth-heavy', 'red', 'oval', 'smooth',
                                         'heavy'), ('red-circle-hard-lighter', 'red',
                                                    'circle', 'hard', 'lighter'),
  ('blue-circle-hard-heavier', 'blue', 'circle', 'hard',
   'heavier'), ('blue-circle-firm-medium', 'blue', 'circle', 'firm', 'medium'), (
     'white-square-hard-heavier', 'white', 'square', 'hard',
     'heavier'), ('red-pentagon-hard-medium', 'red', 'pentagon', 'hard', 'medium'), (
       'green-oval-hard-lighter', 'green', 'oval', 'hard', 'lighter'), (
         'white-pentagon-firm-medium', 'white', 'pentagon', 'firm', 'medium'), (
           'red-circle-firm-light', 'red', 'circle', 'firm', 'light'), (
             'blue-circle-soft-heavy', 'blue', 'circle', 'soft', 'heavy'), (
               'red-rectangle-rough-light', 'red', 'rectangle', 'rough', 'light'), (
                 'red-rectangle-firm-lighter', 'red', 'rectangle', 'firm', 'lighter'), (
                   'red-square-hard-lighter', 'red', 'square', 'hard', 'lighter'), (
                     'white-oval-firm-light', 'white', 'oval', 'firm', 'light'), (
                       'white-pentagon-rough-heavier', 'white', 'pentagon', 'rough',
                       'heavier'), ('yellow-oval-hard-lighter', 'yellow', 'oval', 'hard',
                                    'lighter'), ('yellow-pentagon-hard-heavier', 'yellow',
                                                 'pentagon', 'hard', 'heavier'), (
                                                   'yellow-oval-hard-heavy', 'yellow',
                                                   'oval', 'hard', 'heavy'), (
                                                     'blue-square-hard-heavier', 'blue',
                                                     'square', 'hard', 'heavier'),
  ('yellow-circle-hard-heavy', 'yellow', 'circle',
   'hard', 'heavy'), ('green-circle-hard-light', 'green', 'circle', 'hard', 'light'), (
     'white-circle-rough-light', 'white', 'circle', 'rough',
     'light'), ('yellow-square-rough-light', 'yellow', 'square', 'rough', 'light'), (
       'red-oval-soft-heavy', 'red', 'oval', 'soft', 'heavy'), (
         'green-pentagon-smooth-lighter', 'green', 'pentagon', 'smooth',
         'lighter'), ('blue-circle-firm-medium', 'blue', 'circle', 'firm', 'medium'), (
           'red-oval-soft-heavier', 'red', 'oval', 'soft', 'heavier'), (
             'green-circle-rough-medium', 'green', 'circle', 'rough', 'medium'), (
               'yellow-oval-smooth-heavy', 'yellow', 'oval', 'smooth', 'heavy'), (
                 'red-rectangle-hard-heavy', 'red', 'rectangle', 'hard', 'heavy'), (
                   'blue-pentagon-rough-medium', 'blue', 'pentagon', 'rough', 'medium'), (
                     'yellow-oval-firm-lighter', 'yellow', 'oval', 'firm', 'lighter'), (
                       'yellow-square-smooth-heavy', 'yellow', 'square', 'smooth',
                       'heavy'), ('red-oval-rough-medium', 'red', 'oval', 'rough',
                                  'medium'), ('green-square-rough-light', 'green',
                                              'square', 'rough', 'light'),
  ('blue-oval-rough-lighter', 'blue', 'oval', 'rough',
   'lighter'), ('white-square-smooth-heavy', 'white', 'square', 'smooth', 'heavy'), (
     'white-square-hard-lighter', 'white', 'square', 'hard',
     'lighter'), ('green-oval-smooth-medium', 'green', 'oval', 'smooth', 'medium'), (
       'red-oval-rough-light', 'red', 'oval', 'rough',
       'light'), ('yellow-circle-firm-heavier', 'yellow', 'circle', 'firm', 'heavier'), (
         'white-pentagon-rough-medium', 'white', 'pentagon', 'rough',
         'medium'), ('red-oval-rough-heavier', 'red', 'oval', 'rough', 'heavier'), (
           'blue-oval-smooth-light', 'blue', 'oval', 'smooth',
           'light'), ('yellow-oval-rough-light', 'yellow', 'oval', 'rough', 'light'), (
             'yellow-oval-soft-heavy', 'yellow', 'oval', 'soft', 'heavy'), (
               'blue-oval-smooth-heavy', 'blue', 'oval', 'smooth', 'heavy'), (
                 'red-square-hard-medium', 'red', 'square', 'hard', 'medium'), (
                   'white-oval-hard-medium', 'white', 'oval', 'hard', 'medium'), (
                     'yellow-circle-smooth-heavier', 'yellow', 'circle', 'smooth',
                     'heavier'), ('blue-pentagon-smooth-light', 'blue', 'pentagon',
                                  'smooth', 'light'), ('green-oval-hard-lighter', 'green',
                                                       'oval', 'hard', 'lighter'),
  ('green-square-rough-heavier', 'green', 'square', 'rough', 'heavier'), (
    'green-pentagon-firm-medium', 'green', 'pentagon',
    'firm', 'medium'), ('yellow-oval-hard-medium', 'yellow', 'oval', 'hard',
                        'medium'), ('blue-circle-soft-heavier', 'blue', 'circle', 'soft',
                                    'heavier'), (
                                      'green-oval-soft-medium', 'green', 'oval', 'soft',
                                      'medium'), ('white-oval-rough-medium', 'white',
                                                  'oval', 'rough', 'medium'), (
                                                    'blue-circle-smooth-light', 'blue',
                                                    'circle', 'smooth', 'light'), (
                                                      'blue-square-smooth-medium', 'blue',
                                                      'square', 'smooth', 'medium')
]


class DBGenerator(object):
  def generate_faceted_objects(self):
    '''The generated list was manually copied into this file.'''
    db = []
    for i in range(1000):
      color = facets['color'][random.randint(0, 4)]
      shape = facets['shape'][random.randint(0, 4)]
      texture = facets['texture'][random.randint(0, 4)]
      weight = facets['weight'][random.randint(0, 4)]
      db.append(
        (
          '-'.join(
            [
              color, shape, texture, weight
            ]
          ), color, shape, texture, weight
        )
      )
    pprint.pprint(db, width=100, indent=2)

  def count_duplicates(self):
    d = [f[0] for f in faceted_objects]
    for k, g in itertools.groupby(sorted(d)):
      print k, len(list(g))


if __name__ == "__main__":
  d = DBGenerator()
  d.generate_faceted_objects()
  #d.count_duplicates()
