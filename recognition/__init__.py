from flask import Blueprint
# 创建蓝图实例
rec= Blueprint('rec', __name__)
from . import views
