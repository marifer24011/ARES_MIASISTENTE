const formulario = document.getElementById("form-registro");
const mensaje = document.getElementById("mensaje-registro");

formulario.addEventListener("submit", async function (evento) {
    evento.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const contrasena = document.getElementById("contrasena").value;

    mensaje.textContent = "Registrando estudiante...";
    mensaje.className = "";

    try {
        const respuesta = await fetch("/usuarios/registro", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        nombre: nombre,
        correo: correo,
        contrasena: contrasena
    })
});

        const datos = await respuesta.json();

        if (respuesta.ok) {
            mensaje.textContent = "¡Cuenta creada correctamente! Ya puedes iniciar sesión.";
        
            mensaje.className = "exito";

            formulario.reset();

        } else {
            mensaje.textContent =
                typeof datos.detail === "string"
                    ? datos.detail
                    : "No se pudo registrar el estudiante. ";

            mensaje.className = "error";
        }
    } catch (error) {
        console.error("Error de conexion:", error);

        mensaje.textContent = "No se pudo conectar con el servidor.";

        mensaje.className = "error";
    }
});