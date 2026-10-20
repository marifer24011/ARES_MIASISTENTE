
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def inicio():
    return """
    <h1>Hola ARES</h1>
    <h2>Prueba de Python 🐍</h2>

    <form action="/sumar" method="post">
        <input type="number" name="a" required>
        <input type="number" name="b" required>
        <button type="submit">Sumar</button>
    </form>
    """

@app.post("/sumar", response_class=HTMLResponse)
def sumar(a: int = Form(...), b: int = Form(...)):
    resultado = a + b

    return f"""
    <h1>Resultado: {resultado}</h1>
    <a href="/">Volver</a>
    """
