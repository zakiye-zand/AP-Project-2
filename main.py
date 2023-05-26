from flask import *
app = Flask(__name__)

@app.route("/")
def root():
    return ""
    
app.run(debug=True)