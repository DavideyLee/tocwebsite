from werkzeug.local import Local
from functools import partial
from common.utils import LocalProxy

_thread_locals = Local()

def _find(attr):
    return getattr(_thread_locals, attr, None)

def get_current_org():
    return _find('current_org')

current_org = LocalProxy(partial(_find, 'current_org'))