from django.db import models


class CloudFlareApiKeyModel(models.Model):
    """
    cf 接口信息
    """
    nickname = models.CharField(max_length=64, unique=True, verbose_name='账号标识名称')
    cf_api_key = models.CharField(max_length=128, verbose_name='cf账号的api—key')
    cf_accout_email = models.EmailField(verbose_name='cf帐号的邮箱')
    create_time = models.DateTimeField(auto_now_add=True)


class CloudFlareMindDomainModel(CloudFlareApiKeyModel):
    """
    cf 中间域名信息
    """
    mind_domain_id = models.CharField(max_length=128, verbose_name='中间域名的ZoneID')

    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ("-create_time",)
        verbose_name = 'CloudFlare中间域名信息'
        verbose_name_plural = verbose_name


class CloudFlareSSLApiKeyModel(CloudFlareApiKeyModel):
    """
    cf 证书验证接口信息
    """

    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ("-create_time",)
        verbose_name = 'CloudFlare证书账号信息'
        verbose_name_plural = verbose_name


class CloudFlareDnsZoneListModel(models.Model):
    """
    cf dns域名表
    """
    id = models.BigAutoField(primary_key=True)
    cf_zone_id = models.CharField(max_length=128)
    domain_name = models.CharField(max_length=255)
    cf_zone_status = models.CharField(max_length=18)
    # cf_account = models.ForeignKey("CloudFlareAccountListModel", null=True, blank=True,
    #                                on_delete=models.SET_NULL, related_name='dns_zone_list')
    # cf_api_key = models.ForeignKey("CloudFlareApiKeyModel", null=True, blank=True,
    #                                on_delete=models.SET_NULL, related_name='dns_zone_list')
    update_time = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('cf_zone_id', 'domain_name', 'cf_zone_status')


class CloudFlareDnsParseRecordsListModel(models.Model):
    """
    cf 每个域名的解析记录表
    """
    id = models.BigAutoField(primary_key=True)
    cf_records_id = models.CharField(max_length=128)
    cf_records_type = models.CharField(max_length=12)
    cf_records_name = models.CharField(max_length=255)
    cf_records_content = models.CharField(max_length=255)
    cf_records_proxiable = models.BooleanField(default=True)
    cf_records_proxied = models.BooleanField(default=True)
    cf_records_ttl = models.CharField(max_length=10)
    cf_mind_domain = models.ForeignKey("CloudFlareMindDomainModel", null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name='mind_domain_records')
    cf_records_zone_name = models.CharField(max_length=255)
    cf_records_created_on = models.CharField(max_length=128)
    cf_records_modified_on = models.CharField(max_length=128)
    editing = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    isMonitor = models.BooleanField(default=False)

    class Meta:
        ordering = ['-cf_records_created_on']


class MindDomain17ceStatusModel(models.Model):

    proChoices = {
        "0": "未知",
        "12": "香港",
        "180": "北京",
        "183": "内蒙古",
        "184": "台湾",
        "188": "贵州",
        "189": "宁夏",
        "190": "山东",
        "192": "黑龙江",
        "193": "山西",
        "194": "陕西",
        "195": "广东",
        "196": "河南",
        "221": "上海",
        "227": "云南",
        "235": "湖北",
        "236": "安徽",
        "238": "西藏",
        "239": "江西",
        "241": "澳门",
        "243": "天津",
        "250": "河北",
        "346": "新疆",
        "349": "辽宁",
        "350": "湖南",
        "351": "吉林",
        "352": "广西",
        "353": "四川",
        "354": "海南",
        "355": "浙江",
        "356": "青海",
        "357": "江苏",
        "49": "重庆",
        "79": "福建",
        "80": "甘肃",
    }

    error = models.CharField(max_length=128, null=True)
    HttpCode = models.IntegerField(null=True)
    TotalTime = models.FloatField(null=True)
    pro_id = models.IntegerField(choices=proChoices.items(), default=0)
    Record = models.ForeignKey("CloudFlareDnsParseRecordsListModel", null=True, blank=True,
                               on_delete=models.SET_NULL, related_name='statusOf17ce')
    update_time = models.DateTimeField(auto_now=True)


class MindDomainMonitor(models.Model):
    cityChoices = {
        'sh': '上海',
        'bj': '北京',
        'gz': '广州',
        'hk': '香港'
    }

    title = models.CharField(max_length=4, choices=cityChoices.items())
    HttpCode = models.IntegerField(default=0.00)
    TotalTime = models.FloatField(default=0.00)
    Record = models.ForeignKey("CloudFlareDnsParseRecordsListModel", null=True, blank=True,
                               on_delete=models.SET_NULL, related_name='statusOfServer')
    update_time = models.DateTimeField(auto_now=True)


class CertDirModel(models.Model):
    node_dir = models.CharField(max_length=255, unique=True)
    update_time = models.DateTimeField(auto_now=True)


class SslCertModel(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    cert_file = models.ManyToManyField('CertFileModel', related_name='fileToCert')
    expire_date = models.DateTimeField(null=True)
    result = models.TextField(null=True)
    update_time = models.DateTimeField(auto_now=True)
    cert_dir = models.ManyToManyField('CertDirModel', related_name='dirToCert')
    days = models.IntegerField(null=True)
    cf = models.ForeignKey('CloudFlareSSLApiKeyModel', null=True, blank=True,
                           on_delete=models.SET_NULL, related_name='cert')
    hasAc = models.BooleanField(default=False)
    cf_zone_id = models.TextField(null=True)


class CertFileModel(models.Model):
    cert_file = models.CharField(max_length=255, unique=True)
    update_time = models.DateTimeField(auto_now=True)

