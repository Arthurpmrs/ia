from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .ai_model import evaluate_candidate
from .nlp_processor import CandidateInfoExtractor

extractor = CandidateInfoExtractor()

app = FastAPI()

# Configuração para servir arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class CandidateData(BaseModel):
    education: str
    experience_years: float
    technologies: List[str]
    languages: List[str]
    behavioral_interview_score: float
    role_requirements: Optional[dict] = None


@app.post("/api/evaluate")
async def evaluate(candidate: CandidateData):
    try:
        result = evaluate_candidate(candidate.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/extract-info")
async def extract_info(request: dict):
    try:
        text = request.get("text", "")
        result = extractor.extract_info(text)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
