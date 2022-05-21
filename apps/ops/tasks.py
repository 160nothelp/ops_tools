import json
import base64
from django.conf import settings
from celery import shared_task
import oss2

from .models import FgcBitopImgAliossUpdateInfoModel, FgcBitopImgAliossUpdateTaskModel, \
    MkAliossUpdateTaskModel, MkAliossUpdateInfoModel, SidAliossUpdateInfoModel, SidAliossUpdateTaskModel, \
    UIAliossUpdateInfoModel, UIAliossUpdateTaskModel


@shared_task
def Fcg24ImgAliossUpdate(task_id):
    aliyun_key = FgcBitopImgAliossUpdateInfoModel.objects.all()[0]
    oss_update_task = FgcBitopImgAliossUpdateTaskModel.objects.get(id=task_id)
    ossUpdate(oss_update_task, aliyun_key)


@shared_task
def MkAliossUpdate(task_id):
    aliyun_key = MkAliossUpdateInfoModel.objects.all()[0]
    oss_update_task = MkAliossUpdateTaskModel.objects.get(id=task_id)
    ossUpdate(oss_update_task, aliyun_key)


@shared_task
def SidAliossUpdate(task_id):
    aliyun_key = SidAliossUpdateInfoModel.objects.all()[0]
    oss_update_task = SidAliossUpdateTaskModel.objects.get(id=task_id)
    ossUpdate(oss_update_task, aliyun_key)


@shared_task
def UIAliossUpdate(task_id):
    aliyun_key = UIAliossUpdateInfoModel.objects.all()[0]
    oss_update_task = UIAliossUpdateTaskModel.objects.get(id=task_id)
    ossUpdate(oss_update_task, aliyun_key)


def ossUpdate(oss_update_task, aliyun_key):
    full_path = settings.MEDIA_ROOT + oss_update_task.image_file.filepath
    file_name = oss_update_task.image_file.filename
    print(full_path, file_name)

    auth = oss2.Auth(aliyun_key.aliyunAccessKeyId, aliyun_key.aliyunAccessKeySecret)
    bucket = oss2.Bucket(auth, aliyun_key.aliyunEndpoint, aliyun_key.aliyunBucketName)

    def encode_callback(callback_params):
        cb_str = json.dumps(callback_params).strip()
        return oss2.compat.to_string(base64.b64encode(oss2.compat.to_bytes(cb_str)))

    callback_params = {}
    callback_params['callbackBody'] = 'bucket=${bucket}&object=${object}'
    callback_params['callbackBodyType'] = 'application/x-www-form-urlencoded'
    encoded_callback = encode_callback(callback_params)
    callback_var_params = {'x:my_var1': 'my_val1', 'x:my_var2': 'my_val2'}
    encoded_callback_var = encode_callback(callback_var_params)
    params = {'callback': encoded_callback, 'callback-var': encoded_callback_var}
    result = bucket.put_object_from_file(file_name, full_path, params)
    if result.status == 200:
        oss_update_task.img_url = '%s%s' % (aliyun_key.oss_url, file_name)
    else:
        oss_update_task.img_url = '上传oss失败'
    oss_update_task.status = True
    oss_update_task.result = result.resp.read()
    oss_update_task.save()
