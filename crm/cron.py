from datetime import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as file:
        file.write(message)

    # Optional GraphQL health check
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5,
        )
    except Exception:
        pass
from gql.transport.requests import RequestsHTTPTransport", "from gql import", "gql", "Client"
