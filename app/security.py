from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader, APIKeyCookie


API_KEY = "8263d3f313876d7e000281b54336493c025dcdbc674d4c532d98109fb8ebb9eb"
API_KEY_NAME = "token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):
    if api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not credentials"
        )
