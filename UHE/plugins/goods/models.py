from mongoengine import (DateTimeField, IntField,
                         StringField, ListField)

from UHE.extensions import db


class Goods(db.Document):
    name = StringField()
    price = IntField()
    record = ListField(DateTimeField(),default=[])
    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price,
            'record': self.record,
            'id': str(self.id)
        }

