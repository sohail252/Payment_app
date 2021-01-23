from flask import Flask
from flask_restful import Api,Resource, reqparse, abort
import re
import datetime
from decimal import Decimal

app = Flask(__name__)
api = Api(app)

pay_args = reqparse.RequestParser()
pay_args.add_argument("CreditCardNumber", type=str ,help="Type valid credit card number", required=True)
pay_args.add_argument("CardHolder", type=str ,help="Type valid name", required = True)
pay_args.add_argument("SecurityCode", type=str)
pay_args.add_argument("ExpirationDate", type=str ,help="Type valid Date", required = True)
pay_args.add_argument("Amount", type=int ,help="it should be vallid amount", required = True)


#External Gateway
    
class BasePaymentGateway:
	def __init__(self, repeat=0):
		self.repeat = repeat
		self.gateway = None
		
	def __repr__(self):
		return "<{}>".format("BasePaymentGateway")
	
	def connect(self, gateway=None, details=None):
		if gateway != None:
			if self.authenticate(details):
				return True
		return False
	
	def authenticate(self, details=None):
		if details != None:
			return True
		return False
	
	def pay(self, amount, user_details=None, gateway=None):
		if gateway is None:
			gateway = self.gateway
		while self.repeat + 1 > 0:
			if self.connect(gateway, user_details):
				print("payment of {} in gateway {} sucessful".format(amount, self.gateway))
				return True
			self.repeat -= 1
		return False


class PremiumPaymentGateway(BasePaymentGateway):
	def __init__(self, repeat=3):
		super(PremiumPaymentGateway, self).__init__(repeat)
		self.gateway = "PremiumPaymentGatway"
	
	def __repr__(self):
		return "<PremiumPaymentGateway>"


class ExpensivePaymentGateway(BasePaymentGateway):
	def __init__(self, repeat=1):
		super(ExpensivePaymentGateway, self).__init__(repeat)
		self.gateway = "ExpensivePaymentGateway"
	
	def __repr__(self):
		return "<ExpensivePaymentGateway>"


class CheapPaymentGateway(BasePaymentGateway):
	def __init__(self, repeat=0):
		super(CheapPaymentGateway, self).__init__(repeat)
		self.gateway = "CheapPaymentGateway"
	
	def __repr__(self):
		return "<CheapPaymentGateway>"


class ExternalPayment:
	def __init__(self, amount, card_details=None):
		self.amount = amount
		self.card_details = card_details
	
	def make_payment(self,args1):
		try:
			payment_mode = None
			if args1["Amount"] <= 20:
				payment_mode = CheapPaymentGateway()
			elif 20 < args1["Amount"] < 500:
				payment_mode = ExpensivePaymentGateway()
			elif args1["Amount"] >= 500:
				payment_mode = PremiumPaymentGateway()
			else:
				return False
			
			status = payment_mode.pay(args1["Amount"], args1)
			return status
		except:
			return True

def validate_card(card):
	if not re.search(r"^[456]\d{3}(-?\d{4}){3}$", card) or re.search(r"(\d)\1{3}", re.sub("-", "", card)):
		return False
	return True


#ProcessPayment
class Card(Resource):
	
    def get(self):
        args1 = pay_args.parse_args()
        if not type(args1['CreditCardNumber'] == str and validate_card(args1['CreditCardNumber'])) or not len(args1['CreditCardNumber']) == 16:
            print('invalid credit card number')
            return False,400
        if not type(args1['CardHolder']) == str:
            print("card holder is not of string type")
            return False,400
        if not datetime.datetime.strptime(args1['ExpirationDate'], "%Y/%m/%d") > datetime.datetime.now():
            print("date time error")
            return False,400
        try:
            if not Decimal(args1['Amount']) > 0:
                print("amount is invalid")
                return False,400
        except:
            return False
        else:
            return "Payment Successfull"

	
        

api.add_resource(Card,'/ProcessPayments')


if __name__ == '__main__':
    
    app.run(debug=True)