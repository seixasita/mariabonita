from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi.templating import Jinja2Templates
from datetime import datetime
import csv
import os

app = FastAPI()

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 config com variável global now()
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"])
)
env.globals["now"] = datetime.now

templates = Jinja2Templates(directory="templates")
templates.env = env

CSV_FILE = "usuarios.csv"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/sobre", response_class=HTMLResponse)
async def sobre(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request})

@app.get("/noticias", response_class=HTMLResponse)
async def noticias(request: Request):
    return templates.TemplateResponse("noticias.html", {"request": request})

@app.get("/cadastro", response_class=HTMLResponse)
async def cadastro_get(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request, "erro": None})

@app.post("/cadastro", response_class=HTMLResponse)
async def cadastro_post(
    request: Request,
    nome_completo: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    username: str = Form(...),
    senha: str = Form(...),
    senha2: str = Form(...)
):
    erros = []
    if senha != senha2:
        erros.append("As senhas não coincidem.")
    # Aqui pode adicionar validações extras

    if erros:
        return templates.TemplateResponse("cadastro.html", {"request": request, "erro": erros})

    existe = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome_completo", "email", "cpf", "data_nascimento", "username", "senha"])
        if not existe:
            writer.writeheader()
        writer.writerow({
            "nome_completo": nome_completo,
            "email": email,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "username": username,
            "senha": senha,
        })

    return RedirectResponse("/sucesso", status_code=303)

@app.get("/sucesso", response_class=HTMLResponse)
async def sucesso(request: Request):
    return templates.TemplateResponse("sucesso.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "erro": None})

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), senha: str = Form(...)):
    usuario_encontrado = False
    senha_correta = False

    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                csv_usuario = linha.get("username", "").strip().lower()
                csv_senha = linha.get("senha", "").strip()
                if csv_usuario == username.strip().lower():
                    usuario_encontrado = True
                    if csv_senha == senha.strip():
                        senha_correta = True
                    break

    if not usuario_encontrado or not senha_correta:
        return templates.TemplateResponse("login.html", {"request": request, "erro": "Usuário ou senha inválidos"})

    return templates.TemplateResponse("dashboard.html", {"request": request, "usuario": username})
