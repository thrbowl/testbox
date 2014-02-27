import sys
from types import FunctionType
from flask.ext.login import login_required

# the decorator login_required from flask login
def _permission_required(permission):
    if type(permission) == FunctionType:
        return login_required(permission)

def patch_login_required():
    sys.modules['flask.ext.login'].login_required = _permission_required

def patch_all():
    patch_login_required()


