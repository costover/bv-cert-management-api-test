from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api import api_router
from src.core.config import settings
from src.core.database import engine


# 1. Define application lifecycle events (Startup and Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Actions to run when the server starts up
    yield
    # Actions to run when the server shuts down (e.g., closing open connections)
    await engine.dispose()


# 2. Instantiate the global FastAPI Application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_VERSION_STR}/openapi.json",
    lifespan=lifespan,
)


# 3. Apply Global Cross-Origin Resource Sharing (CORS) Middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
        allow_headers=["*"],  # Allows Authorization, Content-Type, etc.
    )


# 4. Include the central API router (Automates global /api/v1 prefixing)
app.include_router(api_router, prefix=settings.API_VERSION_STR)


# 5. Define a root health-check endpoint (Bypasses versioning for load balancers)
@app.get("/health", tags=["Health"])
async def health_check():
    """Confirms the web server application layer is responsive."""
    return {"status": "healthy"}