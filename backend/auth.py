from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import TokenData, Parent
from database import get_database
from config import settings
import logging

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash with fallback"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.warning(f'Password verification warning: {e}')
        return False  # Simple fallback

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def get_parent_by_email(email: str) -> Optional[dict]:
    """Get parent by email from database"""
    try:
        db = get_database()
        parent = await db.parents.find_one({"email": email})
        return parent
    except Exception as e:
        logger.error(f"Error fetching parent by email: {e}")
        return None

async def authenticate_parent(email: str, password: str) -> Optional[dict]:
    """Authenticate parent credentials"""
    parent = await get_parent_by_email(email)
    if not parent:
        return None
    if not verify_password(password, parent["hashed_password"]):
        return None
    return parent

async def get_current_parent(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current authenticated parent from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    parent = await get_parent_by_email(email=token_data.email)
    if parent is None:
        raise credentials_exception
    
    return parent

async def get_current_active_parent(current_parent: dict = Depends(get_current_parent)) -> dict:
    """Get current active parent"""
    if not current_parent.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive parent account")
    return current_parent

