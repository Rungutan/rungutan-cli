def os_folder():
    return ".rungutan"


def os_file():
    return "credentials"


def os_env_team_id():
    return "RUNGUTAN_TEAM_ID"


def os_env_api_key():
    return "RUNGUTAN_API_KEY"


def hostname():
    return "app.rungutan.com"


def sleep_timeout():
    return 10


def test_running_status():
    return ["STARTING", "VALIDATING", "REFRESHING_WORKERS", "STARTING_WORKERS", "RUNNING_LOADTEST",
            "GENERATE_OVERALL_STATS", "GENERATE_FAILURE_CSV", "GENERATE_REGIONAL_STATS",
            "GENERATE_DETAILED_STATS", "COMPUTE_OVERALL_RESULTS"]


def test_error_status():
    return ["SUBSCRIPTION_INACTIVE", "NOT_ENOUGH_CREDITS", "PAYMENT_FAILURE", "FAILED"]


def test_cancelled_status():
    return ["CANCELLED"]


def test_completed_status():
    return ["FINISHED"]


def test_finished_status():
    return ["FINISHED", "CANCELLED"]


def path(resource, verb):
    rungutan_paths = {
        "domains": {
            "list": "/v1/api/domains/list",
            "add": "/v1/api/domains/add",
            "remove": "/v1/api/domains/remove"
        },
        "notifications": {
            "list": "/v1/api/notifications/list",
            "add": "/v1/api/notifications/add",
            "remove": "/v1/api/notifications/remove"
        },
        "team": {
            "list": "/v1/api/membership/list",
            "add": "/v1/api/membership/add",
            "remove": "/v1/api/membership/remove",
            "change": "/v1/api/membership/change",
            "get": "/v1/api/membership/get"
        },
        "tests": {
            "list": "/v1/api/tests/list",
            "add": "/v1/api/tests/add",
            "cancel": "/v1/api/tests/cancel",
            "get": "/v1/api/tests/get",
            "preview-credits": "/v1/api/credits/preview",
            "set-sharing": "/v1/api/tests/set-sharing",
            "remove": "/v1/api/tests/remove"
        },
        "templates": {
            "list": "/v1/api/templates/list",
            "add": "/v1/api/templates/add",
            "get": "/v1/api/templates/get",
            "remove": "/v1/api/templates/remove"
        },
        "crons": {
            "list": "/v1/api/cron/list",
            "add": "/v1/api/tests/add",
            "remove": "/v1/api/cron/remove",
            "get": "/v1/api/cron/get",
            "preview-credits": "/v1/api/credits/preview",
            "set-status": "/v1/api/cron/set-status"
        },
        "results": {
            "get": "/v1/api/summary-results/get"
        },
        "raw_results": {
            "get": "/v1/api/raw-results/get"
        },
        "vault": {
            "list": "/v1/api/vault/list",
            "add": "/v1/api/vault/add",
            "remove": "/v1/api/vault/remove",
            "get": "/v1/api/vault/get",
            "edit": "/v1/api/vault/edit"
        },
        "csv": {
            "list": "/v1/api/csv/list",
            "get": "/v1/api/csv/get",
            "remove": "/v1/api/csv/remove"
        },
        "certificate": {
            "list": "/v1/api/certificate/list",
            "get": "/v1/api/certificate/get",
            "remove": "/v1/api/certificate/remove"
        },
        "file": {
            "list": "/v1/api/file/list",
            "get": "/v1/api/file/get",
            "remove": "/v1/api/file/remove"
        }
    }
    return rungutan_paths[resource][verb]
