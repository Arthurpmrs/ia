from chatbot.dialogue_manager import DialogueManager
from explainability.explainer import explain_diagnosis
from models.inference import run_diagnosis
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


class SymptomInput(BaseModel):
    message: str


chatbot = DialogueManager()


@app.post("/chat")
async def chat(input: SymptomInput):
    user_message = input.message
    chatbot_reply, structured_data, ready_for_diagnosis = chatbot.process_message(
        user_message
    )
    if ready_for_diagnosis:
        diagnosis = run_diagnosis(structured_data)
        explanation = explain_diagnosis(structured_data, diagnosis)
        return {
            "chatbot_reply": chatbot_reply,
            "diagnosis": diagnosis,
            "explanation": explanation,
        }
    return {"chatbot_reply": chatbot_reply}
