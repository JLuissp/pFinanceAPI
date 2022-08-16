from logging import exception
from urllib import request
from flask import Flask, request, jsonify, render_template
from database.database import dataBase
from sql_model import db, Transactions
from datetime import datetime, date, timedelta, timezone

PATH = 'database/pFinanceDB.sqlite3'

_database = dataBase(PATH)
#_database.create_db()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/Transactions.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/add_transaction', methods=['POST'])
def addTransaction():
    print(request.form)
    try:
        transaction_date = datetime.now(tz=timezone(-timedelta(hours=5)))#.strftime("%Y-%m-%d %H:%M:%S")
        concept = request.form["concepto"]
        payment_method = int(request.form['payment-method'])
        transaction_type = int(request.form['transaction-type'])
        amount = float(request.form['amount'])

        single_transaction = Transactions(transaction_date, concept, payment_method, transaction_type, amount)

        db.session.add(single_transaction)
        db.session.commit()
        return render_template('index.html')
    except Exception:
        exception('\n [SERVER] error in route /api/add_transaction')
        return jsonify({'msg':'no fue posbible añadir la transacción.'})

@app.route('/api/transactions', methods=['GET'])
def getTransactionsBy():

    try:
        transactions=None
        if len(request.args)==0:
            transactions = Transactions.query.all()

        if 'month' in request.args and 'year' in request.args:
            year_ = int(request.args['year'])
            month_ = int(request.args['month'])
            month_days = (date(year_, month_+1, 1) - date(year_, month_, 1)).days
            transactions = Transactions.query.filter(Transactions.date >= date(year_, month_, 1)).filter(Transactions.date <= date(year_, month_, month_days)).all()
        if 'month' in request.args and 'year' not in request.args:
            year_ = datetime.now().year
            month_ = int(request.args['month'])
            month_days = (date(year_, month_+1, 1) - date(year_, month_, 1)).days
            transactions = Transactions.query.filter(Transactions.date >= date(year_, month_, 1)).filter(Transactions.date <= date(year_, month_, month_days)).all()
        if ('year' in request.args) and ('month' not in request.args):
            year_ = int(request.args['year'])
            transactions = Transactions.query.filter(Transactions.date >= date(year_, 1, 1)).filter(Transactions.date <= date(year_+1,1,1))

        serializedData = [transaction.serialized() for transaction in transactions]
        return jsonify(serializedData)
    except Exception:
            exception('[SERVER]: Error')
            return jsonify({'msg': 'Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=4000)