from fastapi import APIRouter, HTTPException, Depends
from .hash_utils import hash_password, verify_password
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .model import SignupRequest
from config.db import get_user_by_username, create_user

router = APIRouter()
security = HTTPBasic()

def authenticate(creadentials:HTTPBasicCredentials=Depends(security)):
    user = get_user_by_username(creadentials.username)

    if not user or not verify_password(creadentials.password,user['password']):
        raise HTTPException(status_code=401,detail="Invalid creadentials")
    return {
        "username":user["username"],
        "role":user["role"]
    }

@router.post('/signup')
def signup(req:SignupRequest):
    existing_user = get_user_by_username(req.username)
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exists")
    
    hashed_pw = hash_password(req.password)
    create_user(req.username, hashed_pw, req.role)

    return {"message":"User Created Successfully"}


@router.get('/login')
def login(user = Depends(authenticate)):
    return{
        "message":f"Welcome {user['username']}",
        "role": user["role"]
    }