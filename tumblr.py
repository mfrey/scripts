#!/usr/bin/env python3.4

import os
import re
import time
import pprint
import argparse
import simplejson
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

PAGESIZE = 50  

class Tumblr:
    def __init__(self, name, location='/tmp'):
        self.name = name
        self.location = location

    def read(self,  identifier=None, start=0, max=2**31-1, type=None):
        if identifier:
            url = "http://%s.tumblr.com/api/read/json?id=%s" % (self.name, identifier)
            response = urlopen(url)
            page = response.read()
            match = re.match("^.*?({.*}).*$", page,re.DOTALL | re.MULTILINE )
            results = simplejson.loads(match.group(1))

            if len(results['posts']) == 0:
                return None 
        else:
            return TumblrIterator(self.name, start, max, type)

    def get_number_of_posts(self):
        try:
           request = Request('http://' + self.name + '.tumblr.com/api/read/json')
           response = urlopen(request)
           page = response.read()
           match = re.match("^.*?({.*}).*$", page, re.DOTALL | re.MULTILINE )
           results = simplejson.loads(match.group(1))
           return results['posts-total']

        except HTTPError as e:
            print((e.code))
        except URLError as e:
            print((e.args))

        return -1

    def download(self):
        posts = self.read()
        for post in posts:
            # TODO: add support for multi photo posts (check json api)
            if post['type'] == 'photo':
                self._download(post)

    def _download(self, post):
        savepath = self.location + '/' + os.path.basename(post['photo-url-1280'])

        try:
            url = Request(post['photo-url-1280'])
            request  = urlopen(url)
            with open(savepath, 'wb') as file:
                file.write(request.read())
        except HTTPError as e:
            print((e.code))
        except URLError as e:
            print((e.args))
        except ValueError:
            print("")


class TumblrIterator:
    def __init__(self, name, start, max, type):
        self.name = name
        self.start = start
        self.max = max
        self.type = type
        self.results = None
        self.index = 0

    def __iter__(self):
       return self

    def __next__(self):
        if not self.results or (self.index == len(self.results['posts'])):
            self.start += self.index
            self.index = 0
            url = "http://%s.tumblr.com/api/read/json?start=%s&num=%s" % (self.name, self.start, PAGESIZE)
            if self.type:
                url += "&type=" + self.type
            response = urlopen(url)
            page = response.read()

            match = re.match("^.*?({.*}).*$", page,re.DOTALL | re.MULTILINE | re.UNICODE)
            self.results = simplejson.loads(match.group(1))

        if (self.index >= self.max) or len(self.results['posts']) == 0:
            raise StopIteration

        self.index += 1

        return self.results['posts'][self.index-1] 


def main():
    parser = argparse.ArgumentParser(description='todo')

if __name__ == "__main__":
    main()
