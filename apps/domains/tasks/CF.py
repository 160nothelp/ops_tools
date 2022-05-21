import datetime
import CloudFlare
from celery import shared_task
from dateutil import parser

from domains.models import CloudFlareMindDomainModel, CloudFlareDnsParseRecordsListModel


per_page = 50
debug = False
raw = True


@shared_task()
def getMindDomainRecords():
    mindDomainObj = CloudFlareMindDomainModel.objects.all()[0]
    cf = CloudFlare.CloudFlare(email=mindDomainObj.cf_accout_email,
                               token=mindDomainObj.cf_api_key,
                               debug=debug,
                               raw=raw)
    page_number = 0
    while True:
        try:
            page_number += 1
            raw_results = cf.zones.dns_records.get(mindDomainObj.mind_domain_id,
                                                   params={'per_page': per_page,
                                                           'page': page_number})
            records = raw_results['result']
            for record in records:
                CloudFlareDnsParseRecordsListModel.objects.update_or_create(
                    cf_records_id=record['id'],
                    defaults={'cf_records_id': record['id'],
                              'cf_records_type': record['type'],
                              'cf_records_name': record['name'],
                              'cf_records_content': record['content'],
                              'cf_records_proxiable': record['proxiable'],
                              'cf_records_proxied': record['proxied'],
                              'cf_records_ttl': record['ttl'],
                              'cf_records_zone_name': record['zone_name'],
                              'cf_records_created_on': record['created_on'],
                              'cf_records_modified_on': record['modified_on'],
                              'cf_mind_domain': mindDomainObj
                              })
            total_pages = raw_results['result_info']['total_pages']
            if page_number >= total_pages:
                break
        except Exception as e:
            print('error:', e)


@shared_task()
def deleteOldMindDomain():
    mindDomainQuery = CloudFlareDnsParseRecordsListModel.objects.all()
    for mindDomainObj in mindDomainQuery:
        if mindDomainObj.update_time:
            ten_minutes_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
            if parser.parse(ten_minutes_ago.strftime('%Y-%m-%d %H:%M:%S.%f')) > \
                    parser.parse(mindDomainObj.update_time.strftime('%Y-%m-%d %H:%M:%S.%f')):
                mindDomainObj.delete()

