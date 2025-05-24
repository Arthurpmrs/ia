from chatbot.dialogue_manager import get_response
from explainability.explainer import explain_diagnosis
from fastapi import FastAPI, Request
from models.inference import run_diagnosis
from pydantic import BaseModel

app = FastAPI()


class SymptomInput(BaseModel):
    message: str


@app.post("/chat")
async def chat(input: SymptomInput):
    user_message = input.message
    chatbot_reply, structured_data = get_response(user_message)
    if structured_data:
        diagnosis = run_diagnosis(structured_data)
        explanation = explain_diagnosis(structured_data, diagnosis)
        return {
            "chatbot_reply": chatbot_reply,
            "diagnosis": diagnosis,
            "explanation": explanation,
        }
    return {"chatbot_reply": chatbot_reply}
