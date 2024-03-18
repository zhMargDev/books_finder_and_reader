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

        # Create a dictionary to store the separated HTML text
        results = {
            "h3": [],
            "li": [],
            "a": []
        }

        # Iterate over the found elements and extract the text and href for each tag
        for h3 in books_finded_html.find_all("h3"):
            results["h3"].append(h3.text)

        for li in books_finded_html.find_all("li"):
            results["li"].append(li.text)

        for a in books_finded_html.find_all("a"):
            results["a"].append({"text": a.text, "href": a.get("href")})

        return results

