from app import app, db
from flask import request, jsonify, make_response, abort
from models import Account

@app.route('/')
def index():
	return "Hello"

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

		account = Account.query.filter_by(username=username).first()

		if username is None or password is None:
			abort(400) # missing arguments
		if account is not None:
			if verify_password(username, password) == True:
				return "Login Success"
			else:
				return "Username or password is not correct"
			
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

def verify_password(username, password):
    user = Account.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    return True