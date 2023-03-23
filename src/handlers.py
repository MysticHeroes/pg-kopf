from utils import _parse_spec_database_name, _log_message
from sql import db_exists, create_database

def handle_create_database (spec):
    target_server = spec["server"]
    target_database = _parse_spec_database_name(spec["db"]["name"])
    _log_message('info', f"""
#spec yaml
spec: 
  server: {target_server}
  db:
    name: {target_database}""")
    if db_exists(target_server, target_database):
        _log_message('warning', f"Target database {target_database} already exists on {target_server}")
    else:
        create_database(target_server, target_database)
