// Interfaz de ARES: reutiliza el HTML/CSS actual del chat.
// Cargar DESPUÉS de principal.js al final de principal.html.
(() => {
    const formulario = document.getElementById('form-chat');
    const campo = document.getElementById('pregunta-chat');
    const conversacion = document.getElementById('conversacion');
    if (!formulario || !campo || !conversacion) {
        console.error('Faltan los elementos del chat en principal.html');
        return;
    }
    const boton = formulario.querySelector('button[type="submit"]');

    function mostrarMensaje(texto, tipo) {
        const contenedor = document.createElement('div');
        contenedor.className = `mensaje ${tipo}`;
        const p = document.createElement('p');
        p.textContent = texto; // Evita insertar HTML recibido.
        contenedor.appendChild(p);
        conversacion.appendChild(contenedor);
        conversacion.scrollTop = conversacion.scrollHeight;
    }

    formulario.addEventListener('submit', async (evento) => {
        evento.preventDefault();
        const mensaje = campo.value.trim();
        if (!mensaje) return;
        mostrarMensaje(mensaje, 'estudiante');
        campo.value = '';
        campo.disabled = true;
        if (boton) boton.disabled = true;

        try {
            const respuesta = await fetch('/api/chatbot/preguntar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({ mensaje })
            });
            const datos = await respuesta.json();
            if (!respuesta.ok) {
                throw new Error(datos.detail || 'No se pudo obtener respuesta');
            }
            mostrarMensaje(datos.respuesta, 'bot');
        } catch (error) {
            console.error('Error del chat:', error);
            mostrarMensaje('No pude responder en este momento. Intenta de nuevo.', 'bot');
        } finally {
            campo.disabled = false;
            if (boton) boton.disabled = false;
            campo.focus();
        }
    });
})();
