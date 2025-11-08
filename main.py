from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import faq_router
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],   # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)
app.include_router(faq_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Intelligent FAQ Bot API"}
