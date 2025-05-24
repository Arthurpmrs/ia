from pydantic import BaseModel


class EvaluationResult(BaseModel):
    decision: str  # "Aprovado", "Aprovado parcialmente", "Reprovado"
    justification: str
    confidence: float
