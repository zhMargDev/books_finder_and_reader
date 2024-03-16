from fastapi import Cookie, FastAPI, Request, HTTPException, Depends, Header, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


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