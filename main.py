
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI(title="Fazenda Maria Bonita")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

WHATSAPP_NUMBER = "5551999439856"  # Atualize para seu número

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "whatsapp_number": WHATSAPP_NUMBER,
        "page": "home"
    })

@app.get("/sobre", response_class=HTMLResponse)
async def sobre(request: Request):
    return templates.TemplateResponse("sobre.html", {
        "request": request,
        "whatsapp_number": WHATSAPP_NUMBER,
        "page": "sobre"
    })
