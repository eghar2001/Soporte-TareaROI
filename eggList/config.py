import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://user:pene.123@localhost/egglist'
    SECRET_KEY = "e49e3f3ea75909673260cea468b84d3a"
    SECURITY_PASSWORD_SALT = SECRET_KEY
    MAIL_SERVER = 'smtp.mail.yahoo.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')