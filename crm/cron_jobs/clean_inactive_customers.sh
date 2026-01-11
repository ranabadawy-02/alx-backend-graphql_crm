#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

count=$(python3 $PROJECT_DIR/manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
count, _ = Customer.objects.filter(
    orders__isnull=True
).delete()

print(count)
EOF
)

echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers count: $count" >> /tmp/customercleanuplog.txt
