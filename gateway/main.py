from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os, requests

app = FastAPI(title="XBPNEUS API Gateway")

DJANGO_URL = os.getenv("DJANGO_URL", "http://web:8000")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{DJANGO_URL}/api/users/login/")

def validate_with_django(token: str):
    r = requests.post(f"{DJANGO_URL}/api/token/verify/", json={"token": token}, timeout=5)
    if r.status_code == 200:
        return True
    raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/me")
def me(token: str = Depends(oauth2_scheme)):
    validate_with_django(token)
    # Em ambiente real, você poderia chamar /api/users/me/ no Django e retornar os dados
    return {"status": "ok"}


@app.get('/health')
def health():
    return {'status':'ok','service':'gateway'}
