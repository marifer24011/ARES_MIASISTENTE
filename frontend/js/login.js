const formulario = document.getElementById("form-login");

formulario.addEventListener("submit", async function (evento) {
    evento.preventDefault();

    const correo = document.getElementById("email").value;
    const contrasena = document.getElementById("password").value;

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
            alert("¡Bienvenido a Mi Asistente, " +datos.usuario.nombre + "!");
        } else {
            alert(datos.detail || "No se pudo iniciar sesión");
        }
    } catch (error) {
        console.error("Error de conexión:", error);
        alert("No se pudo conectar con el servidor");
    }
    
});