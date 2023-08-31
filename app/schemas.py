from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id:int = 0
    username:str
    password:str
    rol:str

    class Config:
        orm_mode=True

class UserUpdate(BaseModel):
    rol:str

    class Config:
        orm_mode=True

class Respuesta(BaseModel):
    mensaje:str

class UserToken(BaseModel):
    username:str
    password:str

    class Config:
        orm_mode=True

class Consultas(BaseModel):
    id:int = 0
    id_user:int = 0
    date:str
    search:str

    class Config:
        orm_mode=True

class ConsultasFecha(BaseModel):
    tipo: str
    fecha_inicio: str
    fecha_fin:str
    orden: str

class ConsultasBusqueda(BaseModel):
    tipo: str
    orden: str