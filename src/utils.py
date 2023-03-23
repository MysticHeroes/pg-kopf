from re import match
import kopf
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def _parse_spec_database_name (target_database: str) -> str:
    # Validate input target_database to prevent sql injection on database creation
    if not match("^[a-zA-Z0-9]+$", target_database):
        raise kopf.PermanentError(
                f"Requested db_name must only contain alpha-numeric characters! Invalid parameter: {target_database}"
        )
    return target_database

def _log_message (stream: str, msg: str):
    # Validate output "stream" name, so as to not expose other methods and properties
    if stream in ("info", "warning", "error", "critical"):
        getattr(logging, stream)(msg)
