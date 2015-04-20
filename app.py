from flask import Flask, request, jsonify, make_response, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///android'

class Account(db.Model):
	__tablename__ = 'account'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(128))
	signup_date = db.Column(db.DateTime)
	email = db.Column(db.String(120), unique=True)

	def hash_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

@app.route('/accounts', methods=['GET'])
def accounts():
	if request.method == 'GET':
		results = Account.query.limit(10).offset(0).all()
		if len(results) == 0:
			abort(404)
		else: 
			json_results = []
			for result in results:
				d = {'username': result.username,
					 'email': result.email}
				json_results.append(d)
			return jsonify(items=json_results)

@app.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
	account = Account.query.filter_by(id=account_id).first()
	if account == None:
		abort(404)
	else:
		json_results = []
		d = {'username': account.username, 'email': account.email}
		json_results.append(d)
		return jsonify(items=json_results)

@app.route('/accounts', methods=['POST'])
def post_accounts():
	if request.method == 'POST':
		username = request.json.get('username')
		password = request.json.get('password')
		signup_date = request.json.get('signup_date')
		email = request.json.get('email')

		if username is None or password is None:
			abort(400) # missing arguments
		if Account.query.filter_by(username=username).first() is not None:
			abort(400) # existing users
		user = Account(username=username, signup_date=signup_date, email=email)
		user.hash_password(password)
		db.session.add(user)
		db.session.commit()
		return "Adding successful"

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error':'Bad Request'}), 400)

if __name__ == '__main__':
	app.run(debug=True)
