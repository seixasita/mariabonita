from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Fazenda Maria Bonita")

@app.get("/", response_class=HTMLResponse)
async def home():
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>🌿 Fazenda Maria Bonita</title>
      <style>
        body {
          margin: 0;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background: linear-gradient(135deg, #1b5e20, #388e3c);
          color: white;
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          text-align: center;
          padding: 2rem;
          animation: fadeIn 1.5s ease-in-out;
        }
        @keyframes fadeIn {
          from {opacity: 0; transform: translateY(20px);}
          to {opacity: 1; transform: translateY(0);}
        }
        h1 {
          font-size: 3rem;
          margin-bottom: 0.2rem;
          text-shadow: 0 0 10px #2e7d32;
        }
        p {
          font-size: 1.25rem;
          margin-top: 0;
          margin-bottom: 2rem;
          text-shadow: 0 0 5px #2e7d32;
        }
        button {
          background-color: #4caf50;
          border: none;
          color: white;
          padding: 1rem 2rem;
          font-size: 1.1rem;
          border-radius: 0.5rem;
          cursor: pointer;
          box-shadow: 0 4px 10px rgba(0,0,0,0.3);
          transition: background-color 0.3s ease;
        }
        button:hover {
          background-color: #357a38;
        }
        footer {
          margin-top: auto;
          padding: 1rem 0;
          font-size: 0.9rem;
          color: #c8e6c9;
          text-shadow: none;
        }
        a {
          color: #a5d6a7;
          text-decoration: none;
          font-weight: bold;
          transition: color 0.3s ease;
        }
        a:hover {
          color: #e8f5e9;
        }
      </style>
    </head>
    <body>
      <h1>🌿 Fazenda Maria Bonita</h1>
      <p>Sistema de gestão rural moderno e eficiente com <strong>INOVAÇÃO E SUSTENTABILIDADE</strong></p>
      <button onclick="alert('Bem-vindo à Fazenda Maria Bonita!')">Clique aqui!!!</button>
      <footer>
        <p>Quer saber mais? <a href="/sobre">Clique aqui para conhecer a fazenda</a></p>
      </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/sobre", response_class=HTMLResponse)
async def sobre():
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Sobre - Fazenda Maria Bonita</title>
      <style>
        body {
          margin: 0;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background: #e8f5e9;
          color: #2e7d32;
          min-height: 100vh;
          padding: 2rem;
          line-height: 1.6;
        }
        h1 {
          text-align: center;
          font-size: 2.5rem;
          margin-bottom: 1rem;
        }
        p {
          max-width: 700px;
          margin: 1rem auto;
          font-size: 1.1rem;
        }
        ul {
          max-width: 700px;
          margin: 1rem auto 2rem auto;
          padding-left: 1.2rem;
          list-style-type: square;
          font-size: 1.1rem;
        }
        a {
          display: block;
          max-width: 700px;
          margin: 0 auto;
          text-align: center;
          font-weight: bold;
          color: #1b5e20;
          text-decoration: none;
          margin-top: 2rem;
          font-size: 1.1rem;
          transition: color 0.3s ease;
        }
        a:hover {
          color: #4caf50;
        }
      </style>
    </head>
    <body>
      <h1>Sobre a Fazenda Maria Bonita</h1>
      <p>A Fazenda Maria Bonita é um projeto rural focado em inovação e sustentabilidade.</p>
      <p>Oferecemos:</p>
      <ul>
        <li>Controle completo do rebanho e insumos</li>
        <li>Relatórios detalhados de produção agrícola</li>
        <li>Sistemas modernos para gestão financeira rural</li>
        <li>Atendimento personalizado para produtores locais</li>
      </ul>
      <a href="/">← Voltar para a página inicial</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
