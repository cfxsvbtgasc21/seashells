HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_app'
USERNAME = 'root'
PASSWORD = '620302'
DB_URI= 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI =DB_URI
