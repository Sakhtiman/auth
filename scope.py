# scope.py

from fastapi import Depends, HTTPException, status
from app.auth import decode_token

def get_user_scopes(token: str = Depends(decode_token)):
    scopes = token.get("scopes")
    if not scopes:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing scopes")
    return scopes

