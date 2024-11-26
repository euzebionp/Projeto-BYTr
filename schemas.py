from pydantic import BaseModel

class AvaliacaoSchema(BaseModel):
    empresa_id: int
    avaliador_id: int
    nota: int
    comentario: str