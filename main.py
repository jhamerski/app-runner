import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException

load_dotenv()

# Dica: No App Runner, o os.getenv lerá direto das "Environment Variables" do painel
API_KEY = os.getenv("X_API_KEY")

app = FastAPI()


def verify_api_key(x_apikey: str = Header(None)):  # Mudei para None para evitar erro de Header ausente antes da lógica
    if x_apikey != API_KEY:
        raise HTTPException(status_code=403, detail="API key inválida")


# Endpoint PROTEGIDO
@app.get("/")
def root(api_key: str = Depends(verify_api_key)):
    return {"message": "Olá do App Runner!"}


# Endpoint ABERTO (Para o App Runner validar o serviço)
@app.get("/health")
def health():
    return {"status": "healthy"}
