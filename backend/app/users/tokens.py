from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from fastapi import Response
from itsdangerous import URLSafeTimedSerializer


def create_access_token(user_id: int) -> str:
    """
    Crea un token di accesso per l'utente con l'ID specificato.
    """

    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE),
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def check_access_token(token: str) -> dict | None:
    """
    Verifica se il token di accesso è valido.
    """

    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    except jwt.ExpiredSignatureError:
        return None


def create_refresh_token(user_id: int, csrf_token: str) -> str:
    """
    Genera un nuovo token di refresh con i dati forniti includendo anche il csrf
    """

    expire = (
        datetime.now(timezone.utc) +
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE)
    )
    return jwt.encode(
        {"sub": str(user_id), "exp": expire, "csrf_token": csrf_token},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def check_refresh_token(token: str) -> dict | None:
    """
    Decodifica il token di refresh e restituisce i dati
    """

    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except Exception:
        return None


def create_csrf_token(user_id: str) -> str:
    serializer = URLSafeTimedSerializer(settings.CSRF_SECRET_KEY)
    return serializer.dumps(user_id, salt="csrf")


def check_csrf_token(token: str) -> str | None:
    serializer = URLSafeTimedSerializer(settings.CSRF_SECRET_KEY)
    try:
        # during as long as refresh token is valid
        # matching the expiration of the refresh token
        max_age_seconds = 60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE
        return serializer.loads(token, salt="csrf", max_age=max_age_seconds)
    except Exception:
        return None


def set_tokens(response: Response, refresh_token: str, csrf_token: str) -> None:
    """
    Setta nei cookie il refresh token e negli headers il csrf
    """

    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=True if settings.PRODUCTION else False,    
        samesite="none" if settings.PRODUCTION else "lax",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE,
        partitioned=True
    )

    response.headers["X-CSRF-Token"] = csrf_token


def delete_cookie_tokens(response: Response) -> None:
    """
    Svuota i campi dei cookie
    """

    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value="",
        max_age=0,
        expires=0,
        path="/",
        secure=True if settings.PRODUCTION else False,
        httponly=True,
        samesite="none" if settings.PRODUCTION else "lax",
        partitioned=True,
    )
