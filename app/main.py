from fastapi import FastAPI
from app.routes import supporters
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine 

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Tymek2026",
    version="1.0",
    openapi_prefix="/tymek2026/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(supporters.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)