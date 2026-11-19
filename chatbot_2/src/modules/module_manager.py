
import json
import unicodedata

from chatbot_2.src.modules.chatbot import crear_chatbot, BASE_DIR


UMBRAL_CONFIANZA = 0.7

RESPUESTA_SIN_COINCIDENCIA = (
    "No tengo una respuesta para eso. "
    "Puedes reformular tu consulta."
)


class ModuleManager:

    def __init__(self):

        self.config_path = (
            BASE_DIR / "config" / "modulos.json"
        )

        self.database_dir = BASE_DIR / "databases"

        with open(
            self.config_path,
            "r",
            encoding="utf-8"
        ) as archivo:
            self.config = json.load(archivo)

        self.modulos_config = self.config["modulos"]
        self.transiciones = self.config.get("transiciones", [])


        self.modulos_permanentes = list(
            self.config.get("modulos_permanentes", [])
        )

        self.modulos_contextuales = list(
            self.config.get("modulos_iniciales", [])
        )

        self.bots = {}

        self._validar_modulos(
            self.modulos_permanentes +
            self.modulos_contextuales
        )

        for nombre in self.modulos_activos:
            self.cargar_modulo(nombre)

    @property
    def modulos_activos(self):

        return list(dict.fromkeys(
            self.modulos_permanentes +
            self.modulos_contextuales
        ))

    def _normalizar(self, texto):

        texto = texto.lower().strip()

        texto = unicodedata.normalize(
            "NFD", texto
        )

        return "".join(
            caracter
            for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )

    def _validar_modulos(self, nombres):

        for nombre in nombres:

            if nombre not in self.modulos_config:

                raise ValueError(
                    f"El módulo '{nombre}' no está registrado."
                )

    def cargar_modulo(self, nombre):

        if nombre not in self.modulos_config:

            raise ValueError(
                f"Módulo desconocido: {nombre}"
            )

        if nombre in self.bots:
            return self.bots[nombre]

        configuracion = self.modulos_config[nombre]

        database_path = (
            self.database_dir /
            configuracion["base_datos"]
        )

        if not database_path.exists():

            raise FileNotFoundError(
                f"No existe la base de datos del módulo "
                f"'{nombre}': {database_path}"
            )

        bot = crear_chatbot(
            nombre=f"ARES_{nombre}",
            database_path=database_path,
            solo_lectura=True
        )

        self.bots[nombre] = bot

        return bot

    def cambiar_modulos(self, nuevos_modulos):

        self._validar_modulos(nuevos_modulos)

        nuevos_modulos = list(dict.fromkeys(
            nuevos_modulos
        ))

        nuevos_modulos = [
            nombre
            for nombre in nuevos_modulos
            if nombre not in self.modulos_permanentes
        ]

        for nombre in nuevos_modulos:
            self.cargar_modulo(nombre)

        self.modulos_contextuales = nuevos_modulos

        print(
            f"\n[ARES] Módulos activos: "
            f"{self.modulos_activos}\n"
        )

    def detectar_transicion(self, mensaje):

        mensaje = self._normalizar(mensaje)

        for transicion in self.transiciones:

            frases = [
                self._normalizar(frase)
                for frase in transicion["frases"]
            ]

            if any(
                frase in mensaje
                for frase in frases
            ):

                return transicion

        return None

    def obtener_mejor_respuesta(self, mensaje):

        mejor_respuesta = None
        mejor_confianza = 0

        for nombre in self.modulos_activos:

            bot = self.cargar_modulo(nombre)

            respuesta = bot.get_response(mensaje)

            confianza = respuesta.confidence

            print(
                f"[DEBUG] {nombre}: "
                f"confianza = {confianza:.4f}"
            )

            if confianza > mejor_confianza:

                mejor_confianza = confianza
                mejor_respuesta = respuesta

        if (
            mejor_respuesta is None
            or mejor_confianza < UMBRAL_CONFIANZA
        ):

            return RESPUESTA_SIN_COINCIDENCIA

        return str(mejor_respuesta)

    def responder(self, mensaje):

        transicion = self.detectar_transicion(mensaje)

        if (
            transicion is not None
            and transicion.get("momento") == "antes"
        ):

            self.cambiar_modulos(
                transicion["modulos"]
            )

        respuesta = self.obtener_mejor_respuesta(
            mensaje
        )

        if (
            transicion is not None
            and transicion.get("momento") == "despues"
        ):

            self.cambiar_modulos(
                transicion["modulos"]
            )

        return respuesta
