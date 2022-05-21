from django.db import models

from upload.models import UploadModel


class AliossUpdateInfoModel(models.Model):
    aliyunAccessKeyId = models.CharField(max_length=128, verbose_name='阿里云KeyId')
    aliyunAccessKeySecret = models.CharField(verbose_name='阿里云KeySecret', max_length=128)
    aliyunEndpoint = models.CharField(verbose_name='Endpoint', max_length=128)
    aliyunBucketName = models.CharField(max_length=128, verbose_name='Bucket名称')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)


class FgcBitopImgAliossUpdateInfoModel(AliossUpdateInfoModel):

    oss_url = models.TextField(default='https://bitop-email.oss-cn-shenzhen.aliyuncs.com/')

    def __str__(self):
        nickname = 'bitop-img-oss-update-info'
        return nickname

    class Meta:
        ordering = ("-create_time",)
        verbose_name = 'bitop email oss信息'
        verbose_name_plural = verbose_name


class FgcBitopImgAliossUpdateTaskModel(models.Model):
    image_file = models.ForeignKey(UploadModel, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='Upload_to_Fgc24mexAliossUpdateTask',
                                   verbose_name='更新文件')
    result = models.TextField(null=True, blank=True, default='上传至oss中……')
    img_url = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)


class MkAliossUpdateInfoModel(AliossUpdateInfoModel):
    oss_url = models.TextField(default='https://bit-appurl.oss-cn-beijing.aliyuncs.com')

    def __str__(self):
        nickname = 'bitop-img-oss-update-info'
        return nickname

    class Meta:
        ordering = ("-create_time",)
        verbose_name = 'bitop 市场 oss信息'
        verbose_name_plural = verbose_name


class MkAliossUpdateTaskModel(FgcBitopImgAliossUpdateTaskModel):
    pass


class SidAliossUpdateInfoModel(AliossUpdateInfoModel):
    oss_url = models.TextField(default='https://bt-sid.oss-cn-beijing.aliyuncs.com')

    def __str__(self):
        nickname = 'bitop-img-oss-update-info'
        return nickname

    class Meta:
        ordering = ("-create_time",)
        verbose_name = 'bitop 运营sid oss信息'
        verbose_name_plural = verbose_name


class SidAliossUpdateTaskModel(FgcBitopImgAliossUpdateTaskModel):
    pass


class UIAliossUpdateInfoModel(AliossUpdateInfoModel):
    oss_url = models.TextField(default='https://bt-ui.oss-cn-beijing.aliyuncs.com')

    def __str__(self):
        nickname = 'bitop-img-oss-update-info'
        return nickname

    class Meta:
        ordering = ("-create_time",)
        verbose_name = 'bitop UI oss信息'
        verbose_name_plural = verbose_name


class UIAliossUpdateTaskModel(FgcBitopImgAliossUpdateTaskModel):
    pass
