from datetime import datetime


class Listening:
    def __init__(self, _id: int, id_user: int, id_excursion: int, date_listening: datetime):
        self._id: int = _id
        self.id_user: int = id_user
        self.id_excursion_point: int = id_excursion
        self.date_listening: datetime = date_listening
