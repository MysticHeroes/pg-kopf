import kopf
from handlers import handle_create_database
from utils import _log_message

_log_message('info', 'Application Started')

@kopf.on.login(retries=3)
def login(**kwargs):
    return kopf.login_via_pykube(**kwargs)

#run on timer, pod creation and resume
@kopf.on.timer("my.local", "v1", "pgdatabases", interval=600, initial_delay=600, idle=30)
@kopf.on.resume("my.local", "v1", "pgdatabases", retries=5, backoff=30)
@kopf.on.create("my.local", "v1", "pgdatabases", retries=5, backoff=30)
def create_database(spec, **kwargs):
    handle_create_database(spec)