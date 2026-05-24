from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.inventory import router as inventory_router
from app.database import engine, Base
from app.routes.ai import router as ai_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory_router)
app.include_router(ai_router)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def home():
    return {"message": "SmartStock AI Backend Running"}