from fastapi import APIRouter, Header, Request
from pydantic import BaseModel, EmailStr
from app.functions_jwt import validate_token, write_token
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.params import Depends
from app.conexion import SessionLocal
import app.models as models,app.schemas as schemas

auth_routes = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserTyped(BaseModel):
    idTyped: int
    usernameTyped: str
    passwordTyped: str

@auth_routes.post("/writeToken")
def getToken(userTyped: UserTyped, db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter_by(username=userTyped.usernameTyped).first()
    print(usuario)
    if usuario is None:
        return JSONResponse(content={"message": "User not found"}, status_code=404)
    elif userTyped.idTyped != usuario.id:
        return JSONResponse(content={"message": "Incorrect id user"}, status_code=404)
    elif userTyped.passwordTyped != usuario.password:
        return JSONResponse(content={"message": "Incorrect Password"}, status_code=404)
    else:
        return write_token(userTyped.model_dump())

@auth_routes.post("/verify/token")
def verify_token(Authorization: str = Header):
    if Authorization:
        return validate_token(Authorization, output=True)
    else:
        return {"message": "Authorization header is missing."}
