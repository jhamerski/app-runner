import json
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException

load_dotenv()


def get_api_key():
    # Local: lê do .env
    local_key = os.getenv("X_API_KEY")
    if local_key:
        return local_key

    # Produção: lê do Secrets Manager
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name="us-east-2",
        )
        response = client.get_secret_value(SecretId="app-runner")
        secret = json.loads(response["SecretString"])
        return secret.get("X_API_KEY")
    except Exception:
        return None


API_KEY = get_api_key()

app = FastAPI()


def verify_api_key(x_apikey: str = Header(None)):
    if not API_KEY or not x_apikey or x_apikey != API_KEY:
        raise HTTPException(status_code=403, detail="API key inválida")


# Endpoint PROTEGIDO
@app.get("/")
def root(api_key: str = Depends(verify_api_key)):
    return {"message": "Olá do App Runner!!!"}


# Endpoint ABERTO (Para o App Runner validar o serviço)
@app.get("/health")
def health():
    return {"status": "healthy"}
