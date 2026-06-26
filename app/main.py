from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Physical Product Catalogue API",
    description=(
        "REST API for managing physical product records in a catalogue. "
        "Supports creating, reading, updating, and deleting products. "
        "All endpoints require an API key passed via the `X-API-Key` header."
    ),
    version="1.0.0",
    contact={"name": "API Support"},
    license_info={"name": "MIT"},
)

app.include_router(router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Physical Product Catalogue API is running."}
