from flask_script import Manager
from api_1_0.app import app

manager = Manager(app)

if __name__ == '__main__':
    manager.run()