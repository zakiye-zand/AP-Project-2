from peewee import *

db = SqliteDatabase('./legolist.db')

class Lego(Model):
    id = IntegerField(primary_key=True)
    price = FloatField(index=True)
    name = CharField(max_length=255)
    url = CharField(max_length=255)

    class Meta:
        database = db
        table_name = 'legos'

db.connect()
db.create_tables([Lego])
db.close()
