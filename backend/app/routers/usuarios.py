
import pymysql
import os

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr, Field
from pwdlib import PasswordHash

from backend.app.database.connection import obtener_conexion

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from backend.app.security.sesiones import (
    generar_token_sesion,
    guardar_sesion
)

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

class InicioSesionGoogle(BaseModel):
    credential: str


@router.post("/login")
def iniciar_sesion(datos: InicioSesion, response: Response):
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


        # Generar y guardar la sesión del estudiante
        token = generar_token_sesion()
        guardar_sesion(usuario["id_usuario"], token)

        # Enviar una cookie segura al navegador
        response.set_cookie(
            key="ares_sesion",
            value=token,
            httponly=True,
            secure=False,  # Solo para desarrollo local con HTTP
            samesite="lax",
            max_age=8 * 60 * 60,
            path="/"
        )


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



    
@router.post("/google")
def iniciar_sesion_google(datos: InicioSesionGoogle, response: Response):
    # Verificar que Google esté configurado
    client_id = os.getenv("GOOGLE_CLIENT_ID")

    if not client_id:
        raise HTTPException(
            status_code=500,
            detail="Google no está configurado en el servidor"
        )

    # Verificar la autenticidad del token
    try:
        informacion = id_token.verify_oauth2_token(
            datos.credential,
            google_requests.Request(),
            client_id
        )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="La credencial de Google no es válida"
        )

    # Obtener los datos verificados de Google
    google_sub = informacion.get("sub")
    correo = informacion.get("email")
    nombre = informacion.get("name")
    foto_url = informacion.get("picture")

    if not google_sub or not correo or informacion.get("email_verified") is not True:
        raise HTTPException(
            status_code=401,
            detail="No se pudo verificar el correo de Google"
        )

    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            # Buscar al estudiante por su identificador de Google
            cursor.execute(
                "SELECT id_usuario FROM usuarios WHERE google_sub = %s",
                (google_sub,)
            )
            usuario = cursor.fetchone()

            if usuario:
                id_usuario = usuario["id_usuario"]

                cursor.execute(
                    """
                    UPDATE usuarios
                    SET ultimo_acceso = NOW()
                    WHERE id_usuario = %s
                    """,
                    (id_usuario,)
                )

            else:
                # Comprobar si el correo ya está registrado
                cursor.execute(
                    "SELECT id_usuario FROM usuarios WHERE correo = %s",
                    (correo,)
                )
                existente = cursor.fetchone()

                if existente:
                    raise HTTPException(
                        status_code=409,
                        detail="Este correo ya tiene una cuenta. Inicia sesión con tu contraseña."
                    )

                # Registrar una nueva cuenta de Google
                cursor.execute(
                    """
                    INSERT INTO usuarios
                    (google_sub, nombre, correo, foto_url, password_hash)
                    VALUES (%s, %s, %s, %s, NULL)
                    """,
                    (google_sub, nombre or correo, correo, foto_url)
                )

                id_usuario = cursor.lastrowid

        conexion.commit()

        # Crear la sesión de ARES
        token = generar_token_sesion()
        guardar_sesion(id_usuario, token)

        response.set_cookie(
            key="ares_sesion",
            value=token,
            httponly=True,
            secure=False,  # Solo desarrollo local con HTTP
            samesite="lax",
            max_age=8 * 60 * 60,
            path="/"
        )

        return {
            "mensaje": "Inicio de sesión con Google exitoso",
            "usuario": {
                "id_usuario": id_usuario,
                "nombre": nombre,
                "correo": correo
            }
        }

    except pymysql.IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se pudo registrar la cuenta de Google"
        )

    finally:
        conexion.close()
