from app import db 
from passlib.apps import custom_app_context as pwd_context

class Account(db.Model):
	__tablename__ = 'accounts'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(128))
	signup_date = db.Column(db.DateTime)
	facebook_id = db.Column(db.String(128))
	email = db.Column(db.String(120), unique=True)

	def hash_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

	def __repr__(self):
		return '<User %r>' % (self.username)