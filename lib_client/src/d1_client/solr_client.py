#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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

# language=rst
"""Basic Solr client.

Based on: http://svn.apache.org/viewvc/lucene/solr/tags/release-1.2.0/client/python/solr.py

DataONE provides an index of all objects stored in the Member Nodes that form the
DataONE federation. The index is stored in an Apache :term:`Solr` database and can be
queried with the SolrClient.

The DataONE Solr index provides information only about objects for which the caller has
access. When querying the index without authenticating, only records related to public
objects can be retrieved. To authenticate, provide a certificate signed by
:term:`CILogon` or a JWT token issued by DataONE when creating the client.

Example:

.. highlight:: python

::

  # Connect to the DataONE Coordinating Nodes in the default (production) environment.
  c = d1_client.solr_client.SolrConnection()

  search_result = c.search({
    'q': 'id:[* TO *]', # Filter for search
    'rows': 10, # Number of results to return
    'fl': 'formatId', # List of fields to return for each result
  })

  pprint.pprint(search_result)

.. highlight:: none

"""
import datetime
import logging
import pprint
import random
import xml.sax.saxutils

import requests.structures

import d1_common.const
import d1_common.url
import d1_common.utils.ulog

import d1_client.baseclient_1_2

log = d1_common.utils.ulog.getLogger(__name__)


FIELD_TYPE_CONVERSION_MAP = {
    "t": "text",
    "s": "string",
    "dt": "date",
    "d": "double",
    "f": "float",
    "i": "int",
    "l": "long",
    "tw": "text_ws",
    "text": "text",
    "guid": "string",
    "itype": "string",
    "origin": "string",
    "oid": "string",
    "gid": "string",
    "modified": "date",
    "created": "date",
}

RESERVED_CHAR_LIST = [
    "+",
    "-",
    "&",
    "|",
    "!",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "^",
    '"',
    "~",
    "*",
    "?",
    ":",
]

DEFAULT_QUERY_DICT = {"wt": {"json": []}, "q": {"*.*": []}, "fl": {"*": []}}


def dump(o, msg=None):
    """Dump object to the log.
    """
    log.debug(">" * 100)
    if msg:
        log.debug(msg)
    log.debug(pprint.pformat(o))
    log.debug("<" * 100)


class QueryBuilder:
    def __init__(self, q=None):
        q = q or {}
        self.param_dict = {}
        for param, field in q.items():
            self.add(param, field)

    def __str__(self):
        return "QueryBuilder({})".format(",".join(self.query_dict.keys()))

    def add(self, param, field="", value=None):
        """
        param: q, fl
        field: id, checksum
        value: str, int, bytes or arbitrarily nested lists of same.
        """
        log.info("#" * 20)
        log.info('add: "{}" "{}" "{}"'.format(param, field, value))
        self.param_dict.setdefault(param, {}).setdefault(field, [])
        if value is None:
            return
        dump(value)
        norm_value = self._norm_value(value)
        dump(norm_value)
        if isinstance(norm_value, str):
            norm_value = [norm_value]
        self.param_dict[param][field].extend(norm_value)
        dump(self.query_dict, "------------------------------")

    @property
    def query_str(self):
        s = self._get_query_str()
        log.info("#" * 100)
        log.info("Generated query string: {}".format(s))
        dump(self.query_dict, "Returned query str from this dict")
        log.info("#" * 100)
        return s

    @property
    def query_dict(self):
        """Direct access to the underlying dict"""
        return self.param_dict

    def get_value(self, param, field, value_idx):
        return self.query_dict[param][field][value_idx]

    def _get_query_str(self):
        default_dict = {**DEFAULT_QUERY_DICT, **self.param_dict}
        ret_list = []
        for param, field_dict in default_dict.items():
            for field, value_list in field_dict.items():
                if not value_list:
                    ret_list.append("{}={}".format(param, field))
                else:
                    for value in value_list:
                        ret_list.append(
                            "{}={}:{}".format(param, field, self._get_value_str(value))
                        )
        return "?{}".format("&".join(ret_list))

    def _get_value_str(self, value):
        return self._prep_query_term(value)

    def _norm_value(self, value):
        flat_list = []

        def r_(v_):
            if isinstance(v_, (str, int)):
                flat_list.append(str(v_))
            elif isinstance(v_, bytes):
                flat_list.append(v_.decode("utf-8"))
            else:
                for v in v_:
                    r_(v)

        r_(value)
        return flat_list

    def _prep_query_term(self, term_str):
        add_star = term_str.endswith("*")
        term_str = term_str.rstrip("*")
        esc_term_str = self._escape_query_term(term_str)
        if add_star:
            return esc_term_str + "*"
        return d1_common.url.encodeQueryElement(esc_term_str)

    def _escape_query_term(self, term):
        """Escape a query term for inclusion in a query.
        """
        # term = term.replace("\\", "\\\\")
        for c in RESERVED_CHAR_LIST:
            term = term.replace(c, r"\{}".format(c))
        return term


