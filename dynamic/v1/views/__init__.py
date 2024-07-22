from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/dynamic/v1')

from dynamic.v1.views.index import *
# from dynamic.v1.views.user import *
from dynamic.v1.views.players import *
from dynamic.v1.views.users import *
from dynamic.v1.views.scouts import *
from dynamic.v1.views.clubs import *
from dynamic.v1.views.players_search import *
from dynamic.v1.views.posts import *
from dynamic.v1.views.likes import *
from dynamic.v1.views.comments import *
from dynamic.v1.views.player_scout import *
