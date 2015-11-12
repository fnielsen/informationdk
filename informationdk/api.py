"""Web interface to information.dk.

Usage:
  api.py <id>

"""

from __future__ import division, print_function

import json

from lxml import etree

import requests


BASE_URL = 'http://www.information.dk'


class Article(object):
    """Represents an article from www.information.dk."""

    def __init__(self, html):
        """Setup HTML parsing."""
        self.html = html
        self.tree = etree.HTML(self.html)
        self.extract()

    def extract(self):
        """Extract elements from article HTML."""
        self.authors = self.extract_authors()
        self.body = self.extract_body()
        self.title = self.extract_title()

    def extract_authors(self):
        """Extract list of authors from HTML."""
        element = self.tree.xpath("//ul[@class='byline inline']")[0]
        authors = [text for text in element.itertext()]
        return authors

    def extract_body(self):
        """Extract article body from HTML."""
        element = self.tree.xpath("//div[@class='field field-name-body']")[0]
        return " ".join([text for text in element.itertext()])

    def extract_title(self):
        """Extract article title from HTML."""
        return [text for text in self.tree.xpath("//h1")[0].itertext()][0]

    def to_dict(self):
        """Convert object to dict."""
        return {
            'authors': self.authors,
            'title': self.title,
            'body': self.body
        }

    def to_json(self):
        """Convert object to JSON."""
        return json.dumps(self.to_dict())


class API(object):
    """API to www.information.dk."""

    def article_from_id(self, id):
        """Return structured information from article.

        Example
        -------
        >>> api = API()
        >>> article = api.article_from_id(551683)
        >>> article['authors'] == ['Lasse Ellegaard']
        True

        """
        response = requests.get(BASE_URL + '/' + str(id))
        article = Article(response.content)
        return article.to_dict()


def main(args):
    """Handle command-line interface."""
    api = API()
    article = api.article_from_id(args['<id>'])
    print(json.dumps(article))


if __name__ == '__main__':
    import docopt

    main(docopt.docopt(__doc__))