class SolrClient(d1_client.baseclient_1_2.DataONEBaseClient_1_2):
    # language=rst
    """Extend DataONEBaseClient_1_2 with functions for querying Solr indexes hosted on
    CNs and MNs.

    Examples:

        To connect to DataONE's production environment::

            solr_client = SolrClient()

        To connect to a non-production environment, pass the baseURL for the environment. E.g.::

            solr_client = SolrClient('https://cn-stage.test.dataone.org/cn')

        For the supported keyword args, see::

            d1_client.session.Session()

        Most methods take a ``query_dict`` as a parameter. It allows passing any number
        of query parameters that will be sent to Solr.

        Pass the query parameters as regular keyword arguments. E.g.::

            solr_client.search(q=Param('id', 'abc*'), fq=Param('id', 'def*'))

        To pass multiple query parameters of the same type, pass a list. E.g., to
        pass multiple filter query (``fq``) parameters::

            solr_client.search(
                q=Param('id', 'abc*'),
                fq=[Param('id', 'def*'), Param('id', 'ghi')]
            )

    See also:

        https://releases.dataone.org/online/api-documentation-v2.0/design/SearchMetadata.html

    """

    def __init__(self, base_url=d1_common.const.URL_DATAONE_ROOT, *args, **kwargs):
        self._base_url = base_url
        header_dict = requests.structures.CaseInsensitiveDict(kwargs.pop("headers", {}))
        header_dict.setdefault(
            "Content-Type", "application/x-www-form-urlencoded; charset=utf-8"
        )
        self._query_engine = kwargs.pop("query_engine", "solr")
        super().__init__(base_url, headers=header_dict, *args, **kwargs)

    def __str__(self):
        return 'SolrClient(base_url="{}")'.format(self._base_url)

    def __repr__(self):
        return str(self)

    # GET queries

    # noinspection PyMethodOverriding
    def get_object(self, doc_id):
        """Retrieve information about the specified document."""
        q = QueryBuilder()
        q.add("q", "id", doc_id)
        resp_dict = self._get_query(q)
        if resp_dict["response"]["numFound"] > 0:
            return resp_dict["response"]["docs"][0]

    def search(self, **query_dict):
        """Search the Solr index.

        Example:

        result_dict = search(q=['id:abc*'], fq=['id:def*', 'id:ghi'])

        """
        return self._get_query(**query_dict)

    # noinspection PyTypeChecker
    def get_ids(self, start=0, rows=1000, **query_dict):
        """Retrieve a list of identifiers for documents matching the query."""
        resp_dict = self._get_query(**query_dict)
        return {
            "matches": resp_dict["response"]["numFound"],
            "start": start,
            "ids": [d["id"] for d in resp_dict["response"]["docs"]],
        }

    def count(self, **query_dict):
        """Return the number of entries that match query."""
        param_dict = query_dict.copy()
        param_dict["count"] = 0
        resp_dict = self._get_query(**param_dict)
        return resp_dict["response"]["numFound"]

    def get_value_counts(self, field_name, maxvalues=-1, sort=True, **query_dict):
        """Retrieve the unique values for a field, along with their usage counts.

        :param field_name: Name of field for which to retrieve values
        :type field_name: string

        :param sort: Sort the result

        :param maxvalues: Maximum number of values to retrieve. Default is -1,
          which causes retrieval of all values.
        :type maxvalues: int

        :returns: dict of {fieldname: [[value, count], ... ], }

        """
        q = QueryBuilder(
            {
                **{
                    "rows": "0",
                    "facet": "true",
                    "facet.field": field_name,
                    "facet.limit": str(maxvalues),
                    "facet.zeros": "false",
                    "facet.sort": str(sort).lower(),
                },
                **query_dict,
            }
        )
        resp_dict = self._post_query(q)
        self.add_solr_dict_root_refs(resp_dict)
        self.make_pairs(resp_dict["facet_fields"])
        self.add_root_attr(
            resp_dict, f"facet_counts/facet_fields/{field_name}", "value_count_list"
        )
        dump(resp_dict, "get_value_counts() returned")
        return resp_dict

    def add_solr_dict_root_refs(self, resp_dict, attr_name=None):
        """Add attributes of nested dicts to the root of Solr response dicts for easier
        access.

        Can be applied to all Solr response dicts.
        """
        self.add_root_attr(resp_dict, "facet_counts/facet_fields", attr_name)
        self.add_root_attr(resp_dict, "response/numFound")

    def add_root_attr(self, root_obj, attr_path, attr_name=None):
        """Add attribute to attribute in object tree to root for easier access.
        Takes a path to the attribute instead of the attribute directly and is
        a no-op for objects without the attribute.

        Args:
            root_obj: The object in which the new name for
            attr_path: str
                String on form '/attr/attr/attr'

                Path to attribute which for which a attribute will be added to the root.
                Each element of the path corresponds to an attribute of the object in
                that location of the tree. All attributes except the final one must
                support element access, like lists and dicts (anything providing
                ``__getitem__()``).
            attr_name: str (optional)
                Name of the new attribute. If not provided, the same name as the
                existing attribute is used.
        """

        def _r(obj_, path_):
            if len(path_) == 1:
                return obj_[path_[0]]
            return _r(obj_[path_[0]], path_[1:])

        path_list = attr_path.strip("/ \n").split("/")
        try:
            root_obj[attr_name or path_list[-1]] = _r(root_obj, path_list)
        except LookupError:
            log.debug(
                'Invalid path for object. path="{}" obj="{}"'.format(
                    attr_path, root_obj
                )
            )

    def make_pairs(self, field_dict):
        """Modify values in dict that are lists that look like they're holding a
        sequence of strings and counts to a list of (str, int) tuples.

        [field, count, field, count] -> [(field, count), (field, count)]

        This is to help prevent the pairs from being split up.
        """
        for k, v in field_dict.items():
            try:
                if not len(v) & 1:
                    field_dict[k] = [
                        (field, int(count)) for field, count in zip(v[::2], v[1::2])
                    ]
            except (ValueError, TypeError):
                pass

    def get_field_min_max(self, field_name, **query_dict):
        """Returns the minimum and maximum values of the specified field. This requires
        two search calls to the service, each requesting a single value of a single
        field.

        @param field_name(string) field_name of the field
        @param query_dict(string) Query identifying range of records for min and max values

        @return list of [min, max]

        """
        param_dict = query_dict.copy()
        param_dict.update({"rows": 1, "fl": field_name, "sort": "%s asc" % field_name})
        try:
            min_resp_dict = self._post_query(**param_dict)
            param_dict["sort"] = "%s desc" % field_name
            max_resp_dict = self._post_query(**param_dict)
            return (
                min_resp_dict["response"]["docs"][0][field_name],
                max_resp_dict["response"]["docs"][0][field_name],
            )
        except Exception:
            log.exception("Exception")
            raise

    def field_alpha_histogram(self, field_name, bin_count=10, **query_dict):
        """Generates a histogram of values from a string field.

        Output is: [[low, high, count, query], ... ]. Bin edges is determined by equal
        division of the fields.

        Potentially very expensive for fields that have a high number of different
        strings.

        """

        log.setLevel(level=logging.DEBUG)
        d1_common.utils.ulog.setup(True)

        q = QueryBuilder(
            {
                **{
                    "rows": "0",
                    "facet": "true",
                    "facet.field": field_name,
                    "facet.limit": 1,
                    "facet.mincount": 1,
                },
                **query_dict,
            }
        )

        bin_dict = {}

        def add_bin_(bin_facet, bin_name=None):
            bin_name = bin_name or bin_facet
            log.debug(f'Adding facet query for bin "{bin_name}": {bin_facet}')
            q.add("facet.query", field=field_name, value=bin_facet)
            bin_dict[bin_facet] = bin_name

        value_count_dict = self.get_value_counts(field_name, maxvalues=-1, **query_dict)
        value_count_list = value_count_dict["value_count_list"]
        value_name_list = [v[0] for v in value_count_list]
        unique_value_count = len(value_count_list)

        log.debug(
            f'Number of unique values for field "{field_name}": {unique_value_count}'
        )

        if unique_value_count == bin_count:
            log.debug(
                "Field has same number of unique values as the requested number of bins."
            )

        if unique_value_count < bin_count:
            log.debug(
                "Field has fewer unique values than the requested number of bins. Lowering number of bins to {}.".format(
                    unique_value_count
                )
            )
            bin_count = unique_value_count

        if unique_value_count == bin_count:
            log.debug("Using equivalence queries for all bins.")
            for v in value_name_list:
                add_bin_(v)

        else:
            log.debug("Field has more unique values than the requested number of bins.")
            delta = unique_value_count // bin_count
            if delta == 1:
                log.debug(
                    "Using equivalence queries for all bins except the last bin, which will include the remainder of terms."
                )
                for i in range(bin_count - 1):
                    add_bin_(value_name_list[i])

                add_bin_(f"[{value_name_list[-1]} TO *]", value_name_list[-1])
            else:
                log.debug("Using range queries for all bins.")
                c_offset = 0.0
                delta = float(unique_value_count) / float(bin_count)
                for i in range(bin_count):
                    lower_idx = int(c_offset)
                    upper_idx = (int(c_offset + delta)) - 1
                    lower_term = value_name_list[lower_idx]
                    upper_term = value_name_list[upper_idx]
                    if i == 0:
                        add_bin_(f"[* TO {upper_term}]", upper_term)
                    elif i == bin_count - 1:
                        add_bin_(f"[{lower_term} TO *]", lower_term)
                    else:
                        add_bin_(f"[{lower_term} TO {upper_term}]", lower_term)

                    c_offset = c_offset + delta

        resp_dict = self._post_query(q)
        resp_dict["bin_dict"] = bin_dict
        dump(resp_dict, "field_alpha_histogram() returned")
        return resp_dict

    # POST queries

    def delete(self, doc_id):
        return self.query(
            "solr",
            "<delete><id>" + self._escape_xml_entity(str(doc_id)) + "</id></delete>",
            do_post=True,
        )

    def delete_by_query(self, query):
        return self.query(
            "solr",
            "<delete><query>" + self._escape_xml_entity(query) + "</query></delete>",
            do_post=True,
        )

    def add(self, **fields):
        return self.query(
            "solr", "<add>{}</add>".format(self._format_add(fields)), do_post=True
        )

    def add_docs(self, docs):
        """docs is a list of fields that are a dictionary of field_name:value for a record."""
        return self.query(
            "solr",
            "<add>{}</add>".format(
                "".join([self._format_add(fields) for fields in docs])
            ),
            do_post=True,
        )

    def commit(self, waitFlush=True, waitSearcher=True, optimize=False):
        xstr = "<commit"
        if optimize:
            xstr = "<optimize"
        if not waitSearcher:  # just handle deviations from the default
            if not waitFlush:
                xstr += ' waitFlush="false" waitSearcher="false"'
            else:
                xstr += ' waitSearcher="false"'
        xstr += "/>"
        return self.query("solr", xstr, do_post=True)

    # Private

    def _escape_xml_entity(self, s):
        return xml.sax.saxutils.quoteattr(s).encode("utf-8")

    def _coerce_type(self, field_type, value):
        """Returns unicode(value) after trying to coerce it into the Solr field type.

        @param field_type(string) The Solr field type for the value
        @param value(any) The value that is to be represented as Unicode text.

        """
        if value is None:
            return None
        if field_type == "string":
            return str(value)
        elif field_type == "text":
            return str(value)
        elif field_type == "int":
            try:
                v = int(value)
                return str(v)
            except:
                return None
        elif field_type == "float":
            try:
                v = float(value)
                return str(v)
            except:
                return None
        elif field_type == "date":
            try:
                v = datetime.datetime(
                    value["year"],
                    value["month"],
                    value["day"],
                    value["hour"],
                    value["minute"],
                    value["second"],
                )
                v = v.strftime("%Y-%m-%dT%H:%M:%S.0Z")
                return v
            except:
                return None
        return str(value)

    def _get_solr_type(self, field):
        """Returns the Solr type of the specified field field_name.

        Assumes the convention of dynamic fields using an underscore + type character
        code for the field field_name.

        """
        field_type = "string"
        try:
            field_type = FIELD_TYPE_CONVERSION_MAP[field]
            return field_type
        except:
            pass
        fta = field.split("_")
        if len(fta) > 1:
            ft = fta[len(fta) - 1]
            try:
                field_type = FIELD_TYPE_CONVERSION_MAP[ft]
                # cache the type so it's used next time
                FIELD_TYPE_CONVERSION_MAP[field] = field_type
            except:
                pass
        return field_type

    def _format_add(self, fields):
        el_list = ["<doc>"]
        for f, v in list(fields.items()):
            field_type = self._get_solr_type(f)
            if isinstance(v, list):
                for vi in v:
                    vi = self._coerce_type(field_type, vi)
                    if vi is not None:
                        el_list.append('<field name="')
                        el_list.append(self._escape_xml_entity(str(f)))
                        el_list.append('">')
                        el_list.append(self._escape_xml_entity(vi))
                        el_list.append("</field>")
            else:
                v = self._coerce_type(field_type, v)
                if v is not None:
                    el_list.append('<field name="')
                    el_list.append(self._escape_xml_entity(str(f)))
                    el_list.append('">')
                    el_list.append(self._escape_xml_entity(v))
                    el_list.append("</field>")
        el_list.append("</doc>")
        return "".join(el_list)

    def _get_query(self, q):
        """Perform a GET query against Solr and return the response as a Python dict."""
        return self._send_query(q, do_post=False)

    def _post_query(self, q):
        """Perform a POST query against Solr and return the response as a Python
        dict."""
        return self._send_query(q, do_post=True)

    def _send_query(self, q, do_post=False):
        """Perform a query against Solr and return the response as a Python dict."""
        result_dict = self.query(
            queryEngine="solr", query_str=q.query_str, do_post=do_post
        )
        dump(result_dict, "Response from Solr")
        return result_dict


