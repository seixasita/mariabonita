from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/pagina", response_class=HTMLResponse)
def pagina():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Página da Fazenda</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f0f8ff; }
                h1 { color: #2c3e50; }
                p { font-size: 18px; }
                ul { list-style-type: square; }
                button {
                    background-color: #3498db;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>
        <body>
            <h1>Bem-vindo à Fazenda MARIA BONITA.</h1>
            <p>Olá, BROKA! Esta é uma página simples servida pelo FastAPI.</p>
            <p>Veja algumas atividades:</p>
            <ul>
                <li>Controle de animais</li>
                <li>Cadastro de insumos</li>
                <li>Relatórios de produção</li>
            </ul>
            <button onclick="alert('Você clicou no botão!')">Clique aqui</button>
        </body>
    </html>
    """
    return html_content
