from peewee import *

db = SqliteDatabase('./legolist.db')

class Lego(Model):
    id = IntegerField(primary_key=True)
    price = FloatField(index=True)
    url = CharField(max_length=255)

    class Meta:
        database = db
        table_name = 'legos'

db.connect()
db.create_tables([Lego])
db.close()

n = int(input("Enter item count: "))
with db:
    for i in range(n):
        try:
            idl = int(input("Lego id: "))
            pl = float(input("Lego price: "))
            urll = input("Lego url: ")
            new_lego = Lego.create(id=idl, price=pl, url=urll)
            new_lego.save()
        except Exception as e:
            print(f"Error: {e}")

with db:
    legos = [lego.url for lego in Lego.select()]
    print(legos)