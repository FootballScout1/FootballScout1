from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
# from api.v1.views.user import *
from api.v1.views.players import *
from api.v1.views.users import *
from api.v1.views.scouts import *
from api.v1.views.clubs import *
from api.v1.views.players_search import *
from api.v1.views.posts import *
from api.v1.views.likes import *
from api.v1.views.comments import *