# =========================================================================


class SolrRecordTransformerBase(object):
    """Base for Solr record transformers.

    Used to transform a Solr search response document into some other form, such as a
    dictionary or list of values.

    """

    def __init__(self):
        pass

    def transform(self, record):
        return record


# =========================================================================


class SolrArrayTransformer(SolrRecordTransformerBase):
    """A transformer that returns a list of values for the specified columns."""

    def __init__(self, cols=None):
        super().__init__()
        self.cols = cols or ["lng", "lat"]

    def transform(self, record):
        res = []
        for col in self.cols:
            try:
                v = record[col]
                if isinstance(v, list):
                    res.append(v[0])
                else:
                    res.append(v)
            except:
                res.append(None)
        return res


# =========================================================================


class SolrSearchResponseIterator(object):
    """Performs a search against a Solr index and acts as an iterator to retrieve all
    the values."""

    def __init__(
        self,
        client,
        page_size=100,
        max_records=1000,
        transformer=SolrRecordTransformerBase(),
        **query_dict,
    ):
        self.client = client
        self.query_dict = query_dict.copy()
        self.page_size = page_size
        self.max_records = max_records or 99999999

        self.c_record = 0
        self.res = None
        self.done = False
        self.transformer = transformer
        self._next_page(self.c_record)
        self._num_hits = 0

        log.debug("Iterator hits={}".format(self.res["response"]["numFound"]))

    def _next_page(self, offset):
        """Retrieves the next set of results from the service."""
        log.debug("Iterator c_record={}".format(self.c_record))
        page_size = self.page_size
        if (offset + page_size) > self.max_records:
            page_size = self.max_records - offset
        param_dict = self.query_dict.copy()
        param_dict.update(
            {
                "start": str(offset),
                "rows": str(page_size),
                "explainOther": "",
                "hl.fl": "",
            }
        )
        self.res = self.client.search(**param_dict)
        self._num_hits = int(self.res["response"]["numFound"])

    def __iter__(self):
        return self

    def process_row(self, row):
        """Override this method in derived classes to reformat the row response."""
        return row

    def __next__(self):
        if self.done:
            raise StopIteration()
        if self.c_record > self.max_records:
            self.done = True
            raise StopIteration()
        idx = self.c_record - self.res["response"]["start"]
        try:
            row = self.res["response"]["docs"][idx]
        except IndexError:
            self._next_page(self.c_record)
            idx = self.c_record - self.res["response"]["start"]
            try:
                row = self.res["response"]["docs"][idx]
            except IndexError:
                self.done = True
                raise StopIteration()
        self.c_record = self.c_record + 1
        return self.transformer.transform(row)


