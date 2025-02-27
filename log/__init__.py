from flask import Blueprint
# 创建蓝图实例
Log = Blueprint('Log', __name__)
from . import views

