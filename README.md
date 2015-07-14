# Chat Line Parser

Parses a line from a chat and returns any meta-data as a JSON string.

## Author

Jesse Lovelace <jesse.lovelace@gmail.com>

## Command Line Usage

    parser.py <input string>

The output of the program will be a JSON encoded dictionary conforming to the
specification given below.

## Library Usage

    import parser

    >>> p = parser.ChatParser()
    >>> p.parse("This is a test (blah) @mentat http://google.com @bart")
    {"mentions": ["mentat", "bart"], "emoticons": ["blah"], "links": [{"url": "http://google.com", "title": "Google"}]}

## Specification

Please write, in Python, code that takes a chat message string and returns a
JSON string containing information about its contents. Special content to look
for includes:

 1. @mentions - A way to mention a user. Always starts with an '@' and ends
    when hitting a non-word character.
    (http://help.hipchat.com/knowledgebase/articles/64429-how-do-mentions-work-)
 2. Emoticons - For this exercise, you only need to consider 'custom' emoticons
    which are alphanumeric strings, no longer than 15 characters, contained in
    parenthesis. You can assume that anything matching this format is an
    emoticon. (https://www.hipchat.com/emoticons)
 3. Links - Any URLs contained in the message, along with the page's title.


For example, calling your function with the following inputs should result in
the corresponding return values.

_Input:_ "@chris you around?"

_Return (string):_

    {
      "mentions": [
        "chris"
      ]
    }

_Input:_ "Good morning! (megusta) (coffee)"

_Return (string):_

    {
      "emoticons": [
        "megusta",
        "coffee"
      ]
    }


_Input:_ "Olympics are starting soon; http://www.nbcolympics.com"

_Return (string):_

    {
      "links": [
        {
          "url": "http://www.nbcolympics.com",
          "title": "NBC Olympics | 2014 NBC Olympics in Sochi Russia"
        }
      ]
    }


_Input:_ "@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016"

_Return (string):_

    {
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
          "title": "Twitter / jdorfman: nice @littlebigdetail from ..."
        }
      ]
    }