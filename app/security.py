from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader


API_KEY = "8263d3f313876d7e000281b54336493c025dcdbc674d4c532d98109fb8ebb9eb"
API_KEY_ADMIN = "1f6de34d09fe9cac053046db03ea721410ae66a8356954a55523ac93a31ddc0a"
API_KEY_NAME = "token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_header_admin = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not credentials"
        )


async def get_api_key_admin(
    api_key_header_admin: str = Security(api_key_header_admin),
):
    if api_key_header_admin == API_KEY_ADMIN:
        return api_key_header_admin
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not credentials"
        )
