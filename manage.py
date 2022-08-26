from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://nadine:root@localhost/flask_db'
app.debug=True

