from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.reference import router as reference_router

app = FastAPI(
    title="FX Pricing API",
    description="Real-time FX pricing engine — conventions, calendars, and pricing",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(reference_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
