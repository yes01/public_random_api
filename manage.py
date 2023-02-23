from app import create_app
from flask_script import Manager

app = create_app("development")
# app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.config['JSON_AS_ASCII'] = False

manager = Manager(app)

if __name__ == '__main__':
    manager.run()

