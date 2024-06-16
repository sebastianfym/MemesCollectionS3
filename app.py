from fastapi import APIRouter, FastAPI
import uvicorn
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from api.routers.public_router import router as public_router
from api.routers.buisnes_router import router as private_router
from api.view import buisnes_memes, public_memes

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your Project Name",
        version="1.0.0",
        description="This is a very cool project",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


v1 = APIRouter(prefix='/api/v1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

v1.include_router(public_router)
v1.include_router(private_router)
app.include_router(v1)

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
