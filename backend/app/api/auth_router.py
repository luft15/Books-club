# backend/app/api/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin
from app.schemas.token_schema import Token
from app.core.dependencies import get_auth_service, get_current_user
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    existing = auth_service.user_service.get_by_username(user_data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    existing_email = auth_service.user_service.get_by_email(user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return auth_service.register(user_data)

# @router.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
#     result = auth_service.login(form_data.username, form_data.password)
#     if not result:
#         raise HTTPException(status_code=401, detail="Incorrect username or password")
#     return result

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    login_data = UserLogin(username=form_data.username, password=form_data.password)
    result = auth_service.login(login_data)
    if not result:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return result

@router.post("/login-json", response_model=Token)
def login_json(login_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    result = auth_service.login(login_data)
    if not result:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return result

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user
