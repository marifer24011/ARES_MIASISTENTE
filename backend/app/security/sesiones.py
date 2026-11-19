
import secrets
import hashlib
from datetime import datetime, timedelta, timezone

from backend.app.database.connection import obtener_conexion


def generar_token_sesion():
    return secrets.token_urlsafe(32)


def obtener_hash_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def guardar_sesion(id_usuario, token):
    token_hash = obtener_hash_token(token)

    fecha_expiracion = (
        datetime.now(timezone.utc) + timedelta(hours=8)
    ).replace(tzinfo=None)

    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sesiones (
                    id_usuario,
                    token_hash,
                    fecha_expiracion
                )
                VALUES (%s, %s, %s)
                """,
                (id_usuario, token_hash, fecha_expiracion)
            )

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def validar_sesion(token):
    if not token:
        return None

    token_hash = obtener_hash_token(token)
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_usuario
                FROM sesiones
                WHERE token_hash = %s
                  AND fecha_expiracion > UTC_TIMESTAMP()
                  AND fecha_revocacion IS NULL
                """,
                (token_hash,)
            )

            sesion = cursor.fetchone()

        return sesion["id_usuario"] if sesion else None

    finally:
        conexion.close()
