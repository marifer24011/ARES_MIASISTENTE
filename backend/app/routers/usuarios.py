
import pymysql
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from pwdlib import PasswordHash

from backend.app.database.connection import obtener_conexion


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
password_hash = PasswordHash.recommended()


class RegistroUsuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    correo: EmailStr
    contrasena: str = Field(min_length=8, max_length=128)


@router.post("/registro", status_code=201)
def registrar_usuario(datos: RegistroUsuario):
    conexion = None

    try:
        conexion = obtener_conexion()

        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id_usuario FROM usuarios WHERE correo = %s",
                (str(datos.correo),)
            )

            if cursor.fetchone():
                raise HTTPException(
                    status_code=409,
                    detail="Este correo ya está registrado"
                )

            hash_seguro = password_hash.hash(datos.contrasena)

            cursor.execute(
                """
                INSERT INTO usuarios (nombre, correo, password_hash)
                VALUES (%s, %s, %s)
                """,
                (
                    datos.nombre.strip(),
                    str(datos.correo),
                    hash_seguro
                )
            )

            id_usuario = cursor.lastrowid

        conexion.commit()

        return {
            "mensaje": "Usuario registrado correctamente",
            "id_usuario": id_usuario
        }

    except pymysql.IntegrityError:
        if conexion:
            conexion.rollback()

        raise HTTPException(
            status_code=409,
            detail="Este correo ya está registrado"
        )

    finally:
        if conexion:
            conexion.close()


class InicioSesion(BaseModel):
    correo: EmailStr
    contrasena: str


@router.post("/login")
def iniciar_sesion(datos: InicioSesion):
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_usuario, nombre, correo, password_hash
                FROM usuarios
                WHERE correo = %s
                """,
                (str(datos.correo),)
            )

            usuario = cursor.fetchone()

            # Verificar credenciales sin revelar si existe el correo
            if (
                not usuario
                or not usuario["password_hash"]
                or not password_hash.verify(
                    datos.contrasena,
                    usuario["password_hash"]
                )
            ):
                raise HTTPException(
                    status_code=401,
                    detail="Correo o contraseña incorrectos"
                )

            cursor.execute(
                """
                UPDATE usuarios
                SET ultimo_acceso = NOW()
                WHERE id_usuario = %s
                """,
                (usuario["id_usuario"],)
            )

        conexion.commit()

        return {
            "mensaje": "Credenciales verificadas correctamente",
            "usuario": {
                "id_usuario": usuario["id_usuario"],
                "nombre": usuario["nombre"],
                "correo": usuario["correo"]
            }
        }

    finally:
        conexion.close()
