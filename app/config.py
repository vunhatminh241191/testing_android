from os import environ
SQLALCHEMY_DATABASE_URI = 'postgresql://testing_android:testing123@localhost/android'
MANDRILL_API_KEY = environ.get('MANDRILL_API_KEY')

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
EMAIL_HOST = 'smtp.mandrillapp.com'