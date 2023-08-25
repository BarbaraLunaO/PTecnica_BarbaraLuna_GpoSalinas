from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL info: {usuario:root, contraseña: mysql1234, puerto:3306, nombre_db:db_registros_clima}
DATABASE_URL = "mysql+mysqlconnector://root:mysql1234@localhost:3306/db_registros_clima"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()