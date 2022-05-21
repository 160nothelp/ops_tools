import subprocess
import re


def create_certificate(domain):
    """
    单域名申请
    :param domain:
    :return:
    """

    cmd = 'acme --issue -d *.%s --dns --yes-I-know-dns-manual-mode-enough-go-ahead-please --force' % domain
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    results = p.stdout.read().decode()
    print(results)
    if 'Cert success' in results:
        return results
    if '"status": 429' in results:
        return '申请超过letsencrypt的速率限制'
    pattern = re.compile("'(.*)'")
    txt_domains = list()
    txt_values = list()
    for result_line in results.splitlines():
        if 'Domain:' in result_line:
            txt_domains.append(pattern.findall(result_line)[0])
        if 'TXT value:' in result_line:
            txt_values.append(pattern.findall(result_line)[0])
    print(txt_domains, txt_values)
    if len(txt_domains) != len(txt_values) or len(txt_domains) == 0:
        return 'acme.sh命令返回值异常1'
    txt_verification = dict(zip(txt_domains, txt_values))
    return txt_verification


def renew_verification(domain):
    cmd = 'acme --renew -d *.%s --yes-I-know-dns-manual-mode-enough-go-ahead-please --force' % domain
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    return p.stdout.read().decode()


def save_cer(results, certObj):
    cer_path = ''
    key_path = ''
    pattern = re.compile(r'((((?<!\w)[A-Z,a-z]:)|(\.{1,2}\\))([^\b%\/\|:\n\"]*))|("\2([^%\/\|:\n\"]*)")|((?<!\w)(\.{1,2})?(?<!\/)(\/((\\\b)|[^ \b%\|:\n\"\\\/])+)+\/?)')
    for result_line in results.splitlines():
        print(result_line)
        if 'And the full chain certs is there:' in result_line:
            cer_path = pattern.search(result_line).group(0)
        if 'Your cert key is in' in result_line:
            key_path = pattern.search(result_line).group(0)
    if cer_path and key_path:
        for certFileObj in (certFileQuery := certObj.cert_file.all()):
            cmd = '\\cp %s %s ' % (cer_path, certFileObj.cert_file)
            p = subprocess.Popen(cmd,  shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            key_file = ''
            for s in certFileObj.cert_file.split('.')[:-1]:
                key_file += s + '.'
            cmd = '\\cp %s %s' % (key_path, key_file + 'key')
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            certObj.result = '完成'
            certObj.save()
    else:
        certObj.result = 'acme.sh命令返回值异常2'
        certObj.save()

