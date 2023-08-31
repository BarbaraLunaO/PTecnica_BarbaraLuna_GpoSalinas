from fastapi import APIRouter, Header
from requests import get
from app.middlewares.verify_token_route import VerifyTokenRoute
import app.models as models,app.schemas as schemas
from datetime import datetime
from app.conexion import SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.functions_jwt import validate_token
from sqlalchemy import asc, desc, and_

users_verificated = APIRouter(route_class=VerifyTokenRoute)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@users_verificated.post("/weather/key/")
def get_key(lugar: str, Authorization: str = Header, db:Session=Depends(get_db)):
    fecha = datetime.now()
    fecha_str = fecha.strftime("%d-%m-%Y %H:%M")
    
    if Authorization:
        usuario = validate_token(Authorization, output=True)
        consulta = models.Consultas(id_user=usuario["idTyped"], date = fecha_str, search= lugar)
        db.add(consulta)
        db.commit()
        db.refresh
    else:
        return {"message": "Authorization header is missing."}

    return get(f'http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey=%09PN9N6NdGl8iIsHh3LYAAkwTcca5y5CsI&q={lugar}').json()

@users_verificated.post("/weather/forecast")
def get_forecast(key: str):
    return get(f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{key}?apikey=PN9N6NdGl8iIsHh3LYAAkwTcca5y5CsI").json()

@users_verificated.post("/consultaDB")
def consultar_datos(consulta:schemas.ConsultasBusqueda or schemas.ConsultasFecha, db:Session=Depends(get_db)):
    #consulta_db = db.query(models.Consultas).all()

    try:
        if isinstance(consulta, schemas.ConsultasFecha):
            fecha_inicio = datetime.strptime(consulta.fecha_inicio, '%d-%m-%Y')
            fecha_fin = datetime.strptime(consulta.fecha_fin, '%d-%m-%Y')

            consulta_db = db.query(models.Consultas).filter(and_(models.Consultas.date >= fecha_inicio, models.Consultas.date <= fecha_fin))

            if consulta.orden == 'asc':
                consulta_db = db.query(models.Consultas).order_by(asc(models.Consultas.date))
            elif consulta.orden == 'desc':
                consulta_db = db.query(models.Consultas).order_by(desc(models.Consultas.date))
    
        elif isinstance(consulta, schemas.ConsultasBusqueda):
            if consulta.orden == 'asc':
                consulta_db = db.query(models.Consultas).order_by(asc(models.Consultas.search))
            elif consulta.orden == 'desc':
                consulta_db = db.query(models.Consultas).order_by(desc(models.Consultas.search))
        else:
            raise ValueError("Tipo de consulta no válido")
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

    resultados = consulta_db.all()
    return resultados

