from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from logging import exception
from urllib import request
from flask import Flask, request, jsonify, render_template, url_for, redirect
from database.database import dataBase
from sql_model import db, Transactions
from datetime import datetime, date, timedelta, timezone
import json
import re
import requests as rqst
import pandas as pd

PATH = 'database/pFinanceDB.sqlite3'

_database = dataBase(PATH)
#_database.create_db()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/Transactions.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


def extract_dict(s) -> list:
    results = []
    s_ = ' '.join(s.split('-,')).strip()
    exp = re.compile(r'(\{.*?\})')
    for i in exp.findall(s_):
        try:
            results.append(json.loads(i))        
        except json.JSONDecodeError:
            pass    
    return results

def query_transactions(from_date, to_date=None):
    if to_date is None: to_date = datetime.now(tz=timezone(-timedelta(hours=5))).strftime("%Y-%m-%d")
    _root = f'http://127.0.0.1:4000/api/transactions?from_date={from_date}&to_date={to_date}'

    if from_date == '': _root = 'http://127.0.0.1:4000/api/transactions'
    handler = rqst.get(_root).text
    return json.loads(handler)


@app.route('/', methods=['GET','POST'])
def addTransaction():
    #print(request.form)
    try:
        if request.method == 'POST':

            if request.form['final-json']:
                json_items = request.form['final-json']
                json_items = extract_dict(json_items)
                for item in json_items:

                    item['date'] = datetime.now(tz=timezone(-timedelta(hours=5)))#.strftime("%Y-%m-%d %H:%M:%S")
                    concept = item["concept"]
                    payment_method = int(item['pay_method'])
                    transaction_type = int(item['transaction_type'])
                    amount = float(item['amount'])

                    single_transaction = Transactions(item['date'], concept, payment_method, transaction_type, amount)

                    db.session.add(single_transaction)
                db.session.commit()

        return render_template('index.html')

    except Exception:
        exception('\n [SERVER] error in route /')
        return jsonify({'msg':'no fue posbible añadir la transacción.'})

@app.route('/search', methods=['POST'])
def search_by_date():

    if request.method == 'POST':

        from_date = request.form['input-from-date']

        to_date = request.form['input-to-date']
        if to_date =='': to_date = datetime.now(tz=timezone(-timedelta(hours=5))).strftime("%Y-%m-%d")
        transactions = query_transactions(from_date, to_date)
        transactions = sorted(transactions, key=lambda x: x['date'], reverse=True)
        transactions_df = pd.DataFrame.from_records(transactions)

        balance = transactions_df.amount.sum()
        mean_income = round(transactions_df.amount[transactions_df.transaction_type == 1].mean(), 2)
        mean_outcome = round(transactions_df.amount[transactions_df.transaction_type == 0].mean(), 2)
        
        return render_template('search.html', n=len(transactions), t_list=transactions, balance = balance,mean_income=mean_income ,mean_outcome=mean_outcome)


@app.route('/api/transactions', methods=['GET'])
def getTransactionsBy():

    if request.method =='GET':

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
            if 'from_date' in request.args and 'to_date' in request.args:

                try:
                    from_date = datetime.strptime(request.args['from_date'],'%Y-%m-%d')
                    to_date = datetime.strptime(request.args['to_date'],'%Y-%m-%d')
                except Exception:
                    exception('[SERVER]: Error')
                    return jsonify({'msg': 'input date should be of the form yyy/mm/dd'})

                transactions = Transactions.query.filter(Transactions.date >= from_date).filter(Transactions.date <= to_date)
            if 'from_date' in request.args and 'to_date' not in request.args:

                try:
                    from_date = datetime.strptime(request.args['from_date'],'%Y-%m-%d')
                    to_date =  datetime.now(tz=timezone(-timedelta(hours=5)))
                except Exception:
                    exception('[SERVER]: Error')
                    return jsonify({'msg': 'input date should be of the form yyy/mm/dd'})

                transactions = Transactions.query.filter(Transactions.date >= from_date).filter(Transactions.date <= to_date)

            serializedData = [transaction.serialized() for transaction in transactions]
            return jsonify(serializedData)
        except Exception:
                exception('[SERVER]: Error')
                return jsonify({'msg': 'Error'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=4000)