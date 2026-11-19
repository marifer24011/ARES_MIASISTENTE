
from pathlib import Path

from chatterbot import ChatBot
from chatterbot.languages import SPA


BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = BASE_DIR / "databases"


def crear_chatbot(nombre, database_path, solo_lectura=True):

    database_path = Path(database_path)

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    bot = ChatBot(
        nombre,
        tagger_language=SPA,
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri=f"sqlite:///{database_path.as_posix()}",
        read_only=solo_lectura
    )

    return bot