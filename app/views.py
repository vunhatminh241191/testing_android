from app import app, db
from flask import request, jsonify, make_response, abort
from models import Account
import datetime
import mandrill
from config import MANDRILL_API_KEY

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

@app.route('/account/<int:account_id>', methods=['GET'])
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
		email = request.json.get('email')
		facebook_id = request.json.get('facebook_id')

		account = Account.query.filter_by(username=username).first()

		if username is None or password is None:
			abort(400) # missing arguments
		if account is not None:
			return login(account, username, password)
		else:
			return signup(username, password, email, facebook_id)

@app.route('/account/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
	account = Account.query.filter_by(id=account_id).first()
	db.session.delete(account)
	db.session.commit()
	return "Delete successful"

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error':'Bad Request'}), 400)

def verify_password(username, password):
	print password
	user = Account.query.filter_by(username = username).first()
	if not user or not user.verify_password(password):
		return False
	return True

def login(account, username, password):
	if verify_password(username, password) == True:
		return "Login Success"
	else:
		return "Username or password is not correct"

def signup(username, password, email, facebook_id):
	user = Account(username=username
		,signup_date=datetime.date.today().strftime("%Y-%m-%d")
		,email=email, facebook_id=facebook_id)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	send_mail('testing_android', [user.email], {})
	return "Adding successful"

def send_mail(template_name, email_to, context):
	mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
	message = {
		'to': [],
		'global_merge_vars': []
	}
	for em in email_to:
		message['to'].append({'email': em})
 
	for k, v in context.iteritems():
		message['global_merge_vars'].append(
			{'name': k, 'content': v}
		)
	mandrill_client.messages.send_template(template_name, [], message)