# =========================================================================


class SolrArrayResponseIterator(SolrSearchResponseIterator):
    """Returns an iterator that operates on a Solr result set.

    The output for each document is a list of values for the columns specified in the
    cols parameter of the constructor.

    """

    def __init__(self, client, page_size=100, cols=None, **query_dict):
        cols = cols or ["lng", "lat"]
        transformer = SolrArrayTransformer(cols)

        param_dict = query_dict.copy()
        param_dict.update({"fields": ",".join(cols)})

        SolrSearchResponseIterator.__init__(
            self, client, page_size, transformer=transformer, **param_dict
        )


# =========================================================================


class SolrSubsampleResponseIterator(SolrSearchResponseIterator):
    """Returns a pseudo-random subsample of the result set.

    Works by calculating the number of pages required for the entire data set and taking
    a random sample of pages until n_samples can be retrieved.  So pages are random, but
    records within a page are not.

    """

    def __init__(
        self,
        client,
        q,
        fq=None,
        fields="*",
        page_size=100,
        n_samples=10000,
        transformer=SolrRecordTransformerBase(),
    ):
        self._c_record = None
        self._page_starts = [0]
        self._c_page = 0
        SolrSearchResponseIterator.__init__(
            self, client, q, fq, fields, page_size, transformer
        )
        n_pages = self._num_hits / self.page_size
        if n_pages > 0:
            sample_size = n_samples / page_size
            if sample_size > n_pages:
                sample_size = n_pages
            self._page_starts += random.sample(list(range(0, n_pages)), sample_size)
            self._page_starts.sort()

    def __next__(self):
        """Overrides the default iteration by sequencing through records within a page
        and when necessary selecting the next page from the randomly generated list."""
        if self.done:
            raise StopIteration()
        idx = self.c_record - self.res["response"]["start"]
        try:
            row = self.res["response"]["docs"][idx]
        except IndexError:
            self._c_page += 1
            try:
                self._c_record = self._page_starts[self._c_page]
                self._next_page(self.c_record)
                idx = self.c_record - self.res["response"]["start"]
                row = self.res["response"]["docs"][idx]
            except IndexError:
                self.done = True
                raise StopIteration()
        self.c_record = self.c_record + 1
        return self.process_row(row)


