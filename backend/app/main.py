import app.database.models_registry
from fastapi import FastAPI, APIRouter
from app.products.routes import router as products_router
from app.categories.routes import router as categories_router
from app.users.routes import router as auth_router
from app.reviews.routes import router as reviews_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions.exception_handlers import EXCEPTION_HANDLERS, limiter



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-CSRF-Token"],
)

# throttling 
app.state.limiter = limiter


# exception handlers
for exc_class, handler in EXCEPTION_HANDLERS:
    app.add_exception_handler(exc_class, handler)


# API v1 prefix
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(categories_router)
api_v1.include_router(products_router)
api_v1.include_router(reviews_router)

# Include API v1 + other routers
app.include_router(auth_router)
app.include_router(api_v1)