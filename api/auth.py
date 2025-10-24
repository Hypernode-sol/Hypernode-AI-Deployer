from __future__ import annotations
import os
from typing import Optional
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
import jwt

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
HTTP_BEARER = HTTPBearer(auto_error=False)

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
API_KEY = os.getenv("API_KEY", None)


def verify_api_key(api_key: Optional[str]) -> Optional[str]:
    if API_KEY is None:
        # If API_KEY is unset, accept no API key auth
        return None
    if api_key and api_key == API_KEY:
        return "apikey:user"
    return None


def verify_bearer_token(credentials: Optional[HTTPAuthorizationCredentials]) -> Optional[str]:
    if not credentials:
        return None
    if credentials.scheme.lower() != "bearer":
        return None
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        sub = payload.get("sub") or "jwt:user"
        return str(sub)
    except Exception as exc:
        return None


async def auth_required(api_key: Optional[str] = Depends(API_KEY_HEADER),
                        bearer: Optional[HTTPAuthorizationCredentials] = Depends(HTTP_BEARER)) -> str:
    """Accept either a valid X-API-Key or a valid Bearer JWT.
    Returns a 'principal' string (e.g., subject/user id) for downstream usage.
    """
    principal = verify_api_key(api_key) or verify_bearer_token(bearer)
    if not principal:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide X-API-Key or Bearer token.",
        )
    return principal


def mint_demo_token(sub: str = "demo-user", ttl_minutes: int = 60) -> str:
    now = datetime.utcnow()
    payload = {"sub": sub, "iat": int(now.timestamp()), "exp": int((now + timedelta(minutes=ttl_minutes)).timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
