#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib
from urlparse import urlparse
from rest_framework import status
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

    def chk_ok(self, response):
        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        except AssertionError:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def chk_bad_request(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def chk_not_found(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
