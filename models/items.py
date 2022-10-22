from db import db

class ItemModle(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float())

    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    @classmethod
    def find_item_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def get_items(cls):
        return cls.query.all()

    @classmethod
    def delete_by_item_name(cls, name):
        delete_item = cls.query.filter(ItemModle.name==name).delete()
        db.session.commit()
        return delete_item

    @classmethod
    def update_by_item_name(cls, name, price):
        update_item = cls.query.filter(ItemModle.name==name).update({"name": name, "price": price})
        db.session.commit()
        return update_item

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.remove(self)
        db.session.commit()