from tools.tools import *
# from tools import *
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone

router = APIRouter()

class Fanpage(BaseModel):
    name_fb: str

@router.post("/fp_data/")
async def param_facebook(data_re: Fanpage,access_token: str = Depends(oauth2_scheme)):
    print(data_re.name_fb)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    invalid_name_fb = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid name fanpage",
    )
    conn = create_connection()
    token_data = decode_bearer_token(access_token)
    _,user = get_user(conn, token_data.email)
    if user is None:
        raise credentials_exception
    
    name_fb = data_re.name_fb
    fb=get_fanpage(conn, name_fb)
    if fb is None:
        raise invalid_name_fb
    conn.close()
    return fb
