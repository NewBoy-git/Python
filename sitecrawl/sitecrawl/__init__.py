from flask import Flask

from sitecrawl.api.crawl_api import api
from sitecrawl.api.select_api import sel
from sitecrawl.api.save_api import sav

from .config import config_map

import logging
from logging.handlers import RotatingFileHandler



# logging.basicConfig(level=logging.DEBUG)
# file_log_handler = RotatingFileHandler('logs/log', encoding='UTF-8')
# # 设置handler 等级为DEBUG
# # 配置日志输出的格式
# logging_format = logging.Formatter(
#     '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
# # 加载日志输出格式
# file_log_handler.setFormatter(logging_format)
# logging.getLogger().addFilter(file_log_handler)



def create_app(config_type):
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_blueprint(sel)
    app.register_blueprint(sav)
    app.config.from_object(config_map[config_type])
    return app



