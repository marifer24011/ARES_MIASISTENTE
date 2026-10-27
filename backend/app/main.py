from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Inicializar ARES
app = FastAPI(
    title="ARES - Mi Asistente",
    description="Sistema de orientación y seguimiento de trámites escolares",
    version="1.0.0"
)

# Archivos CSS
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")

# Archivos JavaScript
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

# Página principal de Mi Asistente
@app.get("/")
def inicio():
    return FileResponse("frontend/index.html")