from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.routers.usuarios import router as usuarios_router

# Inicializar ARES
app = FastAPI(
    title="ARES - Mi Asistente",
    description="Sistema de orientación y seguimiento de trámites escolares",
    version="1.0.0"
)

# Activar las rutas de usuarios
app.include_router(usuarios_router)

# Archivos CSS
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")

# Archivos JavaScript
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

# Archivos de imágenes
app.mount("/img", StaticFiles(directory="frontend/img"), name="img")

# Página principal de Mi Asistente
@app.get("/")
def inicio():
    return FileResponse("frontend/index.html")