from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="X-Admin-Code", auto_error=False)

async def verify_admin_code(api_key: str = Security(api_key_header)):
    CORRECT_CODE = settings.admin_code

    if api_key != CORRECT_CODE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin code"
        )
    return api_key

