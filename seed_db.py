import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product

# Customers
customers = [
    {"name": "Alice", "email": "alice@example.com", "phone": "+1234567890"},
    {"name": "Bob", "email": "bob@example.com", "phone": "123-456-7890"},
    {"name": "Carol", "email": "carol@example.com"}
]

for c in customers:
    Customer.objects.get_or_create(**c)

# Products
products = [
    {"name": "Laptop", "price": 999.99, "stock": 10},
    {"name": "Mouse", "price": 25.5, "stock": 100}
]

for p in products:
    Product.objects.get_or_create(**p)

print("Database seeded successfully!")
