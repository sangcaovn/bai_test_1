from flask_migrate import Migrate
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.model import user, cart, cart_item
from flask_cors import CORS

app = create_app('dev')

CORS(app, resources={r"*": {"origins": "*"}},  supports_credentials=True)
# CORS(app, resources={r"/api/*": {"origins": "*"}},  supports_credentials=True)
app.register_blueprint(blueprint)
# ATBBW8W8ybUXdA4agxHZAGsH3UzB224D0D82
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    manager.run()
