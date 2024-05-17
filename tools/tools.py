from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Union
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import psycopg2
import os
from fastapi import  HTTPException, status, Depends, APIRouter
import json

from dotenv import load_dotenv
load_dotenv('.env')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash the password
def get_password_hash(password):
    return pwd_context.hash(password)

def create_connection():
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                # pgbouncer=True
                                )
        print("Database connected successfully")
    except:
        print("Database not connected successfully")
    return conn

def create_cursor(conn):
    return conn.cursor()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None
    
class User(BaseModel):
    email: str
    full_name: Union[str, None] = None
    phone_number : Union[str, None] = None
    avatar : Union[str, None] = None
    gender : Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

class Fanpage(BaseModel):
    url: str
    follower: Union[int, None] = None
    avatar_fp: Union[str, None] = None

class FanpageInDB(Fanpage):
    user_id: int
    
def decode_bearer_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception
    
def get_user(conn, email: str):
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    result = cursor.fetchone()
    if result:
        return result[0],UserInDB(email=result[1],hashed_password=result[2],full_name=result[3],phone_number=result[4],avatar=result[5],gender=result[6])
    else:
        return None,None
    
class FanpageResponse(BaseModel):
    name_fb: str
    follower: str
    total_likes:int
    total_cmts : int
    rate_pos : int
    rate_neg : int
    rate_neu : int
    num_post : int

def get_fanpage(conn, name_fb: str):
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM fanpage WHERE name_fb = '{name_fb}'")
    result = cursor.fetchone()
    if result:
        return FanpageResponse(name_fb=result[2],follower=result[4],total_likes=result[5],total_cmts=result[6],rate_pos=result[7],rate_neg=result[8],rate_neu=result[9],num_post=result[10])
    else:
        return None

def check_dupli_user_or_email(conn, email: str):
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False  
    
def authenticate_user(conn, email: str, password: str):
    _,user = get_user(conn, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

