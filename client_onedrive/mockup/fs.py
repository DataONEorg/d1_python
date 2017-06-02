#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Filesystem mockups
"""

import datetime
import itertools
import re

#d = datetime.datetime.now()
d = datetime.datetime(2005, 5, 23, 11, 12, 13)

# The filesystem that is used in the unit tests.
#fs = (
#  ('fa', 50, d),
#  ('fb', 51, d),
#  ('d',
#    (
#      ('f2a', 52, d),
#      ('f2b', 53, d),
#      ('f2c', 54, d),
#      ('d2',
#        (
#          ('f3a', 55, d),
#          ('f3b', 56, d),
#        ), d
#      )
#    ), d
#  )
#)

# Mockup of gradual start and end date restriction

# A folder which is not meant to be opened in the mockup.
empty_folder = (('(empty)', 0, d),)

# - Year, month and day values are not listed if there are no objects in the
#   current set that start at that time.
# - The mockup does not vary the available selections based on previous
#   selections.

################################################################################
# Mockup of start date restriction.

unapplied_facets = (('@StartDate', empty_folder, d),
                    ('@EndDate', empty_folder, d),
                    ('@Keyword', empty_folder, d),
                    ('@MemberNode', empty_folder, d),
                    ('@GeographicalArea', empty_folder, d),
                    ('@Field', empty_folder, d),)

objects_unfiltered = (('science_object_1', empty_folder, d),
                      ('science_object_2', empty_folder, d),
                      ('science_object_3', empty_folder, d),
                      ('science_object_4', empty_folder, d),
                      ('science_object_5', empty_folder, d),
                      ('science_object_6', empty_folder, d),
                      ('science_object_7', empty_folder, d),
                      ('science_object_8', empty_folder, d),
                      ('science_object_9', empty_folder, d),)

objects_filtered_by_year = (('obj_start_date_year_filtered_1', empty_folder, d),
                            ('obj_start_date_year_filtered_2', empty_folder, d),
                            ('obj_start_date_year_filtered_3', empty_folder, d),
                            ('obj_start_date_year_filtered_4', empty_folder, d),
                            ('obj_start_date_year_filtered_5', empty_folder, d),)

objects_filtered_by_year_month = (
  ('obj_start_date_year_month_filtered_1', empty_folder, d),
  ('obj_start_date_year_month_filtered_2', empty_folder, d),
  ('obj_start_date_year_month_filtered_3', empty_folder, d),
  ('obj_start_date_year_month_filtered_4', empty_folder, d),
  ('obj_start_date_year_month_filtered_5', empty_folder, d),
)

objects_filtered_by_year_month_day = (
  ('obj_start_date_year_month_day_filtered_1', empty_folder, d),
  ('obj_start_date_year_month_day_filtered_2', empty_folder, d),
  ('obj_start_date_year_month_day_filtered_3', empty_folder, d),
  ('obj_start_date_year_month_day_filtered_4', empty_folder, d),
  ('obj_start_date_year_month_day_filtered_5', empty_folder, d),
)

start_day_facet_vals = (
  ('#05', unapplied_facets + objects_filtered_by_year_month_day, d),
  ('#07', unapplied_facets + objects_filtered_by_year_month_day, d),
  ('#23', unapplied_facets + objects_filtered_by_year_month_day, d),
  ('#30', unapplied_facets + objects_filtered_by_year_month_day, d),
)

start_day = (('@StartDay', start_day_facet_vals, d),
             ) + unapplied_facets + objects_filtered_by_year_month

start_month_facet_vals = (('#01_Jan', start_day, d),
                          ('#02_Feb', start_day, d),
                          ('#03_Mar', start_day, d),
                          ('#10_Oct', start_day, d),
                          ('#12_Dec', start_day, d),)

start_month = (('@StartMonth', start_month_facet_vals, d),
               ) + unapplied_facets + objects_filtered_by_year

start_year_facet_vals = (('#2003', start_month, d),
                         ('#2004', start_month, d),
                         ('#2005', start_month, d),
                         ('#2007', start_month, d),
                         ('#2010', start_month, d),)

start_date_mockup = start_year_facet_vals + unapplied_facets + objects_unfiltered

################################################################################
# Mockup of keyword restriction.


def get_random_words_sorted():
  words = open('./words.txt').read().split('\n')
  words = [re.sub('\'s', '', w) for w in words]
  return words


def group_words(words, n_words_in_group):
  # returns an iterable of lists
  args = [iter(words)] * n_words_in_group
  return itertools.izip_longest(*args)


def first_last_per_group(groups):
  first_last = []
  for g in groups:
    first_last.append('#{0}-{1}'.format(g[0], g[-1]))
  return first_last


def first_last(random_words, n_words_in_group):
  groups = group_words(random_words, n_words_in_group)
  return first_last_per_group(groups)


def group_from_first_last(words, first_last):
  first, last = first_last[1:].split('-')
  g = []
  for w in words:
    if w >= first and w <= last:
      # Only populate one word with the unapplied facets to minimize number of
      # files.
      if w == 'brazennesss':
        g.append((w, unapplied_facets + objects_unfiltered, d))
      else:
        g.append((w, empty_folder, d))
  return g


random_words = get_random_words_sorted()

keyword_group = [(f, group_from_first_last(random_words, f), d)
                 for f in first_last(random_words, 100)]

keyword_restriction_mockup = tuple(
  keyword_group
) + unapplied_facets + objects_unfiltered

################################################################################
# Mockup of member node restriction.

member_nodes = [
  '#Knowledge Network for Biocomplexity (KNB)',
  '#Oak Ridge National Laboratory Distributed Active Archive Center (ORNL DAAC)',
  '#South Africa National Parks (SanParks)',
  '#Ecological Society of America (ESA) Data Registry'
  '#USGS Core Sciences Clearinghouse',
  '#Partnership for Interdisciplinary Studies of Coastal Oceans (PISCO)',
  '#University of California Curation Center (UC3) Merritt Repository',
  '#Long Term Ecological Research Network (LTER)',
  '#Cornell Lab of Ornithology Avian Knowledge Network (AKN)',
  '#ONEShare',
  '#Dryad',
  '#Earth Data Analysis Center (EDAC)',
]

member_node_restriction_mockup = tuple(
  (m, unapplied_facets + objects_unfiltered, d) for m in member_nodes
)

################################################################################
# Mockup of geo area.

continents = [
  '#Africa',
  '#Europe',
  '#Asia',
  '#North America',
  '#South America',
  '#Antarctica',
  '#Australia',
]

countries = [
  '#country in selected continent 1',
  '#country in selected continent 2',
  '#country in selected continent 3',
  '#country in selected continent 4',
]

countries_tuple = tuple(
  [(c, unapplied_facets + objects_unfiltered, d) for c in countries]
)

countries_all = [
  '#Afghanistan',
  '#Albania',
  '#Algeria',
  '#Andorra',
  '#Angola',
  '#Yemen',
  '#Zaire',
  '#Zambia',
  '#Zimbabwe',
]

countries_all_tuple = tuple(
  [(c, unapplied_facets + objects_unfiltered, d) for c in countries_all]
)

longlat = tuple((l, empty_folder, d)
                for l in ('@Degrees', '@Minutes', '@Seconds'))

geo_restriction_mockup = (
  ('@Continent', tuple((m, countries_tuple, d) for m in continents), d),
  ('@Country', countries_all_tuple, d),
  ('@Latitude', longlat, d),
  ('@Longitude', longlat, d),
)

#print geo_restriction_mockup
#exit()

################################################################################
# Mockup of data package

data_package_1 = ((
  'data_package_1', (('data_package_1.bagit.zip', 48321, d),
                     ('pid_abc.jpg', 483, d),
                     ('pid_def.csv', 4833, d),
                     ('pid_ghi.csv', 6553, d),
                     ('pid_jkl.eml', 46553, d),
                     ('pid_jkl.html', 32522, d),
                     (
                       'system', (('pid_abc.jpg.xml', 483, d),
                                  ('pid_abc.jpg.html', 821, d),
                                  ('pid_def.xml', 4833, d),
                                  ('pid_def.html', 8222, d),
                                  ('pid_ghi.csv.xml', 6553, d),
                                  ('pid_ghi.csv.html', 12964, d),
                                  ('pid_jkl.eml.xml', 46553, d),
                                  ('pid_jkl.eml.html', 83212, d),), d
                     ),), d
),)

################################################################################
# Mockup of ONEMercury integration

#fs = (
#  ('dahl', (
#    ('Easter Seaboard, water temperatures, 2000-2005', (
#      ('ark:_13030_m5z60p9f_1_cadwsap-s3410003-005.xml', 34822, d),
#      ('ark:_13030_m5mk6bww_1_cadwsap-s4900546-001.xml', 4676, d),
#      ('scimeta_1067.xml', 9573, d),
#    ), d),
#    ('My project 1', empty_folder, d),
#    ('My project 2', empty_folder, d),
#  ), d),
#)

################################################################################

fs = (('@StartDate', start_date_mockup, d),
      ('@EndDate', empty_folder, d),
      ('@Keyword', keyword_restriction_mockup, d),
      ('@MemberNode', member_node_restriction_mockup, d),
      ('@GeographicalArea', geo_restriction_mockup, d),
      ('@Field', empty_folder, d),) + objects_unfiltered + data_package_1

#pprint.pprint(fs)
#exit()

## The filesystem that is used in the unit tests.
#fs = (
#  ('fa', 50, d),
#  ('fb', 51, d),
#  ('d',
#    (
#      ('f2a', 52, d),
#      ('f2b', 53, d),
#      ('f2c', 54, d),
#      ('d2',
#        (
#          ('f3a', 55, d),
#          ('f3b', 56, d),
#        ), d
#      )
#    ), d
#  )
#)
