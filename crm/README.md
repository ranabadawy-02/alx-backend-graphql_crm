# CRM Celery Setup

## Install dependencies
pip install -r requirements.txt

## Run Migrations
python manage.py migrate

## Start Celery Worker
celery -A crm worker -l info

## Start Celery Beat
celery -A crm beat -l info

## Verify Logs
Check /tmp/crm_report_log.txt for generated weekly reports.
# CRM Celery Setup

## Install Redis and dependencies
sudo apt-get install redis-server
pip install -r requirements.txt

## Run Migrations
python manage.py migrate

## Start Celery Worker
celery -A crm worker -l info

## Start Celery Beat
celery -A crm beat -l info

## Verify Logs
Check /tmp/crm_report_log.txt for generated weekly reports.
