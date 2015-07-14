__author__ = 'mentat'


import unittest
import parser
import json


class TestChatParser(unittest.TestCase):
    """
    Test chat parser correctness.
    """

    # Test cases
    TESTS = {
        "@chris you around?": {
            "mentions": [
                "chris"
            ]
        },
        "Good morning! (megusta) (coffee)": {
            "emoticons": [
                "megusta",
                "coffee"
            ]
        },
        "Olympics are starting soon; http://www.nbcolympics.com": {
            "links": [
                {
                    "url": "http://www.nbcolympics.com",
                    "title": "NBC Olympics | Home of the 2016 Olympic Games..."
                }
            ]
        },
        "@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016": {
            "mentions": [
                "bob",
                "john"
            ],
            "emoticons": [
                "success"
            ],
            "links": [
                {
                    "url": "https://twitter.com/jdorfman/status/430511497475670016",
                    "title": "Justin Dorfman on Twitter: \"nice..."
                }
            ]
        }
    }

    def test_chat_strings(self):
        c = parser.ChatParser()

        for i, o in self.TESTS.iteritems():
            self.assertEquals(c.parse(i), json.dumps(o))

if __name__ == "__main__":
    unittest.main()
