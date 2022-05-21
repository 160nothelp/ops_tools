from celery.schedules import crontab


CELERY_BEAT_SCHEDULE = {
        'getMindDomainRecords': {
            'task': 'domains.tasks.CF.getMindDomainRecords',
            'schedule': crontab(minute='*/5'),
        },
        'delOldMindDomain': {
            'task': 'domains.tasks.CF.deleteOldMindDomain',
            'schedule': crontab(minute='*/5'),
        },
        # 'checkMindDomain17ce': {
        #     'task': 'domains.tasks.apiOf17ce.mindDomain17ce',
        #     'schedule': crontab(minute='*/10'),
        # },
        'switchMindDomain': {
            'task': 'domains.tasks.switchMindDomain.checkHealth',
            'schedule': crontab(minute='*/2'),
        },
        'syncCertDomains': {
            'task': 'domains.tasks.cert.syncDomain',
            'schedule': crontab(minute='*/8')
        },
        'whereIsDns': {
            'task': 'domains.tasks.cert.whereIsDns',
            'schedule': crontab(minute=0, hour=1)
        },
        'renewCert': {
            'task': 'domains.tasks.cert.renewCert',
            'schedule': crontab(minute=30, hour=2)
        }
}
