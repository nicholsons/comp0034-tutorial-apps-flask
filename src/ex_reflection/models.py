from ex_reflection import db


class Area(db.Model):
    __table__ = db.metadata.tables["Area"]


class RecyclingRate(db.Model):
    __table__ = db.metadata.tables["RecyclingRate"]
