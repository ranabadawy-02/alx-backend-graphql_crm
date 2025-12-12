INSTALLED_APPS = [
    # Django apps...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our apps
    'crm',

    # GraphQL
    'graphene_django',
]
GRAPHENE = {
    "SCHEMA": "alx_backend_graphql_crm.schema.schema"
}
