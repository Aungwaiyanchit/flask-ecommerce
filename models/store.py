from xml.dom.pulldom import default_bufsize
from db import db


class StoreModel(db.Model):
    
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship("ItemModel",lazy="dynamic")

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_store_name(cls, name):
        return cls.query.filter_by(name=name).first();
    
    @classmethod
    def get_all_stores(cls):
        return cls.query.all()

    @classmethod
    def delete_by_store_name(cls, name):
        delete_item = cls.query.filter(StoreModel.name==name).delete()
        db.session.commit()
        return delete_item


    def json(self):
        return { "name": self.name, "items": [item.json() for item in self.items.all()] }

    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    