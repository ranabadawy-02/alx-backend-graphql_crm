#!/usr/bin/env python3

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date 7 days ago
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# GraphQL query
query = gql(
    """
    query GetRecentOrders($date: Date!) {
        orders(orderDate_Gte: $date) {
            id
            customer {
                email
            }
        }
    }
    """
)

result = client.execute(query, variable_values={"date": seven_days_ago})

# Log file
log_file = "/tmp/order_reminders_log.txt"

with open(log_file, "a") as f:
    for order in result.get("orders", []):
        log_line = (
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
            f"Order ID: {order['id']}, "
            f"Customer Email: {order['customer']['email']}\n"
        )
        f.write(log_line)

print("Order reminders processed!")
