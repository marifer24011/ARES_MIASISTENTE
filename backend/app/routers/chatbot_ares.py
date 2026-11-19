"""Adaptador FastAPI para los módulos ChatterBot de Sergio.

Demo local: comparte el contexto del módulo activo entre usuarios.
No bloquea el inicio del servidor: carga el modelo en la primera consulta.
"""
import logging
from threading import Lock

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from chatbot_2.src.modules.module_manager import ModuleManager

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])
_manager = None
_lock = Lock()

class PreguntaChat(BaseModel):
    mensaje: str = Field(min_length=1, max_length=500)

@router.post("/preguntar")
def responder_chat(datos: PreguntaChat):
    global _manager
    # No permitir consultas simultáneas sobre el mismo ModuleManager.
    with _lock:
        try:
            if _manager is None:
                _manager = ModuleManager()
            respuesta = _manager.responder(datos.mensaje.strip())
            return {"respuesta": str(respuesta)}
        except Exception:
            logging.exception("Error en chatbot ARES")
            raise HTTPException(
                status_code=500,
                detail="No se pudo procesar la pregunta. Revisa los logs del backend."
            )
