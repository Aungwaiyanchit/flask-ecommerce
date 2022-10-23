from db import db
import sqlalchemy as sa
from sqlalchemy.orm import relationship
class ItemModel(db.Model):

    __tablename__ = "items"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))
    price = sa.Column(sa.Float(precision=2))
    store_id = sa.Column(sa.Integer, sa.ForeignKey('stores.id'))

    store = relationship('StoreModel', )

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    @classmethod
    def find_item_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def get_items(cls):
        return cls.query.all()

    @classmethod
    def delete_by_item_name(cls, name):
        delete_item = cls.query.filter(ItemModel.name==name).delete()
        db.session.commit()
        return delete_item

    @classmethod
    def update_by_item_name(cls, name, price, store_id):
        update_item = cls.query.filter(ItemModel.name==name).update({"name": name, "price": price, "store_id": store_id})
        db.session.commit()
        return update_item
    
    def json(self):
        return { 'name' : self.name, 'price' : self.price  }
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.remove(self)
        db.session.commit()