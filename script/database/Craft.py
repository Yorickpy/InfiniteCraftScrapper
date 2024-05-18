import datetime


class Craft:
    def __init__(self, id: int, libelle: str, emoji: str, discovered: bool, created_at: datetime):
        self._id = id
        self._libelle = libelle
        self._emoji = emoji
        self._discovered = discovered
        self._created_at = created_at

    def __str__(self):
            return f"Craft(id={self._id}, libelle='{self._libelle}', emoji='{self._emoji}', " \
               f"discovered={self._discovered}, created_at='{self._created_at}')"
    def isId() -> bool:
        return id != None and isinstance(id, int) and id > 0
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def libelle(self) -> str:
        return self._libelle

    @libelle.setter
    def libelle(self, value: str):
        self._libelle = value

    @property
    def emoji(self) -> str:
        return self._emoji

    @emoji.setter
    def emoji(self, value: str):
        self._emoji = value

    @property
    def discovered(self) -> bool:
        return self._discovered

    @discovered.setter
    def discovered(self, value: bool):
        self._discovered = value

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime):
        self._created_at = value