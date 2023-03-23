import kopf
from handlers import handle_create_database
from utils import _log_message

_log_message('info', 'Application Started')


# login
# description: Authenticate with Kubernetes API using pykube Kerberos Authentication
# inputs: resource-related kwargs (object)
# output: ConnectionInfo
@kopf.on.login(retries=3)
def login(**kwargs):
    return kopf.login_via_pykube(**kwargs)


# create_database
# description: Process ingresses for pgDatabase type on a timer, # when this pod is created
# or when it is resumed (when paused prior)
# inputs: spec (object)
# output: None
@kopf.on.timer("my.local", "v1", "pgdatabases", interval=600, initial_delay=600, idle=30)
@kopf.on.resume("my.local", "v1", "pgdatabases", retries=5, backoff=30)
@kopf.on.create("my.local", "v1", "pgdatabases", retries=5, backoff=30)
def create_database(spec, **kwargs):
    handle_create_database(spec)