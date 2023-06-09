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

n = int(input("Enter item count: "))

with db:
    for i in range(n):
        try:
            idl = int(input("Lego id: "))
            pl = float(input("Lego price: "))
            nl = input("Lego name: ")
            urll = input("Lego url: ")
            # Check if the Lego object with the given ID already exists
            existing_lego = Lego.get_or_none(id=idl)
            if existing_lego:
                # If it exists, update its price and URL
                existing_lego.price = pl
                existing_lego.name = nl
                existing_lego.url = urll
                existing_lego.save()
            else:
                # If it doesn't exist, create a new Lego object
                new_lego = Lego.create(id=idl, price=pl, name=nl, url=urll)
                new_lego.save()
        except Exception as e:
            print(f"Error: {e}")

with db:
    legos = [lego.url for lego in Lego.select()]
    print(legos)