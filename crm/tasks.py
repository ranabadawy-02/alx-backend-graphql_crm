from celery import shared_task
from datetime import datetime
import requests

@shared_task
def generate_crm_report():
    query = """
    query {
        customersCount
        ordersCount
        totalRevenue
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            timeout=5
        )
        data = response.json().get("data", {})
        customers = data.get("customersCount", 0)
        orders = data.get("ordersCount", 0)
        revenue = data.get("totalRevenue", 0)
    except Exception:
        customers = orders = revenue = 0

    log_file = "/tmp/crm_report_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")
