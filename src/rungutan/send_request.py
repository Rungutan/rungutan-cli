import simplejson as json
import http.client

from rungutan.config import hostname


def send_request(path, payload, creds, method="POST"):

    try:
        # Initiate connection to Rungutan
        conn = http.client.HTTPSConnection(hostname())
        payload["team_id"] = creds["team_id"]
        headers = {
            "X-Api-Key": creds["api_key"],
            "content-type": "application/json"
        }

        conn.request(str(method).upper(), path, json.dumps(payload), headers)
        res = conn.getresponse()
        data = res.read()

        # Check response
        response = data.decode("utf-8")
        response_json = json.loads(response)

        if int(res.status) >= 300:
            return {
                "error": response_json,
                "success": False
            }
        return {
            "response_json": response_json,
            "success": True
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }
