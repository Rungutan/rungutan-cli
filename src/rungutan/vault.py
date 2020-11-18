from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def vault(subcommand, profile_name,  vault_id, key_storage_type, key_name, key_value):

    payload = {}
    if subcommand in ["remove", "get", "edit", "list"]:
        if vault_id is not None:
            payload["vault_id"] = vault_id

    if subcommand in ["add", "edit"]:
        payload["key_storage_type"] = key_storage_type
        payload["key_name"] = key_name
        payload["key_value"] = key_value

    vault_path = path("vault", subcommand)

    response = send_request(
        vault_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])
        exit(0)
    else:
        print_message(response["error"])
        exit(1)
