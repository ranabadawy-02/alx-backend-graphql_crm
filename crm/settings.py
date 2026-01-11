CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]
django_crontab

CRONJOBS = [
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]
INSTALLED_APPS = [
    ...
    'django_celery_beat',
]
