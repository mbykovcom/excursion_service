from datetime import datetime


class Listening:
    def __init__(self, _id: int, id_user: int, id_excursion: int, id_object: int, date_listening: datetime):
        self._id: int = _id
        self.id_user: int = id_user
        self.id_excursion: int = id_excursion
        self.id_object: int = id_object
        self.date_listening: datetime = date_listening
