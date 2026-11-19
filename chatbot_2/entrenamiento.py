
import json
import tempfile

from pathlib import Path
from chatterbot.trainers import JsonFileTrainer

from chatbot_2.src.modules.chatbot import (
    crear_chatbot,
    BASE_DIR
)


def expandir_conversaciones(datos):
    """
    Convierte las listas de in_response_to
    en registros individuales compatibles
    con JsonFileTrainer.
    """

    registros = datos["conversation"]
    conversaciones = []

    # Identificar entradas ya registradas
    textos_existentes = {
        registro["text"]
        for registro in registros
    }

    entradas_agregadas = set()

    for registro in registros:

        respuesta_a = registro.get("in_response_to")

        # Formato tradicional: str o None
        if not isinstance(respuesta_a, list):
            conversaciones.append(registro.copy())
            continue

        # Formato ampliado: lista de entradas
        for pregunta in dict.fromkeys(respuesta_a):

            if not isinstance(pregunta, str) or not pregunta.strip():
                raise ValueError(
                    "Las entradas de in_response_to "
                    "deben ser textos no vacíos."
                )

            # Crear entrada si no existe
            if (
                pregunta not in textos_existentes
                and pregunta not in entradas_agregadas
            ):

                conversaciones.append({
                    "text": pregunta,
                    "in_response_to": None,
                    "persona": "Estudiante",
                    "conversation": registro.get(
                        "conversation", "training"
                    ),
                    "tags": registro.get("tags", []).copy()
                })

                entradas_agregadas.add(pregunta)

            # Crear una respuesta para esta pregunta
            nueva_respuesta = registro.copy()
            nueva_respuesta["in_response_to"] = pregunta

            conversaciones.append(nueva_respuesta)

    # Mantener los campos esperados por field_map
    for registro in conversaciones:
        registro.setdefault("conversation", "training")
        registro.setdefault("persona", None)
        registro.setdefault("tags", [])
        registro.setdefault("in_response_to", None)

    return {"conversation": conversaciones}


def entrenar():

    config_path = BASE_DIR / "config" / "modulos.json"

    with open(
        config_path,
        "r",
        encoding="utf-8"
    ) as archivo:

        config = json.load(archivo)

    database_dir = BASE_DIR / "databases"

    database_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    print("================================")
    print("     ENTRENAMIENTO DE ARES")
    print("================================")

    for nombre, configuracion in config["modulos"].items():

        ruta_json = (
            BASE_DIR /
            "data" /
            configuracion["archivo"]
        )

        ruta_database = (
            database_dir /
            configuracion["base_datos"]
        )

        if not ruta_json.exists():

            print(
                f"[OMITIDO] No existe {ruta_json.name}"
            )

            continue

        print(f"\nEntrenando módulo: {nombre}")

        # Leer los datos originales
        with open(
            ruta_json,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(archivo)

        # Adaptar el formato personalizado de ARES
        datos_expandidos = expandir_conversaciones(datos)

        print(
            f"[INFO] Registros originales: "
            f"{len(datos['conversation'])}"
        )

        print(
            f"[INFO] Registros expandidos: "
            f"{len(datos_expandidos['conversation'])}"
        )

        # Crear ChatBot en modo entrenamiento
        bot = crear_chatbot(
            nombre=f"ARES_{nombre}",
            database_path=ruta_database,
            solo_lectura=False
        )

        entrenador = JsonFileTrainer(
            bot,
            field_map={
                "text": "text",
                "conversation": "conversation",
                "in_response_to": "in_response_to",
                "persona": "persona",
                "tags": "tags"
            }
        )

        # Crear un JSON temporal para ChatterBot
        with tempfile.TemporaryDirectory() as carpeta:

            ruta_temporal = (
                Path(carpeta) / "entrenamiento.json"
            )

            with open(
                ruta_temporal,
                "w",
                encoding="utf-8"
            ) as archivo:

                json.dump(
                    datos_expandidos,
                    archivo,
                    ensure_ascii=False,
                    indent=4
                )

            # Entrenar usando el formato compatible
            entrenador.train(str(ruta_temporal))

        print(
            f"[OK] Módulo {nombre} entrenado."
        )

    print("\n================================")
    print("  ENTRENAMIENTO COMPLETADO")
    print("================================")


if __name__ == "__main__":

    entrenar()
