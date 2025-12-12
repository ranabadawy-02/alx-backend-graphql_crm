import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.db import IntegrityError, transaction
import re
from django.utils import timezone

# -------------------
# Types
# -------------------

import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order

# Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"

# Queries
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()

# -------------------
# Mutations
# -------------------

class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if phone:
            pattern = r"^\+?\d[\d\-\s]+$"
            if not re.match(pattern, phone):
                raise Exception("Invalid phone format")
        try:
            customer = Customer.objects.create(name=name, email=email, phone=phone)
            return CreateCustomer(customer=customer, message="Customer created successfully")
        except IntegrityError:
            raise Exception("Email already exists")


class BulkCreateCustomers(graphene.Mutation):
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    class Arguments:
        input = graphene.List(
            graphene.InputObjectType(
                "CustomerInput",
                name=graphene.String(required=True),
                email=graphene.String(required=True),
                phone=graphene.String()
            )
        )

    def mutate(self, info, input):
        created_customers = []
        errors = []

        for customer_data in input:
            try:
                if hasattr(customer_data, "phone") and customer_data.phone:
                    pattern = r"^\+?\d[\d\-\s]+$"
                    if not re.match(pattern, customer_data.phone):
                        raise Exception(f"Invalid phone format for {customer_data.name}")
                customer = Customer.objects.create(
                    name=customer_data.name,
                    email=customer_data.email,
                    phone=getattr(customer_data, "phone", None)
                )
                created_customers.append(customer)
            except Exception as e:
                errors.append(str(e))
        return BulkCreateCustomers(customers=created_customers, errors=errors)


class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int()

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")
        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

    def mutate(self, info, customer_id, product_ids, order_date=None):
        if not product_ids:
            raise Exception("At least one product must be selected")

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Customer ID is invalid")

        products = Product.objects.filter(pk__in=product_ids)
        if products.count() != len(product_ids):
            raise Exception("One or more product IDs are invalid")

        order = Order(customer=customer)
        order.save()  # save first to get an ID
        order.products.set(products)
        order.total_amount = sum(p.price for p in products)
        if order_date:
            order.order_date = order_date
        order.save()

        return CreateOrder(order=order)

# -------------------
# Mutation Class
# -------------------

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
