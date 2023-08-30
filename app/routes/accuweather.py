from fastapi import APIRouter, Header
from requests import get
from app.middlewares.verify_token_route import VerifyTokenRoute
import app.models as models
from datetime import datetime
from app.conexion import SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.functions_jwt import validate_token

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


