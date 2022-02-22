from fastapi import FastAPI

from api.routes.domain import router as DomainRouter
from api.routes.status import router as StatusRouter

app = FastAPI()


app.include_router(StatusRouter, tags=["Status"], prefix="/api/v1/status")
app.include_router(DomainRouter, tags=["Domain"], prefix="/api/v1/domain")
