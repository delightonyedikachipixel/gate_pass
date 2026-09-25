

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app import models

from app.routers import (
    user_routers,
    visitor,
    vehicle,
    gate_router,
    gate_pass_router,
    gate_log_router,
)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gate Pass System",
    description="Visitor & vehicle gate pass management API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routers.router)
app.include_router(visitor.router)
app.include_router(vehicle.router)
app.include_router(gate_router.router)
app.include_router(gate_pass_router.router)
app.include_router(gate_log_router.router)


@app.get("/", tags=["Security"])
def security_check():
    return {"status": "ok", "service": "gate-pass-system"}