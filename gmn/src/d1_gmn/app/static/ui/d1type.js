//  This work was created by participants in the DataONE project, and is
//  jointly copyrighted by participating institutions in DataONE. For
//  more information on DataONE, see our web site at http://dataone.org.
//
//    Copyright 2009-2016 DataONE
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
function get_next_slice_url(new_start) {
  var url = new URL(window.location.href);
  var search_params = new URLSearchParams(url.search);
  search_params.set("start", new_start);
  url.search = search_params.toString();
  return url.toString();
}

function open_slice(new_start) {
  window.location.href = get_next_slice_url(new_start);
}


// Run when document is ready
$(function () {
  // Add tooltip for truncated text
  $('.tree').each(function () {
    var $ele = $(this);
    if (this.offsetWidth < this.scrollWidth)
      $ele.attr('title', $ele.text());
  });

  // Clear button tooltips
  $('.round-button').each(function () {
      $(this).attr('title', '');
  });

  // Add tooltip for Resolve buttons
  $('.round-button:contains(R)').each(function () {
      $(this).attr('title', 'Resolve on CN');
  });

  // Add tooltip for SysMeta buttons
  $('.round-button:contains(S)').each(function () {
      $(this).attr('title', 'View System Metadata');
  });
});
