from fastapi import APIRouter, HTTPException, status, Depends
from .schemas import LoginRequest, SignupRequest, Token
from .utils import hash_password, verify_password, create_access_token, get_current_parent
from ..db import get_db
from bson import ObjectId

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(payload: SignupRequest):
    db = get_db()
    if await db.parents.find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    doc = {"email": payload.email, "full_name": payload.full_name, "password_hash": hash_password(payload.password), "role": "parent"}
    res = await db.parents.insert_one(doc)
    access = create_access_token({"sub": str(res.inserted_id), "role": "parent"})
    return {"access_token": access}

@router.post("/login", response_model=Token)
async def login(payload: LoginRequest):
    db = get_db()
    parent = await db.parents.find_one({"email": payload.email})
    if not parent or not verify_password(payload.password, parent.get("password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access = create_access_token({"sub": str(parent["_id"]), "role": "parent"})
    return {"access_token": access}

@router.get("/me")
async def me(current = Depends(get_current_parent)):
    return current
