from flask_migrate import Migrate

from core.app_config import create_app
from workflow.models import db

application = create_app(name="task")
migrate = Migrate(application, db)
