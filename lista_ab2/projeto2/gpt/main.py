from decision_engine import classificar_candidato
from extractor import extrair_dados
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chatbot")
async def chatbot(request: Request):
    data = await request.json()
    texto_candidato = data.get("texto", "")
    texto_vaga = data.get("requisitos", "")

    dados_candidato = extrair_dados(texto_candidato)
    dados_vaga = extrair_dados(texto_vaga)

    categoria, justificativas = classificar_candidato(dados_candidato, dados_vaga)

    return JSONResponse(
        {
            "resposta": f"Classificação: {categoria}\nJustificativas:\n- "
            + "\n- ".join(justificativas)
        }
    )
