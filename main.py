from flask import *
from DB import *

app = Flask(__name__)

@app.route("/") 
def root():
    return render_template('home.html', wares_html = stuff )

@app.route("/add") 
def admin():
    return render_template('add.html')

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        pieces = request.form['pieces']
        ageRate = request.form['ageRate']
        item = request.form['item']
        stockCount = request.form['stockcount']
        idCode = request.form['idcode']#باید یونیک باشه؟
        url = request.form['url']
        newItem = Lego(title , price , pieces , ageRate , item , stockCount , idCode , url)
        stuff.append(newItem)

    return redirect(url_for('root'))    

app.route("/remove")
def remove():
    return render_template('remove.html', wares_html= stuff)

@app.route("/removeItem")
def removeItem():
    idCode = request.args.get('idCode')
    msg = "عملیات ناموفق بود"
    for row in stuff:
        if idCode == row.idCode:
            stuff.remove(row)
            msg = "محصول با موفقیت حذف شد"
        
    print(msg)
    return redirect(url_for('root'))

@app.route("/addToCart")
def addToCart():
    productId = int(request.args.get('productId'))
    stockCount = int(request.args.get('stockCount'))
    cartList.append([productId , stockCount])
    return redirect(url_for('root'))

@app.route("/cart")
def cart():
    products = []
    totalPrice = 0
    #اضافه کردن اطلاعات محصولات اضافه شده به سبد خرید بر اساس ای دی کد
    for ware in cartList:
        for row in stuff:
            if ware[0]==row.idCode:
                products.append(row) 
                totalPrice+=row.price*cartList[1] # محاسبه قیمت کل بر اساس قیمت هر یک و تعداد سفارش داده شده

    return render_template("cart.html", products_html = products , totalPrice_html = totalPrice)

@app.route("/removeFromeCart")
def removeFromeCart():
    productId = int(request.args.get("productId"))
    # حذف کالا از سبد خرید
    for ware in cartList:
        if ware[0]==productId:
            cartList.remove(ware)
    return redirect(url_for('cart'))

@app.route("/changeCartCount")
def changeCartCount():
    productId = int(request.args.get("productId"))
    stockCount = int(request.args.get('stockCount'))
    for ware in cartList:
        if ware[0]==productId:
            cartList[1]=stockCount
            
    return redirect(url_for('cart'))



app.run(debug=True)       