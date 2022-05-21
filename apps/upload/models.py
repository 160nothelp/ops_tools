from django.db import models
import os
import datetime

from upload.filesize import convert_size
from upload.storage import PathAndRename


class UploadModel(models.Model):

    username = models.CharField(max_length=20, verbose_name=u'上传用户')
    file = models.FileField(upload_to=PathAndRename("./"), blank=True, verbose_name=u'上传文件')
    archive = models.CharField(max_length=201, default='upload-files', null=True, blank=True, verbose_name=u'文件归档')
    filename = models.CharField(max_length=201, null=True, blank=True, verbose_name=u'文件名')
    filepath = models.CharField(max_length=201, null=True, blank=True, verbose_name=u'文件路径')
    type = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'文件类型')
    size = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'文件大小')
    create_time = models.CharField(max_length=201,
                                   null=True, blank=True,
                                   verbose_name=u'文件日期')

    def save(self, *args, **kwargs):
        from re import sub
        self.create_time = datetime.datetime.now().strftime("%y%m%d%H%M%S%f")
        self.size = '{}'.format(convert_size(self.file.size))
        filename = os.path.splitext(self.file.name)
        self.filename = '{}-{}{}'.format(sub('\W+', '', filename[0]), self.create_time, filename[1]).replace(' ', '_')
        self.filepath = '{}/{}'.format(self.archive, self.filename)
        super(UploadModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.filepath

    class Meta:
        verbose_name = u'文件上传'
        verbose_name_plural = u'文件上传'





