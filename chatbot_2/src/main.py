from chatbot_2.src.modules.module_manager import ModuleManager


def main():

    print("================================")
    print("       ASISTENTE ARES")
    print("================================")

    print("Escribe 'salir' para finalizar.\n")

    
    manager = ModuleManager()

    print(
        f"Módulos iniciales: "
        f"{manager.modulos_activos}\n"
    )

    while True:

        mensaje = input("Tú: ").strip()

        if mensaje.lower() == "salir":

            print("ARES: ¡Hasta pronto!")
            break

        if not mensaje:
            continue

        try:

            respuesta = manager.responder(mensaje)

            print(f"ARES: {respuesta}\n")

        except Exception as error:

            print(f"[ERROR] {error}")


if __name__ == "__main__":
    main()
