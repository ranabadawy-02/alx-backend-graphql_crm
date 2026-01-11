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

3. Schedule a GraphQL Mutation for Product Stock Alerts
mandatory
Objective
Create a django-crontab job that runs every 12 hours, uses a GraphQL mutation to update low-stock products (stock < 10), and logs the updates.

Instructions
Define a GraphQL Mutation:
In crm/schema.py, add a UpdateLowStockProducts mutation that:

Queries products with stock < 10.
Increments their stock by 10 (simulating restocking).
Returns a list of updated products and a success message.
Create a Cron Job:
In crm/cron.py, define update_low_stock that:

Executes the UpdateLowStockProducts mutation via the GraphQL endpoint.
Logs updated product names and new stock levels to /tmp/low_stock_updates_log.txt with a timestamp.
In crm/settings.py, add to CRONJOBS:


CRONJOBS = [
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]
Repo:

GitHub repository: alx-backend-graphql_crm
File: crm/schema.py, crm/cron.py, crm/settings.py
