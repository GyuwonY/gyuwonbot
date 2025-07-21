from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1 import documents, chat
from app.core.exceptions import FileUploadError

app = FastAPI()


@app.exception_handler(FileUploadError)
async def file_upload_exception_handler(request: Request, exc: FileUploadError):
    return JSONResponse(
        status_code=400,
        content={"message": f"File upload failed: {exc.detail}"},
    )


app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
