from flask import *
from sqlite3 import *
from database import *
import requests
conn = connect('legolist.db')
cur = conn.cursor()
stuff = cur.execute("select * from Legos")
stuff = cur.fetchall()
print(stuff)


app = Flask(__name__, template_folder='templates')

cartList = []

@app.route("/") 
def root():
    conn = connect('legolist.db')
    cur = conn.cursor()
    stuff = cur.execute("select * from Legos")
    stuff = cur.fetchall()
    response = requests.get('https://api.sezar.network/CryptoPrice?token=btc')
    btcRate = response.json()['USD']
    btcPrice = []
    for row in stuff:
        btcPrice.append(row[1]/btcRate)

    return render_template('home.html', itemData=stuff , btcPrice= btcPrice)

@app.route("/add") 
def admin():
    return render_template('add.html')

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        title = request.form['name']
        price = request.form['price']
        #pieces = request.form['pieces']
        #ageRate = request.form['ageRate']
        #item = request.form['item']
        #stockCount = request.form['stockcount']
        idCode = request.form['id']#باید یونیک باشه؟
        url = request.form['url']
        newItem = Lego.create(name=title, price=price, id=idCode, url=url)
        newItem.save()
        #stuff.append(newItem)

    return redirect(url_for('root',itemData=stuff))

@app.route("/remove")
def remove():
    return render_template('remove.html', itemData=stuff)


@app.route("/removeItem", methods = ["POST"])
def removeItem():
    if request.method == "POST":
        idCode = int(request.form['id'])
        deleted_record = Lego.get(Lego.id == idCode)
        deleted_record.delete_instance()
        for row in stuff:
            if stuff[0] == idCode:
                stuff.remove(row)

    return redirect(url_for('root',itemData=stuff))

@app.route("/addToCart")
def addToCart():
    productId = int(request.args.get('productId'))
    stockCount = 1
    cartList.append([productId , stockCount])
    return redirect(url_for('root'))

@app.route("/cart")
def cart():
    products = []
    totalPrice = 0
    #اضافه کردن اطلاعات محصولات اضافه شده به سبد خرید بر اساس ای دی کد
    for ware in cartList:
        for row in stuff:
            if ware[0]==row[0]:
                products.append(row)
                totalPrice+=row[1]*ware[1] # محاسبه قیمت کل بر اساس قیمت هر یک و تعداد سفارش داده شده
    response = requests.get('https://api.sezar.network/CryptoPrice?token=btc')
    btcRate = response.json()['USD']
    btcPrice = totalPrice/btcRate

    return render_template("cart.html", cartlist_html= cartList,products_html = products , totalPrice_html = totalPrice ,btcPrice= btcPrice)

@app.route("/removeFromCart", methods=["POST"])
def removeFromCart():
    if request.method == "POST":
        productId = int(request.form['productId'])

        for ware in cartList:
            if ware[0] == productId:
                cartList.remove(ware)

        return redirect(url_for('cart'))

@app.route("/changeCartCount", methods=["GET"])
def changeCartCount():
    productId = int(request.args.get("productId"))
    stockCount = int(request.args.get('stockCount'))
    for ware in cartList:
        if ware[0] == productId:
            ware[1] = stockCount

    return redirect(url_for('cart'))

app.run(debug=True)
