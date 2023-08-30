from jwt import encode, decode
from jwt import exceptions
from datetime import datetime, timedelta
from os import getenv
from fastapi.responses import JSONResponse
from decouple import config

def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(2) }, key=config("SECRET"), algorithm="HS256")
    return token


def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key=config("SECRET"), algorithms="HS256")
        decode(token, key=config("SECRET"), algorithms="HS256")
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"}, status_code=401)
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalidddd Token"}, status_code=401)
