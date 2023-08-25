from sqlalchemy import Column, Integer, String
from .conexion import Base

class User(Base):
    __tablename__= 'usuario'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20))
    password = Column(String(10))
    rol = Column(String(20))