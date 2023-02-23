from flask import Flask
from Config.config import config
import logging
from logging.handlers import TimedRotatingFileHandler


def create_app(config_name):
    # flask实例对象的初始化
    app = Flask(__name__, template_folder='../templates')

    # 因为vue和render_template的模板都是用{{  }}，所以会冲突，将flask的修改为[[  ]]
    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'

    # 根据配置文件中的字典查找对应的配置类
    conf = config[config_name]

    # 加载配置类到flask项目中
    app.config.from_object(conf)

    # 添加日志
    formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s")
    handler = TimedRotatingFileHandler("Log/flask.log", when="D", interval=1, backupCount=15, encoding="UTF-8", delay=False,
                                       utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    from app.modules.callback import callback_blu
    app.register_blueprint(callback_blu)

    return app
