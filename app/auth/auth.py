from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv
from pathlib import Path
import os
import bcrypt

# Load .env from app/.env
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path)

# Setup
security = HTTPBasic()

# Load credentials
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD_HASH = os.getenv("BASIC_AUTH_PASSWORD_HASH")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):

    correct_username = credentials.username == BASIC_AUTH_USERNAME

    try:
        correct_password = verify_password(
            credentials.password, BASIC_AUTH_PASSWORD_HASH)
    except Exception as e:

        correct_password = False

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
