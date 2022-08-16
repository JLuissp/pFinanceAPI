from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Transactions(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    date = db.Column(db.DateTime)
    concept = db.Column(db.Text)
    pay_method = db.Column(db.Integer)
    transaction_type = db.Column(db.Integer)
    amount = db.Column(db.Float)
    
    def __init__(self, date_, concept_, pay_method_, transaction_type_, amount_):
        super().__init__()
        self.date = date_
        self.concept = concept_
        self.pay_method = pay_method_
        self.transaction_type = transaction_type_
        self.amount = amount_

    def __str__(self):
        payment_type = ['efectivo','electronico']
        return f'{self.id}: {self.date} { payment_type[0] if self.transaction_type == 0 else payment_type[1]} {-1*self.amount if self.transaction_type == 0 else self.amount}'

    def serialized(self):

        return {
            'id': self.id,
            'date': self.date,
            'concept' : self.concept,
            'pay_method':self.pay_method,
            'transaction_type':self.transaction_type,
            'amount':self.amount
        }

if __name__ == '__main__':
    print('db created')