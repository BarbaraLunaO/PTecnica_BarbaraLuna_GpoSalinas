# API REST DE CONSULTA DEL CLIMA

Esta API REST permite realizar operaciones de consulta (Crear, Leer, Actualizar y Eliminar) para el registro de usuarios. Además, una vez que un usuario ha sido verificado mediante JWT, la API es capaz de consultar una fuente externa de datos climáticos.

## Instalación

Para comenzar, asegúrate de crear un entorno virtual con Python 3 y luego instala las siguientes dependencias:

```bash
pip install fastapi[all]
pip install sqlalchemy
pip install mysql
pip install mysql-connector-python
pip install uvicorn
pip install pyjwt
pip install decouple
pip install cryptography
```

## Contribuciones

¡Apreciamos las contribuciones! Si deseas realizar cambios importantes, por favor, abre un problema primero para discutir lo que te gustaría cambiar. Asegúrate de actualizar las pruebas según corresponda.

## Licencia

Este proyecto está bajo la Licencia [MIT](https://choosealicense.com/licenses/mit/).
