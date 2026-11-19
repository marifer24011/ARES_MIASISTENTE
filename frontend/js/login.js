
const formulario = document.getElementById("form-login");

formulario.addEventListener("submit", async function (evento) {
    evento.preventDefault();

    const correo = document.getElementById("email").value;
    const contrasena = document.getElementById("password").value;

    const mensaje = document.getElementById("mensaje-login");

    mensaje.textContent = "Verificando credenciales...";
    mensaje.className = "mensaje-login";

    try {
        const respuesta = await fetch("/usuarios/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                correo: correo,
                contrasena: contrasena
            })
        });

        const datos = await respuesta.json();

        if (respuesta.ok) {
            mensaje.textContent =
                "¡Bienvenido a Mi Asistente, " +
                datos.usuario.nombre + "!";

            mensaje.className = "mensaje-login exito";
            window.location.href = "/principal.html"
        } else {
            mensaje.textContent =
                datos.detail || "No se pudo iniciar sesión";

            mensaje.className = "mensaje-login error";
        }

    } catch (error) {
        console.error("Error de conexión:", error);

        mensaje.textContent = "No se pudo conectar con el servidor";
        mensaje.className = "mensaje-login error";
    }
});
