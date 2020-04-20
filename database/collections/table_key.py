from database.connection import Database
from models.other import TableKey


def add(table: str, last_id: int = 1) -> TableKey:
    db = Database()
    collection = db.get_collection('table_keys')
    key_id = collection.insert_one({'table': table, 'last_id': last_id}).inserted_id
    return TableKey(_id=key_id, table=table, last_id=last_id)


def get_last_id(table: str) -> TableKey:
    db = Database()
    collection = db.get_collection('table_keys')
    key = collection.find_one({'table': table})
    if key is None:
        return add(table)
    return TableKey(**key)
