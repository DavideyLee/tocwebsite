from werkzeug.local import Local
from functools import partial
from common.utils import LocalProxy
from .models import Organization

_thread_locals = Local()

def _find(attr):
    return getattr(_thread_locals, attr, None)

def get_current_org():
    return _find('current_org')

def set_current_org(org):
    setattr(_thread_locals, 'current_org', org)

def set_to_root_org():
    set_current_org(Organization.root())

current_org = LocalProxy(partial(_find, 'current_org'))