from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Import main_core file
import core.main_core as main_core


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Main page
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

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