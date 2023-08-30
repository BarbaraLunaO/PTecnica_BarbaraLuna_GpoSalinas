from sqlalchemy import Column, Integer, String, ForeignKey
from .conexion import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__= 'usuario'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20))
    password = Column(String(10))
    rol = Column(String(20))
    consultas = relationship("Consultas", back_populates="user")

class Consultas(Base):
    __tablename__= 'consultas'
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey('usuario.id'))
    date = Column(String(20))
    search = Column(String(20))
    user = relationship("User", back_populates="consultas")
