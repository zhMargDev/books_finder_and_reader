import requests
import re

from tqdm import tqdm # Library for downloading files from other url
from bs4 import BeautifulSoup # Library for parsing html page from other flibusta.site

class Searching:
    website = "https://flibusta.site"

    def __init__(self):
        pass

    def search_books_by_name(self, books_name):
        # Searching all books from flibusta.site website
        html_content = requests.get(f"{self.website}/booksearch?ask={books_name}")

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

    def search_books_by_dict(self, books_dict):
        # Searching all books from flibusta.site website
        html_content = requests.get(f"{self.website}{books_dict}")
        # Convert to BeautifulSoup object for to make it easier to work with html
        soup = BeautifulSoup(html_content.text, "html.parser")

        # id=main this is the main part where all books are shown
        books_finded_html = soup.find(id='main')

        title = books_finded_html.find(class_='title')

        pages_count_html = books_finded_html.find(class_="pager") # Take pages if it not empty
        pages = ['']
        if pages_count_html is not None:
            pages_a_tags = pages_count_html.find_all('a', href=lambda href: '?page' in href if href else False)
            for a in pages_a_tags:
                if a['href'] not in pages:
                    pages.append(a['href'])
        results = {}
        books_data = []
        for page in pages:
            # this for is append to books_data all books from all pages, if page is not 1, it request for all pages and return that books
            if page == '':
                books_links = books_finded_html.find_all('a', href=lambda href: '/b/' in href if href else False)

                # Access the link details (text, href, etc.)
                for link in books_links:
                    link_text = link['href']
                    if link_text.count('/') == 2: # Checking if the link is book's reading link, and is not fb2, epub or other downloading link
                        books_data.append({
                            'text':link.text.strip(),# Get the text content of the anchor tag
                            'href':link['href'],# Get the href attribute value
                        })
            else:
                # If page is not '', find that page
                # Searching all books from flibusta.site website
                print(f"{self.website}{page}")
                html_content = requests.get(f"{self.website}{page}")
                # Convert to BeautifulSoup object for to make it easier to work with html
                soup = BeautifulSoup(html_content.text, "html.parser")

                # id=main this is the main part where all books are shown
                books_finded_html = soup.find(id='main')

                title = books_finded_html.find(class_='title')

                books_links = books_finded_html.find_all('a', href=lambda href: '/b/' in href if href else False)

                # Access the link details (text, href, etc.)
                for link in books_links:
                    link_text = link['href']
                    if link_text.count(
                            '/') == 2:  # Checking if the link is book's reading link, and is not fb2, epub or other downloading link
                        books_data.append({
                            'text': link.text.strip(),  # Get the text content of the anchor tag
                            'href': link['href'],  # Get the href attribute value
                        })

        results = {
            'title': title.text,
            'books': books_data
        }
        return results

    def view_book_desc(self, book_info):
        # Searching all books from flibusta.site website
        html_content = requests.get(f"{self.website}{book_info}")
        # Convert to BeautifulSoup object for to make it easier to work with html
        soup = BeautifulSoup(html_content.text, "html.parser")

        # id=main this is the main part where all books are shown
        book_html = soup.find(id='main')

        book_name = book_html.find('h1', class_='title').text.strip() # Take booke name
        pattern =  r"\(.*?\)"# Pattern for removing (fb2)
        book_name = re.sub(pattern, "", book_name) # Remove (fb2) or (pdf)

        # Try Necessary because the page may not have a book cover
        try:
            book_image = 'http://flibusta.site' + book_html.find('img', alt="Cover image")['src']
        except:
            book_image = ''

        book_desc = book_html.find("h2", text="Аннотация").next_sibling.next_sibling.text # Find description <p> tag

        #book_download_href = 'http://flibusta.site' + book_html.find('span', style="size").next_sibling.next_sibling['href'] # Book's downloading rl link
        books_downloading_url = ''
        all_a_tags = book_html.find_all('a')
        for a_href in all_a_tags:
            #Checking for the presence of a download button in pdf or fb2 format
            if book_info in a_href['href'] and '/fb2' in a_href['href'] or book_info in a_href['href'] and '/pdf' in a_href['href'] or book_info in a_href['href'] and '/download' in a_href['href']:
                books_downloading_url = 'http://flibusta.site' + a_href['href']
                break # whene url is added

        match = re.match(r".*/(.*)", books_downloading_url)
        print(match.group(1))

        book_information = {
            'title': book_name,
            'img':book_image,
            'desc': book_desc,
            'book_href':book_info,
            'donwload':books_downloading_url,
            'type':match.group(1)
        }

        return book_information