# =========================================================================


class SolrValuesResponseIterator(object):
    """Iterates over a Solr get values response.

    This returns a list of distinct values for a particular field.

    """

    def __init__(self, client, field, page_size=1000, **query_dict):
        """Initialize.

        @param client(SolrConnection) An instance of a solr connection to use.
        @param field(string) name of the field from which to retrieve values
        @param q(string) The Solr query to restrict results
        @param fq(string) A facet query, restricts the set of rows that q is applied to
        @param fields(string) A comma delimited list of field names to return
        @param page_size(int) Number of rows to retrieve in each call.

        """

        self.client = client
        self.field = field
        self.page_size = page_size
        self.query_dict = query_dict

        self.c_record = 0
        self.res = None
        self.done = False
        self.index = None

        self._next_page(self.c_record)

    def __iter__(self):
        return self

    def _next_page(self, offset):
        """Retrieves the next set of results from the service."""
        log.debug("Iterator c_record={}".format(self.c_record))
        param_dict = self.query_dict.copy()
        param_dict.update(
            {
                "rows": "0",
                "facet": "true",
                "facet.limit": str(self.page_size),
                "facet.offset": str(offset),
                "facet.zeros": "false",
            }
        )
        resp_dict = self.client._post_query(**param_dict)
        try:
            self.res = resp_dict["facet_counts"]["facet_fields"][self.field]
            log.debug(self.res)
        except Exception:
            self.res = []
        self.index = 0

    def __next__(self):
        if self.done:
            raise StopIteration()
        if len(self.res) == 0:
            self.done = True
            raise StopIteration()
        try:
            row = [self.res[self.index], self.res[self.index + 1]]
            self.index = self.index + 2
        except IndexError:
            self._next_page(self.c_record)
            try:
                row = [self.res[self.index], self.res[self.index + 1]]
                self.index = self.index + 2
            except IndexError:
                self.done = True
                raise StopIteration()
        self.c_record = self.c_record + 1
        return row
