CELERY_ROUTES = {
    'domains.tasks.CF.getMindDomainRecords': {"queue": "for_task_crontab", "routing_key": "for_task_crontab"},
    'domains.tasks.CF.deleteOldMindDomain': {"queue": "for_task_crontab", "routing_key": "for_task_crontab"},
    # 'domains.tasks.apiOf17ce.mindDomain17ce': {"queue": "for_task_crontab", "routing_key": "for_task_crontab"},
    'domains.tasks.switchMindDomain.checkHealth': {"queue": "for_task_crontab", "routing_key": "for_task_crontab"},
    'domains.tasks.cert.syncDomain': {"queue": "for_task_crontab", "routing_key": "for_task_crontab"},
    'domains.tasks.cert.whereIsDns': {"queue": "for_task_crontab", "routing_key": "for_task_crontab"},
    'domains.tasks.cert.renewCert': {"queue": "for_task_crontab", "routing_key": "for_task_crontab"},
    'domains.tasks.switchMindDomain.switch': {"queue": "for_task_run", "routing_key": "for_task_run"},
    'ops.tasks.Fcg24ImgAliossUpdate': {"queue": "for_task_run", "routing_key": "for_task_run"},
    'ops.tasks.MkAliossUpdate': {"queue": "for_task_run", "routing_key": "for_task_run"},
    'ops.tasks.SidAliossUpdate': {"queue": "for_task_run", "routing_key": "for_task_run"},
    'ops.tasks.UIAliossUpdate': {"queue": "for_task_run", "routing_key": "for_task_run"},
}
