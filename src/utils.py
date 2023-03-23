from re import match
import kopf
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


# _parse_spec_database_name
# description: validate spec database name against regex match expression
# inputs: target_database (str)
# output: target_database (str)
def _parse_spec_database_name (target_database: str) -> str:
    # Validate input target_database to prevent sql injection on database creation
    if not match("^[a-zA-z][a-zA-Z0-9_]*$", target_database):
        raise kopf.PermanentError(f"""
                Invalid parameter: {target_database}!
                Target database name must start with a letter, followed by any number of alpha-numeric
                characters or underscores!""")
    return target_database


# _log_message
# description: sends logging messages on the desired output stream
# inputs: stream (str), message (str)
# output: none
def _log_message (stream: str, message: str):
    # Validate output "stream" name, so as to not expose other methods and properties
    if stream in ("info", "warning", "error", "critical"):
        getattr(logging, stream)(message)


# _log_spec_definition
# description: outputs the pgDatabase ingress spec in YAML format to info stream
# inputs: target_server (str), target_database (str)
# output: none
def _log_spec_definition(target_server: str, target_database: str):
    _log_message('info', f"""
#spec yaml
spec: 
  server: {target_server}
    db:
      name: {target_database}""")