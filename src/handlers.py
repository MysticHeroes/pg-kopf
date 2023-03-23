from utils import _parse_spec_database_name, _log_message, _log_spec_definition
from sql import db_exists, create_database


# handle_create_database
# description: Main code handler for spec validation and database creation
# inputs: spec (object)
# output: None
def handle_create_database (spec):
    target_server = spec["server"]
    target_database = _parse_spec_database_name(spec["db"]["name"])
    _log_spec_definition(target_server, target_database)
    if db_exists(target_server, target_database):
        _log_message('warning', f"Target database {target_database} already exists on {target_server}")
    else:
        create_database(target_server, target_database)
