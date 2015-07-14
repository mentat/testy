__author__ = 'mentat'

import re
import json
import urllib2
import logging
import HTMLParser


class ChatParser(object):
    """
    A simple class to wrap string parsing functionality for chat messages.
    """

    def __init__(self):
        super(ChatParser, self).__init__()

        # Compile the needed regex objects
        self.url_re = re.compile(r'https?://[a-zA-Z0-9\./]+')
        self.emoticon_re = re.compile(r'\(([a-zA-Z0-9]{,15})\)')
        self.mention_re = re.compile(r'@(\w+)', re.U)
        self.title_re = re.compile(r'<title>([^<]*)</title>', re.M | re.U | re.I)

    def _parse_urls(self, input_string):
        # Parse out URLs and attempt to fetch title data, return a list of dicts

        urls = []

        for url in self.url_re.findall(input_string):

            url_data = {"url": url, "title": ""}

            try:
                # Open url with 5 second timeout
                f = urllib2.urlopen(url, timeout=5)
            except urllib2.HTTPError as e:
                # Silently log error and continue, maybe we are offline
                logging.debug(e)

                urls.append(url_data)

                continue

            # Only read page 1000 bytes at a time to limit network access when we
            # are only looking for title.  Slight optimization for large HTML files
            # and slow networks.
            html = u''

            while True:
                chunk = f.read(1000)

                if chunk == "":
                    break
                else:
                    html = u'%s%s' % (html, chunk)

                html_match = self.title_re.search(html)

                if html_match:
                    # Fix HTML entities and elide as needed.
                    h = HTMLParser.HTMLParser()
                    title = h.unescape(html_match.group(1))
                    url_data["title"] = self._simple_elide(title)
                    break

            urls.append(url_data)
            return urls

    def _parse_mentions(self, input_string):
        # Parse the @mentions from an input string and return the username
        # sans the "@" as a list. Returns a list of strings.

        return self.mention_re.findall(input_string)

    def _parse_emoticons(self, input_string):
        # Parse any emoticons of the format "(emoticon)" with the caveat that
        # the emoticon identifier cannot be longer than 15 characters.
        # Returns a list of strings.

        return self.emoticon_re.findall(input_string)

    def _simple_elide(self, input_string, max_length=50):
        # A naive function to truncate a string and add an ellipsis. Returns a string.

        if len(input_string) > max_length:
            last_space = input_string.rfind(" ", 0, 46)

            if last_space == -1:
                # Bummer, big hammer, a more elegant solution would have looked
                # for word-boundaries instead, but I assume this is simple enough
                # for the purpose of this exercise.
                return u"%s..." % input_string[0:46]
            else:
                return u"%s..." % input_string[0:last_space]
        else:
            return input_string

    def parse(self, input_string):
        # Parse the given __input_string__ and return a JSON string
        # representation of the meta-data elements.

        result = {}

        urls = self._parse_urls(input_string)

        if urls:
            result['links'] = urls

        mentions = self._parse_mentions(input_string)

        if mentions:
            result['mentions'] = mentions

        emoticons = self._parse_emoticons(input_string)

        if emoticons:
            result['emoticons'] = emoticons

        return json.dumps(result)

if __name__ == "__main__":
    # Allow command line usage
    import sys

    if len(sys.argv) == 2:
        c = ChatParser()
        print c.parse(sys.argv[1])
    else:
        print "parser.py <input string>"
        sys.exit(1)
