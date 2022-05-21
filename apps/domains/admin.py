from django.contrib import admin

from .models import CloudFlareMindDomainModel, CloudFlareSSLApiKeyModel

admin.site.register(CloudFlareMindDomainModel)
admin.site.register(CloudFlareSSLApiKeyModel)
