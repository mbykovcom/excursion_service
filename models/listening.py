from datetime import datetime


class Listening:
    def __init__(self, id_user: int, id_excursion_point: int, date_listening: datetime = datetime.now(),
                 _id: int = None):
        self._id: int = _id
        self.id_user: int = id_user
        self.id_excursion_point: int = id_excursion_point
        self.date_listening: datetime = date_listening

    def __repr__(self):
        return f"Listening: {self._id} | id_user: {self.id_user} | id_excursion_point: {self.id_excursion_point} | " \
               f"date date_listening: {self.date_listening}"
