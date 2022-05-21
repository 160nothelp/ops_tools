import os
import time
import OpenSSL
from urllib3.contrib import pyopenssl
from celery import shared_task
from django.utils import timezone
import tldextract
from dateutil import parser
import CloudFlare

from domains.models import CertDirModel, SslCertModel, CertFileModel, CloudFlareSSLApiKeyModel
from tools.ansible_api.myAnsible import MyAnsiable2
from tools.ansible_api.myInventory import MyInventory
from tools.letsEncrypt import create_certificate, renew_verification, save_cer


cert_dir = '/ssl'
per_page = 50
debug = False
raw = True


@shared_task()
def syncDomain():
    # temphosts_list = [{"ip": nginx_ip, "port": "11020", "username": "root", "password": ""}]
    # inv = MyInventory(temphosts_list)
    #
    # ansible2 = MyAnsiable2(inventory=inv.INVENTORY, connection='smart', variable_manager=inv.VARIABLE_MANAGER)
    # ansible2.run(module="shell",
    #              args="grep -Eo '[^.]+\.[^.]+$' /etc/nginx/conf.d/*_domain | awk -F# '{print $1}' | awk -F: '{print $2}'")
    # results = ansible2.get_result()
    # domains = results.get('success').get(nginx_ip).get('stdout_lines')
    # print(domains)
    # for root, dirs, _ in os.walk(cert_dir):
    #     print(root, dirs)
    for dir in os.listdir(cert_dir):
        CertDirModel.objects.update_or_create(node_dir=dir, defaults={
            'node_dir': dir,
        })
    for dirObj in CertDirModel.objects.all():
        for file in os.listdir(os.path.join(cert_dir, dirObj.node_dir)):
            if os.path.splitext(file)[1] == '.pem' or os.path.splitext(file)[1] == '.cer' \
                    or os.path.splitext(file)[1] == '.crt':
                file_path = os.path.join(cert_dir, dirObj.node_dir, file)
                cer = open(file_path, 'r')
                cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cer.read())
                try:
                    domain_ = pyopenssl.get_subj_alt_name(cert)[0][1]
                    first_level = '%s.%s' % (tldextract.extract(domain_).domain, tldextract.extract(domain_).suffix)
                    expire_date = parser.parse(cert.get_notAfter().decode("UTF-8"))
                    sslObj, _ = SslCertModel.objects.get_or_create(domain=first_level)
                    sslObj.cert_dir.add(dirObj)
                    cfileObj, _ = CertFileModel.objects.update_or_create(
                        cert_file=os.path.join(cert_dir, dirObj.node_dir, file),
                        defaults={
                            'cert_file': os.path.join(cert_dir, dirObj.node_dir, file)
                        })
                    sslObj.cert_file.add(cfileObj),
                    SslCertModel.objects.update_or_create(domain=first_level, defaults={
                        'expire_date': expire_date,
                        'days': (expire_date - timezone.now()).days
                    })
                    cer.close()
                except Exception as e:
                    print(file_path)


@shared_task()
def whereIsDns():
    for CerObj in SslCertModel.objects.all():
        for cfObj in CloudFlareSSLApiKeyModel.objects.all():
            cf = CloudFlare.CloudFlare(email=cfObj.cf_accout_email,
                                       token=cfObj.cf_api_key,
                                       debug=debug,
                                       raw=raw)
            raw_results = cf.zones.get(
                params={'name': CerObj.domain, 'status': 'active'})
            if result := raw_results.get('result'):
                SslCertModel.objects.filter(id=CerObj.id).update(cf=cfObj, hasAc=True, cf_zone_id=result[0].get('id'))

            time.sleep(0.2)


@shared_task()
def renewCert():
    for certObj in SslCertModel.objects.filter(hasAc=True):
        if certObj.days <= 10:
            result = create_certificate(certObj.domain)
            if isinstance(result, dict):
                for txt, value in result.items():
                    cfObj = certObj.cf
                    cf = CloudFlare.CloudFlare(email=cfObj.cf_accout_email,
                                               token=cfObj.cf_api_key,
                                               debug=debug,
                                               raw=raw)
                    dns_records = {
                        'name': txt,
                        'type': 'txt',
                        'content': value,
                        'ttl': 1,
                        'proxied': False
                    }
                    raw_results = cf.zones.dns_records.post(certObj.cf_zone_id, data=dns_records)
                time.sleep(180)
                results = renew_verification(certObj.domain)
                print(results)
                if 'Cert success' in results:
                    save_cer(results, certObj)
                elif 'Verify error' in results:
                    certObj.result = 'DNS记录验证失败'
                    certObj.save()
                else:
                    certObj.result = '未知错误'
                    certObj.save()
            else:
                certObj.result = result
                certObj.save()


