from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1 import chat
from app.core.exceptions import FileUploadError
from app.api.v1 import knowledge_base
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database import create_tables, engine 
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    if engine:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.214:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(FileUploadError)
async def file_upload_exception_handler(request: Request, exc: FileUploadError):
    return JSONResponse(
        status_code=400,
        content={"message": f"File upload failed: {exc.detail}"},
    )


app.include_router(
    knowledge_base.router, prefix="/knowledgebase", tags=["knowledgebase"]
)
app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
