from app.conf.apps import INSTALLED_APPS
from app.conf.core import *
from app.conf.database import *
from app.conf.locale import *
from app.conf.middlewares import MIDDLEWARE

try:
    from app.conf.local_settings import *
except ImportError:
    pass
