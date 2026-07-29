from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile
from .vectorstores import load_vectorstores
from auth.routes import authenticate
import uuid

router = APIRouter()

@router.post('/upload_docs')
async def upload_docs(
    user = Depends(authenticate),
    file: UploadFile = File(...),
    role: str = Form(...)
):
    if user["role"] != "admin":
        raise HTTPException(403, "Only admin can upload file")

    doc_id = str(uuid.uuid4())
    await load_vectorstores([file], role, doc_id)

    return {
        "message": f"{file.filename} uploaded successfully",
        "doc_id": doc_id,
        "accessible_to": role
    }

