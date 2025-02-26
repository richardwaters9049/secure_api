# app/auth.py
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Security(oauth2_scheme)):
    if token != "valid_token":  # Placeholder logic
        raise HTTPException(status_code=401, detail="Invalid token")
    return token
