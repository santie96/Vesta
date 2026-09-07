from fastapi import Request, status
from fastapi.responses import JSONResponse
from .exceptions import *
from slowapi import Limiter
from fastapi.responses import JSONResponse
from slowapi.util import get_remote_address
from datetime import datetime, timezone
import time
from .schemas import RateLimitError
from slowapi.errors import RateLimitExceeded


async def not_found_handler(request: Request, exc: NotFoundException):
    """
    Exception handler for NotFoundException
    """
    
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

async def external_service_error_handler(request: Request, exc: ExternalServiceException):
    """
    Exception handler for ExternalServiceException
    """
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )    
    
async def validation_handler(request: Request, exc: ValidationException):
    """
    Exception handler for ValidationException (and its subclasses)
    """
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})    
    

async def already_exists_handler(request: Request, exc: Exception):
    """
    Exception handler for AlreadyExistsException
    """
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )
    
    
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


# ====================================
# ========  LIMITER  =================
# ====================================

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Custom rate limit handler returns 429 status code with reset time
    """

    limit_item, key_parts = request.state.view_rate_limit

    # reset timer + remaining attempts as a tuple
    reset_time, _ = request.app.state.limiter.limiter.get_window_stats(
        limit_item, *key_parts)

    # convert timestamp to datetime
    unlock_at = datetime.fromtimestamp(reset_time, tz=timezone.utc)

    payload = RateLimitError(
        error="Too many requests. Try again later.",
        unlock_at=unlock_at
    )

    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=payload.model_dump(mode="json"),
        headers={
            # str of max value (0 or any int value)
            # handling negative values from response
            "Retry-After": str(max(0, int(reset_time - time.time())))
        }
    )
    

EXCEPTION_HANDLERS = [
    (RateLimitExceeded, custom_rate_limit_handler),
    (NotFoundException, not_found_handler),
    (AlreadyExistsException, already_exists_handler),
    (ValidationException, validation_handler),
    (ExternalServiceException, external_service_error_handler),
    (Exception, internal_server_error_handler),
]