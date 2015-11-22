#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib
from urlparse import urlparse
from rest_framework.reverse import reverse


class CommonTestMixin(object):

    def prepare_urls(self, path_name, query={}, *args, **kwargs):
        url = reverse(path_name, *args, **kwargs)
        if query:
          url += '?' + urllib.urlencode(query)
        parsed = urlparse(url)
        return url, parsed

    def load_response(self, response):
        return json.loads(response.content)


    def assertResponse(self, original, created, exclude=None):
        exclude = tuple('id',) if exclude is None else exclude
        for k, v in original.iteritems():
            if k in exclude:
                continue
            self.assertEqual(created[k], v)