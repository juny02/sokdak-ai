import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from ulid import ULID

from core.setting import settings

security = HTTPBearer()


def decode_access_token(token: str) -> dict:
    """
    JWT Access Token을 검증하고 디코딩합니다.

    Args:
        token: JWT Access Token 문자열

    Returns:
        디코딩된 payload (dict)

    Raises:
        HTTPException: 토큰이 만료되었거나 유효하지 않은 경우
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> ULID:
    """
    HTTP Authorization 헤더에서 JWT 토큰을 추출하고 검증하여 사용자 ID를 반환합니다.

    Args:
        credentials: HTTP Bearer 토큰

    Returns:
        사용자 ID (ULID)

    Raises:
        HTTPException: 토큰이 없거나 유효하지 않은 경우
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    # Refresh token 거부
    token_type = payload.get("type")
    if token_type == "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token cannot be used for authentication",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: sub not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return ULID.from_str(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid userId format",
            headers={"WWW-Authenticate": "Bearer"},
        )
