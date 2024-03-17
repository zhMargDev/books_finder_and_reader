import requests

from bs4 import BeautifulSoup

class Searching:
    website = "https://flibusta.site/booksearch?"

    def __init__(self):
        pass

    def search_books_by_name(self, books_name):
        # Searching all books from flibusta.site website
        html_content = requests.get(f"{self.website}ask={books_name}")

        # Convert to BeautifulSoup object for to make it easier to work with html
        soup = BeautifulSoup(html_content.text, "html.parser")

        #id=main this is the main part where all books are shown
        books_finded_html = soup.find(id='main')

        # Removing unnecessary lines returned by div, form, h1, hr, br contain other unnecessary information
        for tag in books_finded_html.find_all(['div', 'form', 'h1', 'hr', 'br']):
            tag.extract()

        # Return div with h3, ul and li -> title and books and autors
        return books_finded_html.text

