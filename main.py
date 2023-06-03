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

app.run(debug=True)       