from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs"  # Itt lesz érhető el a Swagger UI
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Fejlesztéshez jó a "*", élesben beállítható a weboldal domainjét
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Regisztráljuk a végpontokat
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Enterprise GenAI Document Assistant API is running!"}