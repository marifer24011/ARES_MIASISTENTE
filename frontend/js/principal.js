// Mostrar el nombre del estudiante que inició sesión
async function mostrarNombreUsuario() {
    try {
        const respuesta = await fetch("/usuarios/actual", {
            method: "GET",
            credentials: "same-origin"
        });

        if (!respuesta.ok) {
            console.log("No se encontró una sesión activa");
            return;
        }

        const datos = await respuesta.json();

        const nombreUsuario = document.getElementById("nombre-usuario");

        if (nombreUsuario && datos.usuario) {
            nombreUsuario.textContent = datos.usuario.nombre;
        }

    } catch (error) {
        console.error("Error al obtener el usuario:", error);
    }
}

mostrarNombreUsuario();


/* ===== MANUAL INTERACTIVO DE ARES ===== */

const tramitesManual = [
    {
        titulo: "Constancia de estudios",
        imagen: "img/ConstanciaEstudios.png",
        descripcion: "Documento oficial que acredita que eres estudiante de la institución.",
        pasos: [
            "Identifica qué tipo de constancia necesitas.",
            "Consulta el costo correspondiente.",
            "Realiza el pago mediante un medio autorizado.",
            "Ten a la mano tu número de control.",
            "Acude a Control Escolar para solicitar información sobre la entrega."
        ]
    },
    {
        titulo: "Pago de semestre",
        imagen: "img/PagodeSemestre.png",
        descripcion: "Información sobre el pago correspondiente al periodo escolar.",
        pasos: [
            "Consulta el importe correspondiente al semestre.",
            "Verifica los medios de pago autorizados.",
            "Realiza el pago siguiendo las indicaciones institucionales.",
            "Conserva tu comprobante de pago."
        ]
    }
];

let indiceManual = 0;

const modalManual = document.getElementById("modal-manual");

function actualizarManual() {
    const tramite = tramitesManual[indiceManual];

    document.getElementById("imagen-manual").src = tramite.imagen;
    document.getElementById("imagen-manual").alt = tramite.titulo;

    document.getElementById("titulo-manual").textContent = tramite.titulo;
    document.getElementById("descripcion-manual").textContent =
        tramite.descripcion;

    const lista = document.getElementById("pasos-manual");
    lista.replaceChildren();

    tramite.pasos.forEach(paso => {
        const elemento = document.createElement("li");
        elemento.textContent = paso;
        lista.appendChild(elemento);
    });

    document.getElementById("contador-manual").textContent =
        `${indiceManual + 1} de ${tramitesManual.length}`;

    document.getElementById("anterior-manual").disabled =
        indiceManual === 0;

    document.getElementById("siguiente-manual").disabled =
        indiceManual === tramitesManual.length - 1;
}

// Abrir el manual al seleccionar una tarjeta
document.querySelectorAll(".tarjeta-manual").forEach(tarjeta => {
    tarjeta.addEventListener("click", () => {
        indiceManual = Number(tarjeta.dataset.tramite);
        actualizarManual();
        modalManual.hidden = false;
    });
});

// Cerrar el manual
document.getElementById("cerrar-manual").addEventListener("click", () => {
    modalManual.hidden = true;
});

// Botón Atrás
document.getElementById("anterior-manual").addEventListener("click", () => {
    if (indiceManual > 0) {
        indiceManual--;
        actualizarManual();
    }
});

// Botón Siguiente
document.getElementById("siguiente-manual").addEventListener("click", () => {
    if (indiceManual < tramitesManual.length - 1) {
        indiceManual++;
        actualizarManual();
    }
});

// Cerrar al hacer clic fuera de la ventana
modalManual.addEventListener("click", evento => {
    if (evento.target === modalManual) {
        modalManual.hidden = true;
    }
});

// Cerrar con la tecla Escape
document.addEventListener("keydown", evento => {
    if (evento.key === "Escape" && !modalManual.hidden) {
        modalManual.hidden = true;
    }
});
