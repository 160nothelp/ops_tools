import os
from django.utils.deconstruct import deconstructible
from re import sub


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, file):
        filename = os.path.splitext(file)
        last_filename = '{}-{}{}'.format(sub('\W+', '', filename[0]), instance.create_time, filename[1]).replace(' ', '_')
        return os.path.join(self.path, instance.archive, last_filename)
