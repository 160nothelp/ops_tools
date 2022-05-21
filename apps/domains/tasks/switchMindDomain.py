import random
from collections import Counter
from django.db.models import Q
import CloudFlare
from celery import shared_task

from domains.models import CloudFlareDnsParseRecordsListModel, CloudFlareMindDomainModel


per_page = 50
debug = False
raw = True


@shared_task()
def checkHealth():
    monitorDomainQuery = CloudFlareDnsParseRecordsListModel.objects.filter(isMonitor=True)
    for monitorDomainObj in monitorDomainQuery:
        codeList = [i.HttpCode for i in monitorDomainObj.statusOfServer.all()]
        ratioDir = ratio(codeList)
        # ipList = [i.cf_records_content for i in monitorDomainQuery]. \
        #     remove(monitorDomainObj.cf_records_content)
        if (ratioTmp := ratioDir.get(200)) is not None:
            if not float(ratioTmp) <= 1:
                timeList = [i.TotalTime for i in monitorDomainObj.statusOfServer.all()]
                maxTime = sort(timeList)[-1]
                if float(maxTime) < 30:
                    continue
        ipList = ['154.23.237.9', '8.210.173.64', '47.57.70.212', '47.57.140.227']

        sameRecordsQuery = [i.cf_records_content for i in CloudFlareDnsParseRecordsListModel.objects.filter(
            Q(isMonitor=True) &
            Q(cf_records_name=monitorDomainObj.cf_records_name))]
        for ip in sameRecordsQuery:
            try:
                ipList.remove(ip)
            except Exception as e:
                pass
        switch.delay(monitorDomainObj, ipList)


def ratio(data):
    countDict = Counter(data)
    proportionDict = dict()

    for i in countDict:
        proportionDict[i] = str(countDict[i] / len(data) * 100)[:5]

    return proportionDict


def sort(li):
    for i in range(len(li) - 1):
        for j in range(len(li) - 1 - i):
            if li[j] > li[j + 1]:
                li[j], li[j + 1] = li[j + 1], li[j]
    return li


@shared_task()
def switch(monitorDomainObj, ipList):
    ip = random.choice(ipList)
    mindDomainObj = CloudFlareMindDomainModel.objects.all()[0]
    cf = CloudFlare.CloudFlare(email=mindDomainObj.cf_accout_email,
                               token=mindDomainObj.cf_api_key,
                               debug=debug,
                               raw=raw)

    try:
        dns_records = {
            'name': monitorDomainObj.cf_records_name,
            'type': 'A',
            'content': ip,
            'ttl': 1,
            'proxied': False
        }
        raw_results = cf.zones.dns_records.put(mindDomainObj.mind_domain_id,
                                               monitorDomainObj.cf_records_id,
                                               data=dns_records)
        monitorDomainObj.cf_records_content = ip
        monitorDomainObj.save()
        for statusObj in monitorDomainObj.statusOfServer.all():
            statusObj.HttpCode = 200
            statusObj.TotalTime=0.0001
            statusObj.save()
    except Exception as e:
        print(e)
