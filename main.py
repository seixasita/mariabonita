from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
import re
from fastapi import UploadFile, File
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def startup_event():
    create_user_table()

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_user_table():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT UNIQUE,
            username TEXT UNIQUE,
            name TEXT,
            email TEXT UNIQUE,
            birthdate TEXT,
            password TEXT
        )
        """
    )
    conn.commit()
    conn.close()


create_user_table()

def create_custos_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS custos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            data TEXT,
            tipo_custo TEXT,
            categoria TEXT,
            valor REAL,
            observacoes TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

create_custos_table()


def verify_cpf(cpf: str) -> bool:
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    # Validação básica do CPF
    def calc_digit(digs):
        s = sum((len(digs)+1 - i)*int(v) for i,v in enumerate(digs))
        r = 11 - s % 11
        return r if r < 10 else 0
    d1 = calc_digit(cpf[:9])
    d2 = calc_digit(cpf[:9] + str(d1))
    return cpf[-2:] == f"{d1}{d2}"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = request.session.get("user")
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/cadastro", response_class=HTMLResponse)
def cadastro_form(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request, "error": None})

@app.post("/cadastro", response_class=HTMLResponse)
@app.post("/cadastro", response_class=HTMLResponse)
def cadastro(request: Request,
             cpf: str = Form(...),
             username: str = Form(...),
             name: str = Form(...),
             email: EmailStr = Form(...),
             birthdate: str = Form(...),
             password: str = Form(...),
             confirm_password: str = Form(...)):

    if not verify_cpf(cpf):
        return templates.TemplateResponse("cadastro.html", {"request": request, "error": "CPF inválido."})
    if password != confirm_password:
        return templates.TemplateResponse("cadastro.html", {"request": request, "error": "As senhas não conferem."})

    hashed_password = pwd_context.hash(password)

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (cpf, username, name, email, birthdate, password) VALUES (?, ?, ?, ?, ?, ?)",
            (cpf, username, name, email, birthdate, hashed_password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return templates.TemplateResponse("cadastro.html", {"request": request, "error": "CPF, email ou usuário já cadastrado."})
    finally:
        conn.close()

    return RedirectResponse(url="/sucesso", status_code=status.HTTP_303_SEE_OTHER)
  
@app.get("/sucesso", response_class=HTMLResponse)
def sucesso(request: Request):
    return templates.TemplateResponse("sucesso.html", {"request": request, "mensagem": "Cadastro realizado com sucesso! Agora faça login."})


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, identificador: str = Form(...), password: str = Form(...)):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE cpf = ? OR username = ?", (identificador, identificador)
    ).fetchone()
    conn.close()
    
    if not user or not pwd_context.verify(password, user["password"]):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Usuário/CPF ou senha inválidos."})

    request.session["user"] = {
        "id": user["id"],
        "name": user["name"],
        "cpf": user["cpf"]
    }
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/noticias", response_class=HTMLResponse)
def noticias(request: Request):
    return templates.TemplateResponse("noticias.html", {"request": request})

@app.get("/sobre", response_class=HTMLResponse)
def sobre(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request})


@app.get("/teste", response_class=HTMLResponse)
def teste_navbar(request: Request):
    return templates.TemplateResponse("teste_navbar.html", {"request": request})

    from fastapi import HTTPException

@app.get("/perfil", response_class=HTMLResponse)
def perfil(request: Request):
    user = request.session.get("user")
    if not user:
        # Não logado, redireciona para login
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("perfil.html", {"request": request, "user": user})

@app.get("/custos", response_class=HTMLResponse)
def listar_custos(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    conn = get_db()
    custos = conn.execute("SELECT * FROM custos WHERE user_id = ?", (user["id"],)).fetchall()
    conn.close()

    return templates.TemplateResponse("custos.html", {"request": request, "custos": custos, "user": user, "error": None})

from datetime import datetime

@app.post("/custos", response_class=HTMLResponse)
def adicionar_custo(request: Request,
                   data: str = Form(...),
                   tipo_custo: str = Form(...),
                   categoria: str = Form(...),
                   valor: float = Form(...),
                   observacoes: str = Form("")):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # Aqui você pode fazer validações simples, como formato da data
    try:
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        error = "Data inválida. Use o formato YYYY-MM-DD."
        return templates.TemplateResponse("custos.html", {"request": request, "error": error, "custos": [], "user": user})

    conn = get_db()
    conn.execute(
        "INSERT INTO custos (user_id, data, tipo_custo, categoria, valor, observacoes) VALUES (?, ?, ?, ?, ?, ?)",
        (user["id"], data, tipo_custo, categoria, valor, observacoes)
    )
    conn.commit()
    conn.close()

    return RedirectResponse(url="/custos", status_code=status.HTTP_303_SEE_OTHER)

from fastapi import UploadFile, File
import pandas as pd
from io import BytesIO

@app.post("/upload-custos")
def upload_custos(request: Request, file: UploadFile = File(...)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    contents = file.file.read()
    df = pd.read_excel(BytesIO(contents))

    # Espera colunas exatas com esses nomes:
    required_columns = {'Data', 'Tipo de Custo', 'Categoria', 'Valor (R$)', 'Observações'}
    if not required_columns.issubset(df.columns):
        return templates.TemplateResponse("custos.html", {
            "request": request,
            "user": user,
            "error": "Planilha inválida. Certifique-se de que as colunas estão corretas.",
            "custos": []
        })

    conn = get_db()
    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO custos (user_id, data, tipo_custo, categoria, valor, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user["id"],
            str(row['Data']),
            str(row['Tipo de Custo']),
            str(row['Categoria']),
            float(row['Valor (R$)']),
            str(row.get('Observações', ''))
        ))
    conn.commit()
    conn.close()

    return RedirectResponse(url="/custos", status_code=303)

@app.get("/relatorio_custos", response_class=HTMLResponse)
def relatorio_custos(request: Request, filtro: str = "30", data_inicio: str = "", data_fim: str = ""):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    from datetime import datetime, timedelta

    conn = get_db()

    hoje = datetime.today().date()

    if filtro == "todos":
        query = "SELECT * FROM custos WHERE user_id = ?"
        params = (user["id"],)
    elif filtro == "personalizado" and data_inicio and data_fim:
        query = "SELECT * FROM custos WHERE user_id = ? AND data BETWEEN ? AND ?"
        params = (user["id"], data_inicio, data_fim)
    else:
        try:
            dias = int(filtro)
            data_limite = hoje - timedelta(days=dias)
            query = "SELECT * FROM custos WHERE user_id = ? AND data >= ?"
            params = (user["id"], data_limite.isoformat())
        except ValueError:
            # Se filtro for inválido, assume todos
            query = "SELECT * FROM custos WHERE user_id = ?"
            params = (user["id"],)

    custos = conn.execute(query, params).fetchall()
    conn.close()

    # Cálculo de totais
    totais_categoria = {}
    totais_tipo = {}
    total_geral = 0

    for custo in custos:
        categoria = custo["categoria"]
        tipo = custo["tipo_custo"]
        valor = custo["valor"]

        totais_categoria[categoria] = totais_categoria.get(categoria, 0) + valor
        totais_tipo[tipo] = totais_tipo.get(tipo, 0) + valor
        total_geral += valor

    return templates.TemplateResponse("relatorio_custos.html", {
        "request": request,
        "user": user,
        "custos": custos,
        "totais_categoria": totais_categoria,
        "totais_tipo": totais_tipo,
        "total_geral": total_geral,
        "filtro": filtro,
        "data_inicio": data_inicio,
        "data_fim": data_fim
    })

# formato brasileiro moeda
import locale

# Define localidade para formato brasileiro
#locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Filtro personalizado para Jinja2
def format_brl(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")



templates.env.filters["format_brl"] = format_brl


