#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

DELETED_COUNT=$(python3 $PROJECT_DIR/manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True) | Customer.objects.filter(orders__created_at__lt=one_year_ago)
deleted, _ = qs.distinct().delete()
print(deleted)
EOF
)

echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT" >> /tmp/customercleanuplog.txt
