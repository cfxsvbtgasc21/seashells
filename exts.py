from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(retry_after=lambda: 60,key_func=get_remote_address)
db = SQLAlchemy()
mail=Mail()