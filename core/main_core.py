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
        results = []

        # Iterate over the found elements and extract the text and href for each tag
        for h3 in books_finded_html.find_all("h3"):
            result_data = {
                'title': '',
                'books': [],
            }
            result_data['title'] = h3.text

            for li in books_finded_html.find_all("li"):
                if 'серии' in h3.text and 'книг' in li.text: #Append books series
                    for a in li.find_all('a'):
                        result_data['books'].append({
                            'book_title': li.text,
                            'href': a.get("href")
                        })
                        break
                elif 'книги' in h3.text and 'книг' not in li.text: # Append books
                    for a in li.find_all('a'):
                        result_data['books'].append({
                            'book_title': li.text,
                            'href': a.get("href")
                        })
                        break

            results.append(result_data)

        return results

