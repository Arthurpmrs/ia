from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chatbot.dialogue_manager import DialogueManager
from models.inference import run_diagnosis
from explainability.explainer import explain_diagnosis
import pathlib

app = FastAPI()

class SymptomInput(BaseModel):
    message: str

chatbot = DialogueManager()

@app.post("/chat")
async def chat(input: SymptomInput):
    user_message = input.message
    chatbot_reply, structured_data, ready_for_diagnosis = chatbot.process_message(user_message)
    if ready_for_diagnosis:
        diagnosis = run_diagnosis(structured_data)
        explanation = explain_diagnosis(structured_data, diagnosis)
        return {
            "chatbot_reply": chatbot_reply,
            "diagnosis": diagnosis,
            "explanation": explanation
        }
    return {"chatbot_reply": chatbot_reply}

@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = pathlib.Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))

app.mount("/static", StaticFiles(directory="./static"), name="static")