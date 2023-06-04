from peewee import *
LDB = SqliteDatabase('./legolist.db')
class Lego(Model):
    id = IntegerField(primary_key = True)
    price = IntegerField(index = True)
    url = CharField(max_length= 255)
#    constraints = [SQL('UNIQUE (id)')]
    class Meta:
        database = LDB
        table_name = 'Legos'
        indexes = (id, True)
LDB.connect()
LDB.create_tables([Lego])
LDB.close()

n = int(input("Enter item count."))
for i in range(n):
    LDB.connect()
    idl = int(input("lego id"))
    pl = float(input("lego price"))
    urll = input("lego url")
    new_lego = Lego.create(id = idl, price = pl, url = urll)
    new_lego.save()
    LDB.close()
print(LDB)
p = Lego.select()
for i in p:
    print(i.url)