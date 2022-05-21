import CloudFlare
from celery import shared_task
import asyncio

from tools.apiOf17ce_ws_cli import hello
from domains.models import MindDomain17ceStatusModel, CloudFlareDnsParseRecordsListModel


def mindDomain17ce():
    mindDomainQuery = CloudFlareDnsParseRecordsListModel.objects.all()
    for mindDomainObj in mindDomainQuery:
        results = asyncio.get_event_loop().run_until_complete(hello(mindDomainObj.cf_records_name))
        for result in results:
            if result.get('error'):
                MindDomain17ceStatusModel.objects.update_or_create(
                    Record=mindDomainObj,
                    pro_id=result.get('data').get('NodeInfo').get('pro_id'),
                    defaults={
                        'error': result.get('error')
                    }
                )
            else:
                if result.get('type') == 'NewData':
                    MindDomain17ceStatusModel.objects.update_or_create(
                        Record=mindDomainObj,
                        pro_id=result.get('data').get('NodeInfo').get('pro_id'),
                        defaults={
                            'Record': mindDomainObj,
                            'HttpCode': result.get('data').get('HttpCode'),
                            'TotalTime': result.get('data').get('TotalTime'),
                            'pro_id': result.get('data').get('NodeInfo').get('pro_id')
                        }
                    )
