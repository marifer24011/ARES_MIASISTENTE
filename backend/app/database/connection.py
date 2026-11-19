
import os
import pymysql
from pymysql.cursors import DictCursor


def obtener_conexion():
    conexion = pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset="utf8mb4",
        cursorclass=DictCursor,
        connect_timeout=5
    )

    return conexion
