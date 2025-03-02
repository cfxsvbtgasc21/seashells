from flask import Blueprint
# 创建蓝图实例
blog = Blueprint('blog', __name__)
from . import views
