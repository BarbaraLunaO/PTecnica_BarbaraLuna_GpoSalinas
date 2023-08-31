from typing import List, Union
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from starlette.responses import RedirectResponse
import app.models as models,app.schemas as schemas
from .conexion import SessionLocal, engine
from sqlalchemy.orm import Session
from app.routes.auth import auth_routes
from app.routes.accuweather import users_verificated
from dotenv import load_dotenv

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_routes, prefix="/api")
app.include_router(users_verificated, prefix="/api")

load_dotenv()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get('/usuarios/', response_model=List[schemas.User])
def show_users(db:Session=Depends(get_db)):
    usuarios = db.query(models.User).all()
    return  usuarios

@app.post('/usuarios/')
def create_users(entrada:schemas.User ,db:Session=Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == entrada.username).first()

    if existing_user:
        return {"message": "Username ya ocupado"}, existing_user

    usuario = models.User(username=entrada.username, password=entrada.password, rol=entrada.rol)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@app.put('/usuarios/')
def update_users(usuario_id:int, entrada:schemas.UserUpdate ,db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter_by(id=usuario_id).first()

    if usuario:
        usuario.rol = entrada.rol
        db.add(usuario)
        db.commit()
        db.refresh
        return  {"message": "Rol actualizado"}, usuario
    else:
        return {"message": "Usuario no existente"}


@app.delete('/usuarios/', response_model=schemas.Respuesta)
def delete_users(usuario_id:int, db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter_by(id=usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        consultas = db.query(models.Consultas).filter_by(id_user=usuario_id).all()
        if consultas:
            db.delete(consultas)
            db.commit
        respuesta = schemas.Respuesta(mensaje="Ususario y Consultas eliminados exitosamente")
    else:
        respuesta = schemas.Respuesta(mensaje="Usuario no encontrado, ingrese un id disponible")
    return  respuesta

