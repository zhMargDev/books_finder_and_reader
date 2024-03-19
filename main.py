from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from lxml import etree # Fb2 reader
from PyPDF2 import PdfReader # Pdf reader
from starlette.responses import RedirectResponse

# Import main_core file
import core.main_core as main_core


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Main page
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

# Open book page, and if downloading url is not empty, download a book
@app.get('/b/{book_id}/type={book_type}')
async def book(request: Request, book_id: int, book_type: str):

    if book_type == 'download':  # If book is pdf
        book_type_r = 'pdf'
        try:
            with open(f"/static/books/{book_id}.pdf", "rb") as f:
                reader = PdfReader(f)
                # Get number of pages (optional)
                num_pages = len(reader.pages)
                # Render the first page as an example
                page = reader.pages[0]
                html = page.extract_text()  # Extract text from the page
            return templates.TemplateResponse("book.html", {"request": request, "book_html": html})
        except FileNotFoundError:
            # Handle the case where the PDF file is not found
            return RedirectResponse(url="")

    elif book_type == 'fb2':  # If book is fb2
        book_type_r = 'fb2'
        try:
            with open(f"/static/books/{book_id}.{book_type}", "rb") as f:
                print(True)

                tree = etree.parse(f)
                html = etree.tostring(tree, method="html")
            return templates.TemplateResponse("book.html", {"request": request, "book_html": html})
        except FileNotFoundError:
            # Handle the case where the FB2 file is not found
            return RedirectResponse(url="")

        # Handle invalid book types or other errors
    return RedirectResponse(url="")

# Request to server for adding sessions so that the notification does not show anymore
@app.post("/block_notification")
async def block_notification(request: Request):
    response = Response(status_code=200)  # Create a response object
    response.set_cookie(
        key="block_notification",  # Set the cookie with the specified key
        value="true",  # Set its value to "true"
        expires=365 * 24 * 60 * 60,  # Set the expiration time to one year
        path="/",  # Make the cookie accessible from all paths on your domain
    )
    return response

# Parser for search book from flibusta.site website
@app.post("/search_book")
async def search_book(request: Request):
    books_name = await request.json()

    # Search and return finded books
    response_data = main_core.Searching().search_books_by_name(books_name)

    return response_data

#Search book by dict
@app.post("/search_book_by_dict")
async def search_book_by_dict(request: Request):
    dict_name = await request.json()

    # Search book by dict
    response_data = main_core.Searching().search_books_by_dict(dict_name)

    return response_data

# Search and response books insformation
@app.post('/view_book_desc')
async def view_book_desc(request: Request):
    book_ = await request.json()

    # Search book and response that book's information
    response_book = main_core.Searching().view_book_desc(book_)

    return response_book

