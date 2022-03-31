from flask_migrate import Migrate
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.model import user, cart, cart_item

app = create_app('dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    manager.run()
