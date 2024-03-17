import requests

from bs4 import BeautifulSoup

class Searching:
    website = "https://flibusta.site/booksearch?"

    def __init__(self):
        pass

    def search_books_by_name(self, books_name):
        # Searching all books from flibusta.site website
        response = requests.get(f"{self.website}ask={books_name}")
        print(response.text)

        return True

